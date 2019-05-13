from doclib import bot, message

def sample(chatbot, msg):
    return 'this is a sample message'

def doubleReply(chatbot, msg):
    msg2 = chatbot.sendMsg('reply 1', parent=msg)
    chatbot.sendMsg('reply 2', parent=msg2)

def restart(chatbot, msg):
    if msg.dict.data.sender.is_manager:
        chatbot.conn.close()
        chatbot.connect()
        chatbot.start()
        chatbot.sendMsg("Restarted", msg)

sampleBot = bot('sample bot', 'test')
sampleBot.regexes = {'^!test$':sample, '^!replyTwice$':doubleReply, '^!trouble$':"Which standard troubleshooting techniques did you apply?\nHow did you try to diagnose the problem?\nWhich Internet search queries produced which results?\nWhich of the proposed resolutions did you try?", "^!restart$":restart}




sampleBot.connect()
sampleBot.start()
