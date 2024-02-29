import pump_symbol
from symbols import futures_stream
import streams

if __name__ == '__main__':
    new_dict = pump_symbol.pump_symbol_dict()
    futures_url = futures_stream.futures_url()
    stream = streams.Streams
    stream.threads(futures_url, new_dict)