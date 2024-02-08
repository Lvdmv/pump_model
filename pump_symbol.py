import model
from symbols import list_symbols


def pump_symbol_dict():
    """Создание словаря с тикерами инструментов и объектами класса модели"""
    pump_symbol = dict()
    client = model.IsPUMP().client  # инициализация клиента
    futures_symbols = list_symbols.future_symbols(client)  # список тикеров фьючерсов
    for sym in futures_symbols:
        pump_symbol[sym] = model.pump_model.IsPUMP()
    return pump_symbol