
import pandas as pd
import numpy as np
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()  # переменные среды храняться в env.example
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


# Модель входа
class IsPUMP:
    def __init__(self):
        self.client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)
        self.hourly_average_volumes = dict()
        self.num = 0

    def data_processing(self, symbol, period=14):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=period + 1)

        df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                           'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                           'Taker Buy Quote Asset Volume', 'Ignore'])

        return df

    def is_abnormal_volume(self, symbol):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)
        if klines:
            volumes = [float(kline[5]) for kline in klines]
            hourly_average_volume = sum(volumes) / len(volumes)
            self.hourly_average_volumes[symbol] = hourly_average_volume


    def learn_regression(self):
        # df_r = self.df_corr.iloc[:self.index+1]
        # print('df_r', df_r.shape)
        # self.X = [np.array(range(0, self.index)).reshape(-1, 1)]
        # self.y = df_r
        # print('X=', self.X)
        # print('y=', self.y.shape)
        # self.lr = LinearRegression().fit(self.X, self.y + 2 * df_r.std())
        # return self.lr
        pass

    # пробитие верхнего канала
    def is_exit_channel_high(self, new_index):
        pass

    # проверка аномального хая
    def anomaly_high(self, corr_index):
        pass

    def pump_clear(self):
        pass

    # ПОИСК ТОЧКИ ВХОДА
    def search_entry_point(self, corr_symbol):
        self.num += 1
        print(f'{corr_symbol} {self.num}')
