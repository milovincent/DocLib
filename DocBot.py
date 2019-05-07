from socketBot import bot
import re

def calc(msg):
    result = 0
    try:
        if re.search(r"([a-wyzA-Z]+)", re.search("^!calc (.*)", msg['data']['content']).group(1)) == None:
            result = eval(str.replace(re.search("^!calc (.*)", msg['data']['content']).group(1), "^", "**"))
        else:
            return "nice try bub"
        return str(result)
    except:
        return "Invalid! Sorry pal."
def linker(msg):
    message = {}
    if msg['data']['sender']['name'] != 'RedditLinker':
        users = re.findall(r'(?<![a-zA-Z0-9])/?u/([a-zA-Z0-9_-]{3,20})\b', msg['data']['content'], flags=0)
        for i in users:
            message['reddit.com/u/%s' % i] = 'RedditLinker'
        reddits = re.findall(r'(?<![a-zA-Z0-9])/?r/([a-zA-Z0-9_-]{2,21})\b', msg['data']['content'], flags=0)
        for i in reddits:
            message['reddit.com/r/%s' % i] = 'RedditLinker'
    print(message)
    return message

DocBot = bot("DocBot", "xkcd")
DocBot.connect()
DocBot.regexes = {r"^!doc$": "Ey", "^!calc (.*)": calc, r'(?<![a-zA-Z0-9]{1}/)u/([a-zA-Z0-9_-]{3,20})\b': linker,r'(?<![a-zA-Z0-9]{1}/)r/([a-zA-Z0-9_-]{2,21})\b': linker}
DocBot.start()
