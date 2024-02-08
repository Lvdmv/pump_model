import pump_symbol
import future_stream
import streams

if __name__ == '__main__':
    new_dict = pump_symbol.pump_symbol_dict()
    futures_url = future_stream.futures_url()
    stream = streams.Streams
    stream.threads(futures_url, new_dict)