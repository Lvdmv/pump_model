import symbols
import model

def futures_url():
    """
    Функция для формирования URL для получения данных о фьючерсах

    Return:
    ----------
    new_stream : str
        URL для потоковой передачи данных с информацией о фьючерсах
    """
    client = model.IsPUMP().client  # Инициализация клиента
    futures_symbols = symbols.future_symbols(client)  # Получение символов фьючерсов
    new_stream = 'wss://fstream.binance.com/stream?streams=ftmusdt@kline_1m'  # Базовый URL
    for sym in futures_symbols:
        new_stream += '/' + sym + '@kline_1m'  # Добавление символов для каждого фьючерса в URL
    return new_stream