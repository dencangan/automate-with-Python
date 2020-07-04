"""Generic dataframe handling"""

import pandas as pd
import numpy as np
from re import escape
import warnings


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
                out = out.str.replace("%s+$" % escape(sep), "")  # removes trailing sep
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
