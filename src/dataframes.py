"""Generic dataframe handling"""

import pandas as pd
import numpy as np
import re
import warnings
import collections


def df_to_ndarry(df, index, values, default_values=np.nan):
    """
    Converts pandas dataframe into N-dimensional arrays stored in a dictionary.
    Column name as key for 'values' specified and 'dims' as key for 'index' specified.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to convert into array and store in dictionary.
    index : list
        Column(s) used to specify dimensions of nd-array.
    values : list
        Column(s) specifying elements to be stored in nd-array.
    default_values : default, np.nan, values to nd-array before populating
        NOTE: default values will be used to initialise output array, and thus affect the dtype
        Be careful when using str for default values, the default value will determine the number of characters
        that can be stored in a cell.

    Returns
    -------
    Dictionary of nd-arrays.

    Example
    -------
    >>> import pandas as pd
    >>> df = pd.DataFrame({"date": ["2020-01-01", "2020-01-02", "2020-01-03"], "col_1": [1, 2, 3], "col_2": [4, 5, 6]})
    >>> ndarry = df_to_ndarry(df, index=["date"], values=["col_1", "col_2"])
    """
    assert np.all(np.in1d(index, df.columns)), f"'index' specified: {index} not in column names: {df.columns}"
    assert np.all(np.in1d(values, df.columns)), f"'values' specified: {values} not in column names: {df.columns}"

    # Create a multi index to determine where to assign in nd-array
    midx = pd.MultiIndex.from_arrays([df[i].values for i in index], names=index)

    values, default_values = np.array(values), np.array(default_values)

    # One default value, multiple values
    if len(values) != len(default_values):
        if (len(values) > 1) & (len(default_values) == 1):
            default_values = np.repeat(default_values, len(values))

    out = dict()
    # get the shape of the nd-array
    shape = [len(i) for i in midx.levels]

    for i, v in enumerate(values):
        # create array matching dimensions, filled with default value
        tmp = np.full(shape, default_values[i])
        # populate using the values and assign to label (location) in nd-array
        tmp[tuple(midx.labels)] = df[v].values.flat
        # store array results in output dictionary
        if v == 'dims':
            print("'dims' detected as key, renaming to '_dims'")
            out['_dims'] = tmp
        else:
            out[v] = tmp

    # Include name of dimensions
    dim_names = collections.OrderedDict()
    for i, n in enumerate(midx.names):
        dim_names[n] = np.array(midx.levels[i])

    out['dims'] = dim_names

    return out


def df_summary(df):
    """Returns summary of a dataframe"""
    x_axis, y_axis = df.shape
    df_cols = list(df)
    df_nan = df.isna().sum().sum()
    df_dtypes = list(df.dtypes.unique())
    print(f"\n{'-'*18}\nDataFrame Summary\n{'-'*18}\nNumber of rows: {x_axis}\nNumber of columns: "
          f"{y_axis}\nColumn names: {df_cols}\nNumber of NaNs: {df_nan}\nUnique dtypes: {df_dtypes}")


def concatenate_columns(sep="", *args, _add=True, na_fill=np.nan):
    """
    Concatenate multiple columns of pd.DataFrame with specified separator.

    Parameters
    ----------
    sep: str
        Concatenation separator string eg '_'.
    _add: bool,
        True will use "add" method.
        False will use "+" method, which is much faster for large df
    na_fill:
        value to provide if any arg is missing (isnull)
    Returns
    -------
        pd.Series of columns
    """

    # check the lens of the arguments, warn if not all the same
    arg_len = set([len(arg) for arg in args])
    if len(arg_len) > 1:
        warnings.warn('Args do not all have the same length')

    df = pd.DataFrame()
    for arg in args:
        # if arg is not a DataFrame or Series: convert to series
        if not isinstance(arg, (pd.DataFrame, pd.Series)):
            raise AssertionError("Input arg must be dataframe or series!")
        # concat data
        df = pd.concat([df, arg], axis=1, ignore_index=True)

    try:
        if _add:
            out = df.astype(str).add(sep).sum(axis=1)

            if sep != "":
                out = out.str.replace("%s+$" % re.escape(sep), "")  # removes trailing sep
        else:
            df = df.astype(str)
            concat_str = (f'%s+"{sep}"+' * df.shape[1]) % tuple([f'df[{x}]' for x in list(df.columns)])
            concat_str = concat_str[:(-4 - len(sep))]
            out = eval(concat_str)

        # Any columns with NaN will concatenate it with NaN. eg. "a" + "_" + NaN
        mask = df.isnull().any(axis=1)
        out[mask] = na_fill
    except AttributeError:
        out = pd.Series()

    return out
