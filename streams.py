import websocket
import threading
import json
import model


class Streams(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(url=url, on_open=self.on_open)

        self.on_message = lambda ws, msg: self.message(msg)
        self.on_error = lambda ws, er: print('Error', er)
        self.on_close = lambda ws: print('### closed ###')
        self.symbol = ''
        self.pump_symbol = model.pump_model.IsPUMP()
        self.run_forever()

    def on_open(self, ws):
        print('Websocket was opened')

    def message(self, msg):
        data_json = json.loads(msg)
        self.symbol = data_json['data']['s']
        self.pump_object = self.dict_object[self.symbol.lower()]
        self.pump_object.search_entry_point(self.symbol, data_json['data']['k']['c'], data_json['data']['k']['v'])

    def threads(aruments, new_dict):
        Streams.dict_object = new_dict
        return threading.Thread(target=Streams, args=(aruments,)).start()