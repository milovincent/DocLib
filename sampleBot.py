from doclib import Bot

def sample(chatbot, msg):
    return 'this is a sample message'

def doubleReply(chatbot, msg):
    msg2 = chatbot.sendMsg('reply 1', parent=msg)
    chatbot.sendMsg('reply 2', parent=msg2)


sampleBot = Bot(nick = 'bugBot', room = 'test', owner = "sample user", help = "a sample bot included in Doctor Number Four's DocLib. Responds to:\n!test\n!replyTwice\n!trouble")
sampleBot.set_regexes({'^!test$':sample, '^!replyTwice$':doubleReply, '^!trouble$':"Which standard troubleshooting techniques did you apply?\nHow did you try to diagnose the problem?\nWhich Internet search queries produced which results?\nWhich of the proposed resolutions did you try?"})




sampleBot.connect()
sampleBot.simple_start()
