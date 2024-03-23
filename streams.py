# загрузка основных библиотек
import websocket
import threading
import json

# Создадим класс Streams, наследующий библиотеу WebSocket с приложением WebSocketApp
class Streams(websocket.WebSocketApp):
    """Класс Streams для загрузки данных с биржи Binance

        Attributes
        ----------
        on_message: str
            получает поток данных с биржи
        on_error: str
            присылает сообщение об ошибке
        on_close: str
            присылает сообщение о закрытии подключения
        symbol: str
            символ инструмента
        run_forever
            запускает основной поток данных

        Methods
        -------
        on_open(): str
            метод открытия соединения
        message()
            метод для получения и обработки данных
        threads()
            метод для создания многопоточного запроса по нескольким инструментам
        """
    def __init__(self, url):
        """
        Инициализируем подключение к бирже Binance

        пропишем свойства внутри класса, для открытия соединения, обработки сообщения,
        обработать возможную ошибку и закрытие

        Attributes
        ----------
        url:
            получение url адреса для подключения к бирже
        """
        super().__init__(url=url, on_open=self.on_open) # обращаемся к атрибутам родительского класса websoket
        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, er: print('Error', er)
        self.on_close = lambda ws: print('### closed ###')
        self.symbol = ''
        self.run_forever()

    def on_open(self, ws):
        """
        Открытие соединения

        Parameters
        ----------
        ws: объект WebSocketApp
        """
        print('Websocket was opened')

    def message(self, msg):
        """
        Метод получает поток данных, конвертирует данные с биржи в json объект, а затем фильтрует данные

        Parameters
        ----------
        msg: str
            поток данных
        """
        data_json = json.loads(msg)  # выгрузим json
        self.symbol = data_json['data']['s']
        self.pump_object = self.dict_object[self.symbol.lower()]  # объект класса IsPUMP
        self.pump_object.search_entry_point(self.symbol, data_json['data']['k']['c'], data_json['data']['k']['v']) # поиск точки входа

    def threads(aruments, new_dict):
        """
        Метод для создания многопоточного запроса по нескольким инструментам
        """
        Streams.dict_object = new_dict # объект класса IsPUMP(для каждого символа)
        return threading.Thread(target=Streams, args=(aruments,)).start()