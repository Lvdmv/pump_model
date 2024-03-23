import pump_symbol
from symbols import futures_stream
import streams

if __name__ == '__main__':
    """
    Инициализирует словарь символов pump_symbol, 
    получает URL для фьючерсов и запускает потоки с указанным URL и словарем
    """
    new_dict = pump_symbol.pump_symbol_dict()   # Инициализация словаря символов
    futures_url = futures_stream.futures_url()  # Получение URL для фьючерсов
    stream = streams.Streams  # Инициализация потоков
    stream.threads(futures_url, new_dict)  # Запуск потоков
