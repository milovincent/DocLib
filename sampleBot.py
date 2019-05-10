from doclib import bot

def sample(msg):
    return "this is a sample message"

def evaluate(msg):
    try:
        return eval(re.search("^!calc (.*)$",msg['data']['content']).group(1))
    except:
        return "nice try"

sampleBot = bot("sample bot", "test")
sampleBot.regexes = {"^!test$":sample, "^!calc (.*)$":evaluate}




sampleBot.connect()
sampleBot.start()
