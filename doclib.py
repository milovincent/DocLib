import websockets
import websocket
import json
import re
import random
import argparse
from attrdict import AttrDict

parser = argparse.ArgumentParser(description='A euphoria.io bot library.')
parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')


class message:
    def __init__(self, json={}):
        self.dict = AttrDict(json)

class bot:
    def __init__(self, nick, room, owner = ""):
        args = parser.parse_args(args = ["--test", "--debug", "-t"], namespace = self)
        self.nick = nick
        self.room = room if not self.test else "test"
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = owner

    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        self.setNick(self.nick)
        print('connected.')

    def sendMsg(self, msg, parent=message(self.conn.recv()))):
        if re.search(r"^\[.+,.+\]$", msg):
            msg = random.choice(msg[1:-1].split(","))
        self.conn.send(json.dumps({'type': 'send', 'data': {'content': msg, 'parent': parent.dict.data.id}}))
        reply = message(json.loads(self.conn.recv()))
        print(f'Message sent: {reply.dict.data.content} replying to: {parent.dict.data.id} by {parent.dict.data.sender.name}')
        return reply

    def restart(self, msg):
        self.conn.close()
        self.connect()
        self.start()
        self.sendMsg("Restarted", msg)

    def start(self):
        try:
            while True:
                msg = message(json.loads(self.conn.recv()))
                if msg.dict.type == 'ping-event':
                    self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.dict.data.time}}))
                    print("Pong!")
                elif msg.dict.type == 'send-event' and msg.dict.data.sender.name != self.nick:
                    if re.search(f'^!kill @{self.normname}$', msg.dict.data.content) != None and "is_manager" in msg.dict.data.sender.keys() or msg.dict.data.sender.name == self.owner:
                        self.kill()
                    if re.search(f'^!kill @{self.normname}$', msg.dict.data.content) != None and "is_manager" in msg.dict.data.sender.keys() or msg.dict.data.sender.name == self.owner:
                        self.restart()
                    for regex, response in self.regexes.items():
                        if re.search(regex, msg.dict.data.content) != None:
                            if callable(response):
                                result = response(self, msg)
                                if type(result) == str:
                                    self.sendMsg(result, msg)
                                elif type(result) == dict:
                                    for send, nick in result.items():
                                        self.setNick(nick)
                                        self.sendMsg(send, msg)
                                    self.setNick(self.nick)
                                elif type(result) == list:
                                    for send in result:
                                        self.sendMsg(send, msg)
                            else:
                                self.sendMsg(response, msg)
                            break
                elif msg.dict.type == 'error':
                    print(msg.dict)
        except Killed:
            pass
    def setNick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise Killed

class Killed(Exception):
    pass
