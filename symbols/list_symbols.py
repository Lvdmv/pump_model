

def future_symbols(client):
    """
    Функция для извлечения символов фьючерсов

    Attributes
    ----------
    client : объект
        Объект клиента для работы с фьючерсами

    Return:
    ----------
    symbols : list
        Список символов инструментов
    """
    data_fut = client.futures_exchange_info()
    return [
        symbol['symbol'].lower() for symbol in data_fut["symbols"]
        if symbol["contractType"] == "PERPETUAL"
        and symbol['symbol'].endswith('USDT')
    ]