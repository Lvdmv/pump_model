import symbols
import model


def futures_url():
    client = model.IsPUMP().client
    futures_symbols = symbols.future_symbols(client)
    new_stream = 'wss://fstream.binance.com/stream?streams=ftmusdt@kline_1m'
    for sym in futures_symbols:
        new_stream += '/' + sym + '@kline_1m'
    return new_stream