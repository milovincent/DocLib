from socketBot import bot

def sample(msg):
    return "this is a sample message"

sampleBot = bot("sample bot", "test")
sampleBot.regexes = {"^!test$":sample}




sampleBot.connect()
sampleBot.start()
