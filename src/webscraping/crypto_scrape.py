"""
Created on: 2nd Aug 19
Author: Dencan Gan

Script for scraping daily btc prices from coin market cap.
"""

from src.utils import soupify
from src.utils import convert_object_to_datetime
from datetime import datetime
import pandas as pd


class Crypto:

    def __init__(self, crypto):
        self.crypto = crypto
        self.labels = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Cap']
        self.pattern = 'td'

    def historic_data(self, start_date=None, end_date=datetime.today().strftime('%Y%m%d')):
        """Pulls specific historical cryptocurrency data from coin market cap and uploads to mongodb.

        Args:
            start_date (str): Start date of period. Acceptable type, yyyymmdd.
            end_date (str): End date, defaults to today.

        Returns:
            d (dict): Dictionary of historical crypto data

        Notes:
            If no start date is found for a specific cryptocurrency, it will return the one-month of historical data
        """

        default_link = r'https://coinmarketcap.com/currencies/' + self.crypto + '/historical-data/'

        if start_date is None:
            # Using coinmarketcap default page (1 month data)
            custom_link = default_link

        else:
            custom_link = default_link + '?start=' + start_date + '&end=' + end_date

        # Pulling html
        soup = soupify(url=custom_link)

        historic_data = []
        for x in (soup.select(self.pattern)):
            historic_data.append(x.text)

        data = {}
        for i, e in enumerate(self.labels):
            data[e] = historic_data[i::7]

        df = pd.DataFrame(data)

        df_ctd = convert_object_to_datetime(s=df).sort_values('Date')
        df_ctd = df_ctd.set_index('Date')
        return df_ctd

    def daily_data(self):
        """Daily scrap function
        """
        link = r'https://coinmarketcap.com/currencies/' + self.crypto + '/historical-data/'

        soup = soupify(url=link)  # Pulling html

        historic_data = []

        for x in (soup.select(self.pattern)):
            print(x.text)
            historic_data.append(x.text)

        day_data = dict(zip(self.labels, historic_data[0:7]))

        df = pd.DataFrame(day_data, index=[0])

        df_ctd = convert_object_to_datetime(s=df).sort_values('Date')
        df_ctd = df_ctd.set_index('Date')

        return df_ctd


if __name__ == '__main__':
    # Initialise crypto class and crypto to scrape
    scrape = Crypto(crypto='bitcoin')
    # df_full = scrape.historic_data()
    df_daily = scrape.daily_data()






