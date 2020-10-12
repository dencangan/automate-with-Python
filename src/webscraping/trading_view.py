"""Scraping financial data from tradingview
"""

import pandas as pd
from src.utils import soupify


def parse_to_df(soup, labels):

    data = []
    for x in (soup.select('td')):
        data.append(x.text)

    keys = {}
    for i, e in enumerate(labels):
        keys[e] = data[i::len(labels)]

    return pd.DataFrame(keys)


def crypto(num=None):

    soup = soupify("https://uk.tradingview.com/markets/cryptocurrencies/prices-all")
    labels = ['Crypto', 'Market_Cap', 'FD_Market_Cap', 'Last', 'Available_Coins', 'Total_Coins',
              'Traded_Volume','Change %']

    df = parse_to_df(soup, labels)
    df['Crypto'] = df['Crypto'].str.replace('\n', "").str.replace("\t", "")

    if num is not None:
        df = df.head(num)

    return df


def stocks(region, category, num=None):
    labels = ['Ticker', 'Last', '% Change', 'Change', 'Signal', 'Vol', 'Mkt Cap', 'P/E', 'EPS', 'Employees',
              'Industry']
    link = 'https://www.tradingview.com/markets/stocks-' + region + '/' + category
    soup = soupify(link)

    df = parse_to_df(soup, labels)
    df['x'] = df['Ticker'].str.strip('\n').str.replace('\t', '').str.split('\n')
    df[['(new_ticker)', 'Name', '(blank)']] = pd.DataFrame(df.x.values.tolist(), index=df.index)
    df = df.drop(columns=['Ticker', '(blank)', 'x'])
    df = df.rename(columns={'(new_ticker)': 'Ticker'})

    stock_detail = df.head(num)[['Name', 'Ticker', 'Last', '% Change', 'Signal', 'Vol', 'Mkt Cap',
                                           'Industry']]

    return stock_detail


def currency(num=None):
    soup = soupify(r"https://uk.tradingview.com/markets/currencies/rates-major/")
    labels = ['Currency_Pair', 'Last', 'Change %', 'Change', 'Bid', 'Ask', 'High', 'Low', 'Rating']

    df = parse_to_df(soup, labels)
    df['Currency_Pair'] = df['Currency_Pair'].str.replace('\n', "").str.replace('\t', '-')

    if num is not None:
        df = df.head(num)

    return df


def indices(num=None):
    soup = soupify(r"https://uk.tradingview.com/markets/indices/quotes-major/")
    labels = ["Index", "Last", "Change %", "Change", "High", "Low", "Rating"]
    df = parse_to_df(soup, labels)
    df['Index'] = df['Index'].str.replace('\n', "").str.replace('\t', '-')

    if num is not None:
        df = df.head(num)

    return df


if __name__ == "__main__":

    df_indices = indices(num=None)