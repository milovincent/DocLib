from socketBot import bot

def sample(msg):
    return "this is a sample message"

sampleBot = bot("sample bot for AP", "xkcd")
sampleBot.regexes = {"^!ap$":sample}




sampleBot.connect()
sampleBot.start()
