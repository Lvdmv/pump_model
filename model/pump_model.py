import pandas as pd
from linear_regression import CustomLinearReg
import numpy as np
from binance.client import Client
import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # переменные среды храняться в env.example
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


# Модель входа
class IsPUMP:
    def __init__(self):
        """
        Инициализация класса для поиска точки входа

        Attributes
        ----------
        client: объект
            Объект класса Client
        X: np.array, shape (n_samples, n_features)
            Входные признаки
        y: np.array, shape (n_samples,)
            Целевая переменная
        lr: объект
            Объект класса CustomLinearReg
        is_not_position: bool
            Флаг проверяет открыта ли позиция по инструменту
        Methods
        -------
        data_processing()
            Обработка данных
        send_to_telegram()
            Метод для отправки сообщений
        search_entry_point()
            Метод для определения точки входа
        """
        self.client = Client(api_key=API_KEY, api_secret=API_SECRET)
        self.X = None
        self.y = None
        self.lr = CustomLinearReg()
        self.is_not_position = True

    def data_processing(self, symbol):
        """
        Обработка данных для указанного символа

        Parameters
        ----------
        symbol : str
            Символ инструмента

        Return:
        ----------
        df : pd.DataFrame
            Обработанные данные
        """
        klines = self.client.futures_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1MINUTE,
                                            since='1 minute ago UTC', limit=60)

        df = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                                           'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                                           'Taker Buy Quote Asset Volume', 'Ignore'])

        self.X = np.array(df[['Volume']].iloc[:-1]).astype(float)
        self.y = np.array(df['Close'].iloc[:-1]).astype(float)
        return df

    def send_to_telegram(self, message):
        """
        Отправка сообщения в Telegram

        Parameters
        ----------
        message : str
            Текст сообщения
        """
        apiURL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        try:
            requests.get(apiURL, json={'chat_id': CHAT_ID, 'text': message})
        except requests.exceptions.Timeout:
            print('BOT requests.exceptions.Timeout')

    # ПОИСК ТОЧКИ ВХОДА
    def search_entry_point(self, corr_symbol, corr_price, corr_volume):
        """
        Поиск точки входа

        Parameters
        ----------
        corr_symbol : str
            Символ инструмента
        corr_price : float
            Текущая цена инструмента
        corr_volume : float
            Текущий объем инструмента
        """
        self.data_processing(corr_symbol)
        cv = (self.y.std() / self.y.mean()) * 100  # коэффициент вариации(для определения равномерности распределения значений выборки)

        if int(self.y.sum()) != 0 and int(self.X.sum()) != 0 and cv < 0.9 and float(corr_volume) > self.X.mean() * 2:
            self.lr.fit(self.X, self.y)  # обучение линейной регрессии
            y_pred = self.lr.predict(np.array([float(corr_volume)]).reshape(-1, 1))  # получение предсказания линейной регрессии
            if self.is_not_position and y_pred[0] != 0:
                y_pred_std = y_pred + self.y.std() * 2
                if float(corr_price) > y_pred_std:  # проверка цены актива на аномальное отклонение
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    text = f'PUMP {corr_symbol} corr_price = {corr_price} y_pred = {y_pred[0]:.3f}  cv = {cv:.3f} {time_now}'
                    self.is_not_position = False
                    self.send_to_telegram(text)
