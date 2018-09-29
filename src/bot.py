import discord
from discord.ext import commands
import random
from credentials import *
import requests
description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.event
async def on_message(msg):
	if not msg.webhook_id is None:
		pass
	else:
		webhook1 = 'hook1' 
		webhook2 = 'hook2'
		data = {'msg':'' + msg.content,'name':msg.author,'avatar':msg.author.avatar_url_as(), 'webhook1':webhook1, 'webhook2':webhook2}
		r = requests.post('https://multicord.000webhostapp.com/discordmessage.php', data = data)
		print(str(msg.author) + ' sent ' + str(msg.content))
		print(r.text)
		await bot.process_commands(msg)
bot.run(BOT_TOKEN)