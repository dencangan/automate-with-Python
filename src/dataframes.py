"""Generic dataframe handling"""

import pandas as pd


def df_summary(df):
    """Returns summary of a dataframe"""

    x_axis, y_axis = df.shape
    df_cols = list(df)
    df_nan = df.isna().sum().sum()
    df_dtypes = list(df.dtypes.unique())
    print(f"\n{'-'*18}\nDataFrame Summary\n{'-'*18}\nNumber of rows: {x_axis}\nNumber of columns: "
          f"{y_axis}\nColumn names: {df_cols}\nNumber of NaNs: {df_nan}\nUnique dtypes: {df_dtypes}")

