from const import *
import discord
import asyncio
from start import log

client = discord.Client()                              												# get client
functions = {}                                          											# define the functions dict

@client.event
async def on_ready():                                   											# some logging
	log('All set and ready!')
	log('Bot logged in as', client.user.name, 'with id', client.user.id)
	log('-----')


@client.event
async def on_message(message):
	log(message.server, '/', message.channel, '/', message.author, 'wrote', message.content)
	if any([message.content.startswith(i) for i in prefixes]):
		text = message.content.lower()                      											# parse message
		content = text.split()[1:]
		await asyncio.sleep(0.2)                            										# make it feel natural
		await client.send_typing(message.channel)
		await asyncio.sleep(1)            											# more logging
		if len(content):
			if content[0] in functions.keys():
				await functions[content[0]].func(message, content[2:] if len(content) > 2 else [])  # call the function
			else:
				await client.send_message(message.channel, 'Я не понимаю, чего ты от меня хочешь!')
		else:
			await client.send_message(message.channel, 'Что?')

class Command:
	def __init__(self, name, func, syntax=None, sdesc='Not provided.', desc='No description for the command provided.'):
		if name in functions.keys():																# check for repeating 
			raise KeyError()
		self.name = name
		self.func = func
		if syntax is None:
			self.syntax = prefixes[0] + ' ' + name
		else:
			self.syntax = syntax
		self.sdesc = sdesc
		self.desc = desc
		functions[name] = self

# Functions go here
async def help(message, args):
	if len(args) == 0:
		log('Listing commands.')
		embed = discord.Embed(title='Помощь по боту', color=0x008800)
		embed.set_author(name='Minecraft Бот')
		embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9")
		for key in functions:
			embed.add_field(name='`' + functions[key].syntax + '`', value=functions[key].sdesc, inline=True)
		await client.send_message(message.channel, embed=embed)
	elif len(args) == 1 or len(args) == 2 and args[0] in prefixes:
		if len(args) == 2:
			arg = args[1]
		else:
			arg = args[0]
		log('Getting help for', arg + '.')
		if arg in functions.keys():
			function = function[arg]
			embed = discord.Embed(title='Помощь по ' + arg, color=0x008800)
			embed.set_author(name='Minecraft Бот')
			embed.set_thumbnail(url="https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9")
			embed.add_field(name='`' + function.syntax + '`', value=function.desc, inline=True)
			await client.send_message(message.channel, embed=embed)
		else:
			log('Unknown command.')
			await client.send_message(message.channel, 'Я не знаю, что такое `' + prefixes[0] + ' ' + arg + '`!')
	else:
		log('Too many arguments!')
		await client.send_message(message.channel, 'Я твоя не понимать, ты говорить коротко!')

async def restart(message, args):
	if len(args) > 0:
		await client.send_message(message.channel, 'Ты чего, совсем обалдел? Не только пытаешься меня убить, но и грузишь всем этим своим бредом?')
	else:
		if 'Lord' in [str(role) for role in message.author.roles]:
			await client.send_message(message.channel, 'Я вернусь! :thumbsup:')
			client.close()
		else:
			await client.send_message(message.channel, 'Да кто ты такой?')
# Functions end

# Strings go here
strings = {
    'desc.none':'Ну, я не знаю, она что-то делает, но что... мне не сказали. Попробуй и узнаешь! :wink:',
    'embed.author':'Minecraft Бот',
    'embed.thumbnail':'https://d1u5p3l4wpay3k.cloudfront.net/minecraft_ru_gamepedia/b/bc/Wiki.png?version=26fd08a888d0d1a33fb2808ebc8678e9',
    'func.help.overflow':'Я твоя не понимать, ты говорить коротко!',
    'func.help.title':'Помощь по боту',
    'func.help.specific.title':'Помощь по %s',
    'func.help.specific.unknown':'Я не знаю, что такое `%s %s`!',
    'func.kill.failure':'Да кто ты такой?',
    'func.kill.overflow':'Ты чего, совсем обалдел? Не только пытаешься меня убить, но и грузишь всем этим своим бредом?',
    'func.kill.success':'Я вернусь! :thumbsup:',
    'func.none':'Что?',
    'func.unknown':'Я не понимаю, чего ты от меня хочешь!',
    'sdesc.none':'Не знаю...'
}
# Strings end
# Commands go here
prefixes = ['!bot']
Command("help", help, syntax='!minecraft help [команда]', sdesc='Этот список или помощь по команде.', desc='Показывает список всех команд или подробное описание указаной команды (как то, что вы сейчас читаете).')
Command("restart", restart, syntax='!minecraft restart', sdesc='Перезапуск бота.', desc='Перезапускает бота. Доступно только `@Owner`.')
# Commands end

client.run(token)