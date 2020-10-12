"""Testing alpha vantage API
"""

import json

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators


class Trade:

    def __init__(self, region, category):

        with open(r'C:\Users\Dencan Gan\Credentials\credentials.json') as json_cfg:
            credentials = json.load(json_cfg)

        api = credentials['alpha_vantage']['api_key']

        self.labels = ['Ticker', 'Last', '% Change', 'Change', 'Signal', 'Vol', 'Mkt Cap', 'P/E', 'EPS', 'Employees',
                       'Industry']
        self.link = 'https://www.tradingview.com/markets/stocks-' + region + '/' + category

        self.time_series = TimeSeries(api, output_format='pandas')
        self.technical_indicator = TechIndicators(api)

    def daily_data(self, stock):
        data_daily, meta_data_daily = self.time_series.get_daily(symbol=stock, outputsize='full')
        return data_daily, meta_data_daily

    def intraday_data(self, stock, interval='1min'):
        data_intraday, meta_data_intraday = self.time_series.get_intraday(symbol=stock, interval=interval, outputsize='full')
        return data_intraday, meta_data_intraday

    def simple_moving_average(self, stock):
        sma, meta_sma = self.technical_indicator.get_sma(symbol=stock)
        return sma, meta_sma

    def execute(self, stock_data):

        # Starting price
        execute_price = stock_data['4. close'][0]

        for timestamp, price in stock_data.iterrows():

            # If profited before, assign next closing price and executed price
            if execute_price is None:
                execute_price = price['4. close']

            # If executed price lower than closing, we are profit making
            if execute_price < price['4. close']:
                profit = float(price['4. close'] - execute_price)
                print(timestamp, 'Profit making trade.', profit)

                # Once profited, reset executed price to 0
                execute_price = None

            # Skip and continue
            else:
                print(timestamp, 'Loss making trade.')



