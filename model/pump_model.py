import pandas as pd
from linear_regression import CustomLinearReg
import numpy as np
from binance.client import Client
import datetime
import os
from dotenv import load_dotenv
import requests


load_dotenv()  # переменные среды храняться в env.example
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


# Модель входа
class IsPUMP:
    def __init__(self):
        self.client = Client(api_key=API_KEY, api_secret=API_SECRET,  testnet=False)
        self.hourly_average_volumes = dict()
        self.X = None
        self.y = None
        self.lr = CustomLinearReg()
        self.angle = False
        self.is_not_position = True

    def data_processing(self, symbol, amt_clines):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE,
                                            since='1 minute ago UTC', limit=amt_clines)

        df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                           'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                           'Taker Buy Quote Asset Volume', 'Ignore'])

        self.X = np.array(df[['Volume']]).astype(float)
        self.y = np.array(df['Close']).astype(float)
        return df

    def is_angle_accept(self):
        if abs(self.y[0] - self.y[-1]) <= self.y.std() * 16:
            self.angle = True

    def is_abnormal_volume(self, symbol):
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR, limit=24)
        if klines:
            volumes = [float(kline[5]) for kline in klines]
            hourly_average_volume = sum(volumes) / len(volumes)
            self.hourly_average_volumes[symbol] = hourly_average_volume

    def send_to_telegram(self, message):
        apiURL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        try:
            requests.post(apiURL, json={'chat_id': CHAT_ID, 'text': message})
        except Exception as e:
            print(e)

    # ПОИСК ТОЧКИ ВХОДА
    def search_entry_point(self, corr_symbol, corr_price, corr_volume):
        print(f'{corr_symbol}')

        self.data_processing(corr_symbol, 240)

        if int(self.y.sum()) != 0 and int(self.X.sum()) != 0:
            self.lr.fit(self.X, self.y)
            y_pred = self.lr.predict(np.array([float(corr_volume)]).reshape(-1, 1)) + self.y.std() * 2
            cv = self.y.std() / self.y.mean()
            if y_pred[0] != 0 and cv < 0.009 and float(corr_price) > y_pred:
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                text = f'PUMP {corr_symbol} corr_price = {corr_price} y_pred = {y_pred[0]:.3f} cv = {cv:.3f} {time_now}'
                self.send_to_telegram(text)
                print(text)
                self.is_not_position = False
        print()
