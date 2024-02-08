def future_symbols(client):
    data_fut = client.futures_exchange_info()
    return [
        symbol['symbol'].lower() for symbol in data_fut["symbols"]
        if symbol["contractType"] == "PERPETUAL"
        and symbol['symbol'].endswith('USDT')
    ]