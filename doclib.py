import websockets
import websocket
import json
import re
import random
import argparse
from attrdict import AttrDict

parser = argparse.ArgumentParser(description='A euphoria.io bot library.')
parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_false')


class message:
    def __init__(self, json={}):
        self.dict = AttrDict(json)

class bot:
    def __init__(self, nick, room, owner = ""):
        args = parser.parse_args(args = ["--test", "--debug", "-t"], namespace = self)
        self.nick = nick
        self.room = room if self.test != True else "test"
        print("Debug: " + str(self.test))
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = owner

    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        self.setNick(self.nick)
        print('connected.')

    def sendMsg(self, msgString, parent = None):
        if re.search(r"^\[.+,.+\]$", msgString):
            msgString = random.choice(msgString[1:-1].split(","))
        if type(parent) is AttrDict:
            self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent.data.id}}))
            reply = AttrDict(json.loads(self.conn.recv()))
            print(f'Message sent: {reply} replying to: {parent.data.id} by {parent.data.sender.name}')
        elif type(parent) is string:
            self.conn.send(json.dumps({'type': 'send', 'data': {'content': msgString, 'parent': parent}}))
            reply = AttrDict(json.loads(self.conn.recv()))
            print(f'Message sent: {reply} replying to: {parent}')

        return reply

    def restart(self, msg):
        self.conn.close()
        self.connect()
        self.start()
        self.sendMsg("Restarted", msg)

    def start(self):
        try:
            while True:
                msg = AttrDict(json.loads(self.conn.recv()))
                if msg.type == 'ping-event':
                    self.handle_ping(msg)
                elif msg.type == 'send-event' and msg.data.sender.name != self.nick:
                    self.handle_message(msg)
                elif msg.type == 'error':
                    print(msg.dict)
        except Killed:
            pass

    def handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def handle_message(self, msg):
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None and "is_manager" in msg.data.sender.keys() or msg.data.sender.name == self.owner:
            self.kill()
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None and "is_manager" in msg.data.sender.keys() or msg.data.sender.name == self.owner:
            self.restart()
        if re.search('^!ping$', msg.data.content) != None:
            self.sendMsg("Pong!", msg)
        for regex, response in self.regexes.items():
            if re.search(regex, msg.data.content) != None:
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

    def setNick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise Killed

class Killed(Exception):
    pass
