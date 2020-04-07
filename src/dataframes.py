"""Generic dataframe handling"""

import pandas as pd


def df_summary(df):
    """
    Returns summary of a dataframe
    """
    x_axis, y_axis = df.shape
    df_cols = list(df)
    df_nan = df.isna().sum().sum()
    df_dtypes = list(df.dtypes.unique())
    print(f"\n{'-'*18}\nDataFrame Summary\n{'-'*18}\nNumber of rows: {x_axis}\nNumber of columns: "
          f"{y_axis}\nColumn names: {df_cols}\nNumber of NaNs: {df_nan}\nUnique dtypes: {df_dtypes}")


def convert_object_to_datetime(s):
    """
    Turning date from object to np.datetime64

    Parameter
    ----------
        s : pd.Dataframe or pd.Series
            Pass in dataframe if multi column process is needed

    Returns
    -------
        pd.Series
        pd.DataFrame: All columns containing "date" (case in-sensitive) will be amended

    Note:
        This method can handle EITHER "/" or "-" date separators but not a combination of both.
        Users should check that there are no mixtures of separators if s is an array
    """

    def find_format(series):

        # Default separator
        sep = "/"

        if pd.Series(series).str.contains("-").all():
            sep = "-"

        x = pd.Series(series).str.split("/|-", expand=True).values

        try:
            x = x.astype(int)
            month_pattern = "%m"

        except ValueError:
            month_pattern = "%b"

        year_col, month_col, date_col = None, None, None

        for i in range(x.shape[-1]):
            if x[:, i].dtype != object:
                if all(x[:, i].astype(int) > 1000):
                    year_col = i
                elif all(x[:, i].astype(int) <= 12):
                    month_col = i
                elif all(x[:, i].astype(int) <= 31):
                    date_col = i
            else:
                # Only month can be string and must be in the middle
                date_col, month_col, year_col = 0, 1, 2
                break

        assert year_col is not None, "Cannot find year in date string"

        try:
            year_pattern = "%Y" if (x[:, year_col].astype(int) > 1000).all() else "%y"
        except (ValueError, TypeError, IndexError):
            # Last resort couldn't figure format out, let pandas do it
            return None

        def month_and_date(current_sep, m, d, mp):
            if m > d:
                return current_sep.join(["%d", f"{mp}"])
            else:
                return current_sep.join([f"{mp}", "%d"])

        if year_col == 0:
            if month_col is not None and date_col is not None:
                fmt = sep.join((year_pattern, month_and_date(sep, month_col, date_col, month_pattern)))
            else:
                fmt = sep.join([year_pattern, f"{month_pattern}", "%d"])  # default to non US style

        elif year_col == 2:
            if month_col is not None and date_col is not None:
                fmt = sep.join([month_and_date(sep, month_col, date_col, month_pattern), year_pattern])
            else:
                fmt = sep.join(["%d", f"{month_pattern, year_pattern}"])  # default to non US style

        else:
            raise ValueError("Year in the middle of date separators!")

        return fmt

    # This is an extremely fast approach to datetime parsing. Some dates are often repeated.
    # Rather than to re-parse these, we store all unique dates, parse them, and use a lookup to convert all dates.
    if isinstance(s, pd.DataFrame):
        out = s.copy(True)  # this is the bottleneck
        for column_name, column in out.iteritems():
            # Loop through all the columns passed in
            if "date" in column_name.lower():
                if column.dtype != "<M8[ns]" and ~column.isnull().all():
                    # If date is provided as a string then ignore and set to int
                    try:
                        col = column.astype(int)
                        out[column_name] = col
                    except:
                        # Find the date columns(case in-sensitive)
                        # If pandas cant find the format, ignore error and maintain input
                        u_dates = pd.to_datetime(column.unique(),
                                                 format=find_format(column.unique()),
                                                 errors="ignore")
                        dates = dict(zip(column.unique(), u_dates.tolist()))
                        out[column_name] = column.map(dates.get)
        return out

    else:
        if s.dtype == "<M8[ns]":
            return s
        # Get unique dates
        u_dates = pd.to_datetime(s.unique(), format=find_format(s.unique()))
        dates = dict(zip(s.unique(), u_dates.tolist()))
        return s.map(dates.get)