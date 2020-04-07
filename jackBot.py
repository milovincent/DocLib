from doclib import Bot
import re

def tumble(chatbot, msg):
    chatbot.setNick('tumbleweed')
    chatbot.sendMsg(parent = msg, msg = '/me rolls by')
    chatbot.setNick('jackBot')


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def kill(chatbot, msg):
    chatbot.sendMsg(parent = msg, msg = "/me ceases to annoy")
    chatbot.kill()

def greatScott(chatbot, msg):
    chatbot.setNick('DocBrown')
    chatbot.sendMsg(parent = msg, msg = 'Great Scott, %s' % (msg.data.sender))
    chatbot.setNick('jackBot')

def xyzzers(chatbot, msg):
    if re.search("@xyzzy", msg.data.content) == None:
        chatbot.sendMsg("Ask @Xyzzy.")

def honkkonk(chatbot, msg):
    chatbot.setNick('An Untitled Goose')
    chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
    chatbot.setNick('jackBot')

def alive(chatbot, msg):
    chatbot.sendMsg(parent = msg, msg = '/me IS ALIVE!')
    chatbot.setNick('Thunder')
    chatbot.sendMsg(parent = msg, msg = '/me crashes')
    chatbot.setNick('jackBot')

def myThing(chatbot, msg):
    chatbot.setNick('DocBrown')
    chatbot.sendMsg(parent = msg, msg = 'Hey, that\'s my thing!')
    chatbot.setNick('jackBot')

def honk(chatbot, msg):
    geese = re.findall(r'(?i)(\d*?|two|three|four|five|six|seven|eight|nine|ten)(^|\s|\b)g(oo|ee)se($|\s|\b)', msg.data.content, flags = 0)
    ordinals = ["", "nother", " Third", " Fourth", " Fifth", " Sixth", " Seventh", " Eighth", " Ninth", " Tenth"]
    numberOfGeese = 0
    gooseLevel = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9, "ten":10}
    for goose in geese:
        numberOfGeese += 1
        if goose[0] != '' and goose[0] != "1":
            if re.match(pattern = r"(\d*?)", string = goose[0]):
                numberOfGeese += int(goose[0]) - 1
            elif re.match(pattern = r"(two|three|four|five|six|seven|eight|nine|ten)", string = goose[0]):
                numberOfGeese += gooseLevel.get(goose[0], 1)
    for goose in range(0, numberOfGeese) :
        if goose < 9:
            chatbot.setNick(f'A{ordinals[goose]} Goose')
            chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
            chatbot.setNick('jackBot')
        elif numberOfGeese > 15:
            chatbot.setNick('Another Throng of Geese')
            chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
            chatbot.setNick('The Final Goose')
            chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
            chatbot.setNick('jackBot')
            break
        elif numberOfGeese == 10:
            chatbot.setNick('The Final Goose')
            chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
            chatbot.setNick('jackBot')
            break
        else:
            chatbot.setNick('The Final Few Geese')
            chatbot.sendMsg(parent = msg, msg = 'Glory to Hong Kong!')
            chatbot.setNick('jackBot')
            break

def linker(chatbot, msg):
    if msg.data.sender != 'RedditLinker':
        users = re.findall(r'(?<![a-zA-Z0-9])/?u/([a-zA-Z0-9_-]{3,20})\b', msg.data.content, flags=0)
        for i in users:
            chatbot.setNick('RedditLinker')
            chatbot.sendMsg(parent = msg, msg = 'reddit.com/u/%s' % i)
            chatbot.setNick('jackBot')
        reddits = re.findall(r'(?<![a-zA-Z0-9])/?r/([a-zA-Z0-9_-]{2,21})\b', msg.data.content, flags=0)
        for i in reddits:
            chatbot.setNick('RedditLinker')
            chatbot.sendMsg(parent = msg, msg = 'reddit.com/r/%s' % i)
            chatbot.setNick('jackBot')

def room(chatbot, msg):
    if msg.data.sender != 'Heimdall':
        message = 'You\'re in &%s! Welcome! Say hi, guys!' % (chatbot.room)
        chatbot.sendMsg(message)

def userlist(chatbot, msg):
    response = ""
    for user in chatbot.get_userlist():
        if "bot" not in user.id:
            response += user.name + "\n"
    return response

jackBot = Bot(nick = "jackBot", room = "xkcd", owner = "DoctorNumberFour")
jackBot.set_regexes({         r'(?i)([\s\S]*?)where\.?\s?am\.?\s?i': room,
                            r'(?i)this\.?\s?town\.?\s?(ain\'t|aint|isn\'t|isnt|is not)\.?\s?big\.?\s?enough\.?\s?for\.?\s?(the\.?\s?two\.?\s?of\.?\s?us|the both of us|us two|both of us)': tumble,
                            r'(?i)gigawatt': greatScott,
                            r'(?i)back\.?\s?to\.?\s?the\.?\s?future': greatScott,
                            r'(?i)great\.?\s?scott': myThing, r'(?<![a-zA-Z0-9]{1}/)u/([a-zA-Z0-9_-]{3,20})\b': linker,r'(?<![a-zA-Z0-9]{1}/)r/([a-zA-Z0-9_-]{2,21})\b': linker,
                            '^!kill @jackbot$': kill,
                            r'(?i)([\s\S]*?)where\.?\s?is(\.?\s?bot\.?\s?bot|([\s\S]*?)other\.?\s?bots)': 'BotBot is back up in &bots, courtesy of @DoctorNumberFour and @myhandsaretypingwords! If you want to use an external tool though, there\'s still yaboli (a Python library from Garmy), basebot (a Python library from Xyzzy), and DocLib (a Python library from DoctorNumberFour, used to make jackBot).\n use ![library name] for a link to the github pages of each library to get started, or go to &bots to use the almighty BotBot (reborn as DotBot) again!',
                            r'(?i)Point for user jackBot registered\.': 'Why thank you!',
                            r'(?i)^!games (=3|niekie|@=3)$': '=3 has 10 of 25 Jackbox games.',
                            r'(?i)^!games (dnf|doctornumberfour|dn4|@DoctorNumberFour)$': '@DoctorNumberFour has 25 of 30 Jackbox games.',
                            r'(?i)^!games$': 'There are 31 games total that @DoctorNumberFour has, and 10 that =3 has. There are a total of 30 Jackbox games in the party packs, with a few standalone ones.',
                            '^!players$': 'Most games require at least 3 players (though Guesspionage and Fibbage only require 2 and several only require 1) and can hold up to 8 players (though Bracketeering can hold up to 16, Bidiots and Zeeple Dome hold 6, and Bomb Corp can only hold 4).',
                            r'(?i)who([\s\S]*?)jack\.?\s?bot': 'I was made by @DoctorNumberFour using his own bot library, DocLib: https://github.com/milovincent/DocLib !',
                            r'(?i)(when|where)([\s\S]*?)jack\.?\s?bot': 'I am an eldritch abomination from a land outside of time. Do not ask me such trivial things.',
                            r'(?i)^is\.?\s?this\.?\s?real\.?\s?life\??':'Yes',
                            'how([\s\S]*?)base\.?\s?bot':xyzzers,
                            '/me spies an? @?jackBot':'/me spies you back',
                            '/me has resurrected @jackBot':alive,
                            '^!basebot$':'https://github.com/CylonicRaider/basebot',
                            '^!yaboli$':'https://github.com/Garmelon/yaboli',
                            r'(?i)^!doclib$':'https://github.com/milovincent/DocLib',
                            '^!help$':'I\'m a miscellaneous bot made by @DoctorNumberFour using his Python 3 bot library, DocLib (!doclib for a github link.) I\'m slowly being updated to give info on every jackbox game.',
                            r'(?i)(^|\s|\b)(\d*?|two|three|four|five|six|seven|eight|nine|ten)(^|\s|\b)g(oo|ee)se($|\s|\b)': honk, r'(?i)(^|\s|\b)honk($|\s|\b)': honkkonk,
                            r'^!listusers$' : userlist})
jackBot.connect()
jackBot.simple_start()
# #r'(?i)([\s\S]*?)how([\s\S]*?)win([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': "I'm not gonna tell you how to cheat! Mostly because I don't know :/",
#                             r'(?i)([\s\S]*?)how([\s\S]*?)many (?!(people|players|participants))([\s\S]*?)jackbox': 'There are 25 games total that @DoctorNumberFour has, and 10 that =3 has. Most games require at least 3 players (though Guesspionage and Fibbage only require 2 (and several only require 1! ^^)) and can hold up to 8 players, though Bracketeering can hold up to 16 and a few have lower limits. In the future, please use !games for the number of games, and !players [game] for number of players.',
#                             r'(?i)([\s\S]*?)how([\s\S]*?)many([\s\S]*?)(people|players|participants)([\s\S]*?)(?!(need|have|must))([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'Most games require at least 3 players (though Guesspionage and Fibbage only require 2 (and several only require 1! ^^)) and can hold up to 8 players, though Bracketeering can hold up to 16.',
#                             r'(?i)([\s\S]*?)how([\s\S]*?)many([\s\S]*?)(people|players|participants)([\s\S]*?)(need|have|must)([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'Most games require at least 3 players (though Guesspionage and Fibbage only require 2 (and several only require 1! ^^)).',
#                             r'(?i)([\s\S]*?)(what|\\bwat\\b|how(?!(many|join|play|win))|why|tell([\s\S]*?)about)([\s\S]*?)(?!(quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp))([\s\S]*?)jackbox([\s\S]*?)(?!(quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp))': 'Jackbox games are a series of games that someone hosts (ask @DoctorNumberFour or =3) and everybody can play, by opening a stream (probably at grv.to/jackboxkcd (Doctor\'s stream) or maybe at mixer.com/drownthewitch (=3\'s stream)) on a browser tab or somewhere else, where there is a 4-character code for the current game. Then they go to jackbox.tv in another browser tab or on their smartphone, and enter the code and a nickname there. Most games need 3 players or more.\nThere are euphoria themed games, as well as fast or slow-paced games, and trivia or drawing games as well. It\'s all lots of fun!',
#                             r'(?i)([\s\S]*?)where([\s\S]*?)(watch|stream)([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'There are three locations. Most often, @DoctorNumberFour streams at grv.to/jackboxkcd, or his youtube channel, https://www.youtube.com/c/MiloSzecket_says_the_fourth_doctor_is_the_best_one/live (yes he knows how stupid the url is), and sometimes =3 streams at mixer.com/drownthewitch.',
#                             r'(?i)([\s\S]*?)(how|where)([\s\S]*?)(join|participate)([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': ' First, start watching a stream, and to play the games, go to jackbox.tv and type in the room code when it comes up (4 capital letters).',
#                             r'(?i)([\s\S]*?)where(?!(join|participate|watch|stream|not))([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'There are three locations. Most often, @DoctorNumberFour streams at grv.to/jackboxkcd, or his youtube channel, https://www.youtube.com/c/MiloSzecket_says_the_fourth_doctor_is_the_best_one/live (yes he knows how stupid the url is), and sometimes =3 streams at mixer.com/drownthewitch. If you\'re asking what page to go to to play, that\'s jackbox.tv.',
#                             r'(?i)([\s\S]*?)when([\s\S]*?)(?!(jackbox\.?\s?(created|founded|made)|(created|founded|made)\.?\s?jackbox))([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'Ask @DoctorNumberFour or =3! Probably right now! https://mixer.com/DoctorNumberFour or grv.to/jackboxkcd (Doctor\'s stream), https://www.youtube.com/c/MiloSzecket_says_the_fourth_doctor_is_the_best_one/live (Doctor\'s youtube) or mixer.com/drownthewitch (=3\'s stream).',
#                             r'(?i)([\s\S]*?)who([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)': 'Normally it\'s either @DoctorNumberFour or =3, but I\'d ask @DoctorNumberFour first, he\'s usually more available. If it\'s Doctor #4 streaming, the stream site is probably https://mixer.com/DoctorNumberFour, but it could also be grv.to/jackboxkcd or his youtube:  https://www.youtube.com/c/MiloSzecket_says_the_fourth_doctor_is_the_best_one/live, and if it\'s =3 streaming, the site is mixer.com/drownthewitch.',
#                             r'(?i)([\s\S]*?)when([\s\S]*?)(jackbox(created|founded|made)|(created|founded|made)jackbox)': 'Jackbox was founded in 2008.',
#                             r'(?i)^!(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)\s?specifics': 'These are the games we could be playing, from most likely to least likely:  \n\nMad Verse City (3-8 players) - You and at least 2 friends (and Gene) play rap-battlin\' robots!\n\nYou Don\'t Know Jack (1-8 players) - A trivia game with a twist!\n\nPatently Stupid (3-8 players) - Create inventions to solve problems – and pit them against each other!\n\nSplit The Room (3-8 players) - Vote on hypothetical questions! The winner is whoever best – you guessed it – splits the room!\n\nBracketeering (3-16 players) - The deranged debate tournament! Place smart bets on what will win stupid arguments.\n\nCivic Doodle (3-8 players) - Compete to see who can make the best additions to a mural in your attempt to "beautify" the city.\n\nQuiplash XL/2 (3-8 players) - The laugh-a-minute battle of wits and wittiness, sometimes with Euph-flavored flair!\n\nTee K.O. (3-8 players) - Draw pictures, write slogans, then swap them around to create your own custom t-shirt warriors. You can even buy them at the end!  \n\nTrivia Murder Party (1-8 players) - Be the last to survive a serial killer\'s absurd trivia game show. But it\'s fun!  \n\nEarwax (3-8 players) - It\'s the sound effects game that\'ll have you up to your ears in laughter!  \n\nGuesspionage (2-8 players) - Guess the percentages of people that do things, based on internet surveys. And it\'s fun!  \n\nBidiots (3-6 players) - Outbid your opponents for absurd art – drawn by players themselves – and win this strangely competitive auction game! \n\nSurvive the Internet (3-8 players) - It\'s survival of the funniest as you playfully take your friends out of context across the World Wide Web.  \n\nFibbage 3 (2-8 players) - Fib your way through this all new version of the classic, which is the same, but more 70s-themed.\n\nFibbage: Enough About You (3-8 players) - Fibbage with facts about the players!\n\nFibbage 2 (3-8 players) - Lie to your friends, avoid their lies, and spot the truth.\n\nBomb Corp (1-4 players): You work in an office. With bombs. (NOTE: hard to play with any lag)\n\nZeeple Dome (1-6 players) - Fling yourself at evil aliens in order to get back home! NOTE: REALLY hard to play with any lag.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)quiplash': 'In Quiplash, you and your friends each answer two prompts, and the answers you each give are voted on by the other players! It\'s a lot of fun, and there\'s even an &xkcd themed game to play!\n3-8 players',
#                             '^!players quiplash':'Quiplash is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)(\bt(?:ee)?\.?\s?k\.?\s?o\b)': 'In Tee K. O., you and your friends draw designs, write slogans, and mix-n-match them to create t-shirts, which are then pitted against one another in a sort of battle royale! It\'s tons of fun, and you can even buy the shirts afterwards!\n3-8 players',
#                             '^!players (\bt(?:ee)?\.?\s?k\.?\s?o\b)':'Tee K.O. is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)(Trivia\.?\s?Murder\.?\s?Party|TMP)': 'This is a general trivia game, but with a unique serial killer twist! From finger removal to the Loser Wheel, much deadly fun is to be had playing Trivia Murder Party! \n1-8 players',
#                             '^!players (Trivia\.?\s?Murder\.?\s?Party|TMP)':'Trivia Murder Party is played with 1-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)earwax': 'In Earwax, one player is chosen as a "judge." That player chooses a prompt, and everyone else gets a list of sounds and chooses the two sounds that best represent the prompt. The judge does their job (choosing the best sounds) and the winner gets a point! The first to 3 points wins.\n3-8 players',
#                             '^!players earwax':'Earwax is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)guesspionage': 'Guess the percentage of people that did a thing, based on a Reddit survey conducted yearly! Everyone else guesses higher or lower. The closer you are, the more points you get.\n2-8 players',
#                             '^!players guess?pionage':'Guesspionage is played with 2-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)bidiots': 'Bidiots is a fast-paced auction game, played using art made by you! Everyone gets a paddle and some possibly terrible advice in this light-speed game!\n3-6 players',
#                             '^!players bidiots':'Bidiots is played with 2-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)fibbage/s?(?!(eay|enough about you))': 'In Fibbage, the players are given a ridiculous fact with one word or phrase missing. They must spot the truth, and provide a lie to catch others. In Enough About You mode, players do the same with questions they themselves have answered, showing how much you know about your friends!\n3-8 players',
#                             '^!players fibbage/s?(?!(eay|enough about you))':'Fibbage is played with 2-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)fibbage(eay|enough about you)': 'In Fibbage, the players are given a ridiculous fact with one word or phrase missing. They must spot the truth, and provide a lie to catch others. In Enough About You mode, players do the same with questions they themselves have answered, showing how much you know about your friends!',
#                             '^!players fibbage(eay|enough about you)':'Fibbage: Enough About You is played with 2-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)bracketeering': 'In Bracketeering, Everybody answers a strange question, like "Which vegetable should Benedict Cumberbatch play as in his next movie?" Then your answers face off in a showdown for the ages! (which you gamble on)\n3-16 players',
#                             '^!players bracketeering':'Bracketeering is played with 3-16 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)civic\.?\s?doodle': 'In Civic Doodle, the mayor of Doodle city has commissioned you (all of you) to make art to put all around the city! Take turns adding to a communal drawing, then voting on which addition is best. Maybe you\'ll even get to paint a portrait to hang in Town Hall!\n3-8 players',
#                             '^!players civic\.?\s?doodle':'Civic Doodle is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)bomb\.?\s?corp': 'In Bomb Corp, you try to beat the clock in daily office tasks such as filing and defusing bombs. NOTE: Hard to play with lag.\n1-4 players',
#                             '^!players bomb\.?\s?corp':'Bomb Corp is played with 1-4 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)zeeple\.?\s?dome':'In Zeeple Dome, you play a sadistic alien flinging humans around what is basically jackbox\'s version of Running Man. A gauntlet of co-op, fast-flinging fun! Unless you have lag.\n1-6 players',
#                             '^!players zeeple\.?\s?dome':'Zeeple Dome is played with 1-6 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)mad\.?\s?verse\.?\s?city':'In Mad Verse City, you play a robot taking part in the sickest rap battle of the century! Answer prompts for the last word of your first line, then shit yourself as you try in vain to come up with something clever to say in the second one!\n3-8 players',
#                             '^!players mad\.?\s?verse\.?\s?city':'Mad Verse City is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)split\.?\s?the\.?\s?room':'In Split the Room, you are given (and expected to create) hypothetical what-if scenarios for the other players to vote on. Hosted by Schrödinger\'s cat itself!\n3-8 players',
#                             '^!players split\.?\s?the\.?\s?room':'Split the Room is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)patently\.?\s?stupid':'In Patently Stupid, you are given a problem to solve, and must do so with nothing but a sub-par cocktail napkin, a pen, and some ingenuity! Players then vote on designs in order to fund them!\n3-8 players',
#                             '^!players patently\.?\s?stupid':'Patently Stupid is played with 3-8 people.',
#                             r'(?i)([\s\S]*?)(what|wat|how(?!(many))|why)([\s\S]*?)(y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack)':'You Don\'t Know Jack is a trivia game with a twist! It\'s like a normal trivia game, but presided over by a large streaming corporation with little-to-no backstory known as Binjpipe. Just try and figure them out!\n1-8 players',
#                             '^!players (y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack)':'You Don\'t Know Jack is played with 1-8 people.',
#                             r'(?i)([\s\S]*?)(jackbox|quiplash|bracketeering|earwax|trivia murder party|t\.?\s?m\.?\s?p|tmp|\bt(?:ee)?\.?\s?k\.?\s?o\b|civic doodle|fibbage|guesspionage|bidiots|survive the internet|bomb corp|zeeple dome|mad verse city|y\.?\s?d\.?\s?k\.?\s?j|you don\'?t know jack|patently stupid|split the room)\.?\s?a\.?\s?game': 'Yes!',
#                             r'(?i)(what|wat|how(?!(many))|why)([\s\S]*?)survive\.?\s?the\.?\s?internet': 'In Survive the Internet, you do just that by using your evil brain to twist someone\'s innocent comment about how selfie sticks are an abomination into something a genocidal maniac would say! (all in good fun of course:smile:)\n3-8 players',
#                             r'(?i)(^!help\s*@?jackBot$|(what|who|why)([\s\S]*?)jack\.?\s?bot)': 'I tell you about Jackbox games! Just ask (using jackbox in your question)! Use:\n !jackboxspecifics for a list of games,\n !games <user> to see how many jackbox games a user has,\n !players to learn about player requirements,\n and more! I\'ve added some easter eggs as well!\nMade by @DoctorNumberFour using his own bot library, DocLib: https://github.com/milovincent/DocLib.',
