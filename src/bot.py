import discord
from discord.ext import commands
import random
from credentials import *
import requests
import json
import time
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
	if msg.content.startswith(bot.command_prefix + 'webhook'):
		await bot.process_commands(msg)
	if not msg.webhook_id is None or  msg.content.startswith(bot.command_prefix + 'webhook'):
		pass
	else:
		file = open('data/webhooks.json', 'r')
		json_ = json.loads(file.read())
		hook = json_[str(msg.guild.id)]
		print(hook)
		#data = {'msg':str(msg.channel) + ' : ' + msg.content,'name':msg.author,'avatar':msg.author.avatar_url_as(), 'webhook':hook}
		data = '''
		{
		"username":"<@''' + str(msg.author) + '''>",
		"avatar_url":"''' + str(msg.author.avatar_url_as()) + '''",
		"embeds":[{
		"description":"''' + '#' + str(msg.guild) + '.' + str(msg.channel) + ' > ' + str(msg.content) + '''",
		"color":1293882
				}
			]
		}
		'''
		print(data)
		r = requests.post(hook, data = data, headers = {'Content-Type':'application/json'})
		print(str(msg.author) + ' sent ' + str(msg.content))
		try:
			time.sleep(int(json.loads(r.text)['retry_after']))
		except Exception:
			pass
		file.close()
		
@bot.command()
async def webhook(ctx):
	
	if 'add' in ctx.message.content:
		file = open('data/webhooks.json', 'r')
		msg = file.read()
		if ctx.message.guild.id in json.loads(msg).keys():
			await ctx.send("Failed to add webhook. You may only link 2 servers.")
		file.close()
		file = open('data/webhooks.json', 'w')
		hook_ = ',"%s":"%s"}' % (ctx.message.guild.id, ctx.message.content.split('add ')[1])
		file.write(msg[:-1] + hook_)
		msg__ = await ctx.send("Added webhook!")
		await msg__.add_reaction('😁')
bot.run(BOT_TOKEN)