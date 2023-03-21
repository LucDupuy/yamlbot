import discord
import re
import sys

TOKEN = sys.argv[1]
# key=word value=boolean should be treated as standalone
ILLEGAL_WORDS_REF = {
    'yaml': False,
    'java': False, 
    'prolog': True,
    'json': True,
    'web dev': False,
    'webdev': True,
    'dba': True, 
    'database': False,
    'db': True,
    'fossil': True, 
    'smalltalk': True,
    'aws': True, 
    'azure': True,
    'js': True
}

ILLEGAL_WORDS = ILLEGAL_WORDS_REF.keys()
CENSOR_CHAR = '\*'

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    user = message.author.name
    if message.author == client.user:
        return

    msg_to_send = message.content
    has_curse = False
    for word in ILLEGAL_WORDS:
        curse = '\\b' + word + '\\b' if ILLEGAL_WORDS_REF[word] else word
        regex_pattern = re.compile(curse, re.IGNORECASE)
        msg_to_send, num_subs = regex_pattern.subn(word[0]+CENSOR_CHAR*(len(word) - 1), msg_to_send)
        if(not has_curse and num_subs > 0):
            await message.delete()
            has_curse = True


    print(has_curse)

    if(has_curse):
        msg_to_send = f"What {user} meant to say is:  " + msg_to_send
        await message.channel.send(msg_to_send)


client.run(TOKEN)
