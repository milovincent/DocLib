import websockets
import websocket
import json
import re
import random
import argparse
from attrdict import AttrDict
from getpass import getpass




class Bot:
    def __init__(self, nick, room = "bots", owner = "", password = "", help = None, ping = None):
        parser = argparse.ArgumentParser(description=f'{nick}: A euphoria.io bot.')
        parser.add_argument("--test", "--debug", "-t", help = "Used to debug dev builds. Sends bot to &test instead of its default room.", action = 'store_true')
        parser.add_argument("--room", "-r", help = f"Set the room the bot will be placed in. Default: {room}", action = "store", default = room)
        parser.add_argument("--password", "-p", help = "Set the password for the room the bot will be placed in.", action = "store", default = password)

        args = parser.parse_args()

        self.nick = nick
        self.room = args.room if args.test != True else "test"
        print("Debug: " + str(args.test))
        self.normname = re.sub(r"\s+", "", self.nick)
        self.owner = owner
        self.password = args.password
        self.handlers = {}
        self.help = help
        self.ping = ping


    def connect(self):
        self.conn = websocket.create_connection(f'wss://euphoria.io/room/{self.room}/ws')
        reply = AttrDict(json.loads(self.conn.recv()))
        reply = AttrDict(json.loads(self.conn.recv()))
        self.handle_ping(reply)
        reply = AttrDict(json.loads(self.conn.recv()))
        if reply.type == "snapshot-event":
            self.setNick(self.nick)
        elif reply.type == "bounce-event":
            self.handle_auth(self.password)
            self.setNick(self.nick)
        else:
            print(reply)
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

    def restart(self, msg = None):
        self.conn.close()
        self.connect()
        self.start()
        self.sendMsg("Restarted", msg)

    def simple_start(self):
        try:
            while True:
                msg = AttrDict(json.loads(self.conn.recv()))
                if msg.type == 'ping-event':
                    self.handle_ping(msg)
                elif msg.type == 'send-event' and msg.data.sender.name != self.nick:
                    self.handle_message(msg)
                elif msg.type == 'error':
                    print(msg.dict)
                elif msg.type == 'bounce-event':
                    self.handle_auth(msg)
                else:
                    self.handle_other(msg)
        except Killed:
            pass

    def nothing(msg):
        return

    def set_regexes(self, regexes):
        self.regexes = regexes
        if self.help == None:
            if f"^!help @{self.normname}$" in regexes.keys():
                self.help = regexes[f"^!help @{self.normname}$"]
            else:
                self.help = f"@{self.normname} is a bot made with Doctor Number Four's Python 3 bot library, DocLib (link: https://github.com/milovincent/DocLib) by @{self.owner}.\nIt follows botrulez and does not have a custom !help message yet."
        if self.ping == None:
            if '^!ping$' in regexes.keys():
                self.ping = regexes['^!ping$']
            elif f'^!ping @{self.normname}$' in regexes.keys():
                self.ping = regexes[f'^!ping @{self.normname}$']
            else:
                self.ping = "Pong!"

    def advanced_start(self, function = nothing):
        if callable(function):
            try:
                while True:
                    msg = AttrDict(json.loads(self.conn.recv()))
                    if msg.type == 'send-event' and msg.data.sender.name != self.nick:
                        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None and is_privileged(msg.data.sender):
                            self.kill()
                        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None and is_privileged(msg.data.sender):
                            self.restart()
                    if msg.type in self.handlers.keys():
                        self.handlers[msg.type](msg)
                    else:
                        self.function(msg)
            except Killed:
                pass
        else:
            print("Advanced start must be given a callable message handler function that takes an AttrDict as its argument.")

    def handle_ping(self, msg):
        self.conn.send(json.dumps({'type': 'ping-reply', 'data': {'time': msg.data.time}}))

    def handle_message(self, msg):
        if re.search(f'^!kill @{self.normname}$', msg.data.content) != None and is_privileged(msg.data.sender):
            self.kill()
        if re.search(f'^!restart @{self.normname}$', msg.data.content) != None and is_privileged(msg.data.sender):
            self.restart()
        if re.search('^!ping$', msg.data.content) != None or re.search(f'^!ping @{self.normnaem}$', msg.data.content) != None:
            self.sendMsg(self.ping, msg)
        if re.search(f'^!help @{self.normname}$', msg.data.content):
            self.sendMsg(self.help, msg)
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

    def handle_auth(self, pw):
        self.conn.send(json.dumps({'type': 'auth', 'data': {'type': 'passcode', 'passcode': pw}}))
        reply = AttrDict(json.loads(self.conn.recv()))
        if reply.data.success == True:
            print(f'Successfully logged into {self.room}.')
        else:
            print(f'Login unsuccessful. Reason: {reply.data.reason}')
            self.handle_auth(getpass("Enter the correct password: "))

    def handle_other(self, msg):
        if msg.type in self.handlers.keys():
            self.handlers[msg.type](msg)


    def setNick(self, nick):
        self.conn.send(json.dumps({'type': 'nick', 'data': {'name': nick}}))

    def kill(self):
        self.conn.close()
        raise Killed

    def is_privileged(user):
        return "is_manager" in user.keys() or user.name == self.owner

    def get_userlist(self):
        self.conn.send(json.dumps({'type': 'who', 'data': {}}))
        reply = AttrDict(json.loads(self.conn.recv()))
        while reply.type != "who-reply":
            reply = AttrDict(json.loads(self.conn.recv()))
        return reply.data.listing

    def move_to(self, roomName, password = ""):
        self.room = roomName
        self.password = password
        self.restart()

    def set_handler(self, eventString, function):
        if callable(function):
            self.handlers += {eventString : function}
        else:
            print(f"WARNING: handler for {eventString} not callable, handler not set.")

class Killed(Exception):
    pass
