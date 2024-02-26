import pandas as pd
from linear_regression import CustomLinearReg
import numpy as np
from binance.client import Client
import datetime
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
        self.X = None
        self.y = None
        self.lr = CustomLinearReg()

    def data_processing(self, symbol, period=10):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE, limit=period)

        df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                           'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                           'Taker Buy Quote Asset Volume', 'Ignore'])

        # df['Open Time'] = df['Open Time'].astype(int)
        # df['Open_Time'] = self.get_formatted_time(df['Open Time'])
        # print(df[['Open_Time', 'Open', 'High', 'Low', 'Close']])
        self.X = np.array(df[['Volume']]).astype(float)
        self.y = np.array(df['Close']).astype(float)
        return df

    def get_formatted_time(self, timestamp):
        dt_object = datetime.datetime.fromtimestamp(timestamp / 1000.0)
        time_str = dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
        return time_str

    def is_abnormal_volume(self, symbol):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)
        if klines:
            volumes = [float(kline[5]) for kline in klines]
            hourly_average_volume = sum(volumes) / len(volumes)
            self.hourly_average_volumes[symbol] = hourly_average_volume

    # пробитие верхнего канала
    def is_exit_channel_high(self, new_index):
        pass

    # проверка аномального хая
    def anomaly_high(self, corr_index):
        pass

    def pump_clear(self):
        pass

    # ПОИСК ТОЧКИ ВХОДА
    def search_entry_point(self, corr_symbol, corr_price, corr_volume):
        print(f'{corr_symbol}')
        self.data_processing(corr_symbol)
        if int(self.y.sum()) != 0 and  int(self.X.sum()) != 0:
            self.lr.fit(self.X, self.y)
            y_pred = self.lr.predict(np.array([float(corr_volume)]).reshape(-1, 1))
            if y_pred[0] != 0:
                diff_price = np.round(((float(corr_price) - y_pred) / (y_pred + 1e-15)) * 100, 2)
                if diff_price > 1:
                    print(f'$$$$$$$$  PUMP {corr_symbol} {diff_price[0]}%   y_pred = {y_pred[0]} y_corr = {corr_price}')
        print()


