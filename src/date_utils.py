from datetime import datetime
import numpy as np
import pandas as pd


def last_business_date(holidays=None, date=None):
    """
    Input date and retrieves last business date. Takes holidays and weekends into account using holiday list as input.

    Parameter
    ----------
    holidays : list
        List of holiday dates in np.datetime64
    date : str, default datetime today
        Date input should be YYYY-MM-DD

    Returns
    -------
    np.datetime64 of last business date

    Example
    -------
    >>> last_business_date("2019-12-25") # should return "2019-12-24" (Christmas Day)
    >>> last_business_date("2019-04-22") # should return "2019-04-18" (Monday after Good Friday, Thursday)
    >>> last_business_date("2019-10-19") # should return "2019-10-18" (Saturday returns Friday)
    >>> last_business_date("2019-10-20") # should return "2019-10-18" (Sunday returns Friday)
    >>> last_business_date("2019-10-14") # should return "2019-10-11" (Monday returns Friday)
    """

    if holidays is None:
        raise AssertionError("Please input list of holidays.")

    if date is None:
        current_date = np.datetime64(datetime.today(), 'D')

    else:
        current_date = np.datetime64(date)

    # If found in holiday params, offset set to 0
    if current_date in holidays:
        offsets = 0

    # If not found in holiday params, offset set to -1 to get last business day
    else:
        if pd.to_datetime(current_date).weekday() == 5 or pd.to_datetime(current_date).weekday() == 6:
            offsets = 0

        else:
            offsets = -1

    return np.busday_offset(current_date, offsets=offsets, roll='preceding',
                            holidays=holidays)


def look_back_dates(num, holidays, start_date=datetime.today().strftime('%Y-%m-%d')):
    """
    Look back dates, accounting for holidays and weekends.

    Parameters
    ----------
    num : int
        Input number of look back days
    holidays : list
        List of holiday dates in np.datetime64
    start_date : str
        Input date format YYYY-MM-DD, defaults to today's date

    Returns
    -------
    List of numpy.datetime64 dates

    Example
    -------
    >>> look_back_dates(num=5)
    """

    look_back_lst = []
    x = 0
    while x < num:
        start_date = last_business_date(date=start_date, holidays=holidays)
        x += 1
        look_back_lst.append(start_date)
    return look_back_lst