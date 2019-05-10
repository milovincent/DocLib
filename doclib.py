import websockets
import websocket
import json
import re

class bot:
    def __init__(self, nick, room):
        self.nick = nick
        self.room = room

    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        self.setNick(self.nick)
        print("connected.")

    def sendMsg(self, msg, parent={}):
        self.conn.send(json.dumps({'type': 'send', 'data': {'content': msg, "parent": parent['data']['id']}}))
        print(f"Message sent: {msg} replying to: {parent['data']['id']} by {parent['data']['sender']['name']}")

    def start(self):
        while True:
            msg = json.loads(self.conn.recv())
            if msg['type'] == "ping-event":
                self.conn.send(json.dumps({"type": "ping-reply", "data": {"time": msg["data"]["time"]}}))
            elif msg['type'] == "send-event" and msg['data']['sender']['name'] != self.nick:
                for regex, response in self.regexes.items():
                    if re.search("^!kill @DocBot$", msg["data"]["content"]) != None and msg['data']['sender']['is_manager']:
                        self.conn.close()
                    elif re.search(regex, msg["data"]["content"]) != None:
                        if callable(response):
                            result = response(msg)
                            if type(result) == str:
                                self.sendMsg(result, msg)
                            elif type(result) == dict:
                                for message, nick in result.items():
                                    self.setNick(nick)
                                    self.sendMsg(message, msg)
                                self.setNick(self.nick)
                            elif type(result) == list:
                                for message in result:
                                    self.sendMsg(message, msg)
                        else:
                            self.sendMsg(response, msg)
                        break
            elif msg['type'] == "error":
                print(msg)
    def setNick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))
