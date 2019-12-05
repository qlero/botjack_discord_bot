#import discord
from discord.ext import commands
import local_commands
import time

#################/!\#################
#to remove before uploading to github
#################/!\#################
token = "YOUR TOKEN HERE"
#################/!\#################
#################/!\#################

bot = commands.Bot(command_prefix = "!")

model = local_commands.run_model()

#List all the available commands in the dictionary below
functions = {
	"!info" : "Help, dah! If, followed by ``<function_name>``, provides you information on a specific bot function",
	"!avatar" : "So you may know who rebuilt my face.",
	"!roll" : "Let me roll dice for you by writing this command followed by ``***!roll 1d6***`` for instance. Go Fish!",
	"imgML" : "``not a callable function`` Whenever a picture (.jpg, .jpeg, or .png) is uploaded directly to discord, botjack runs a check against " + \
	"a ML-trained model to check whether or not it is Safe for Woona."
}

@bot.event
async def on_ready():
	print("Logged in as",bot.user.name,bot.user.id,"------",sep="\n")
	print("I got my gun, my beer, a fire in my belly, and a grin on my face.")

@bot.event
async def on_error(message):
	await message.channel.send("I am dying--again--beep, boop!")
	await bot.process_commands(message)

@bot.event
async def on_message(message):
	print("message detected")
	ml = ""
	# for loop checking for embeds
	for item in message.embeds:
		url = item.to_dict()["thumbnail"]["url"]
		msg = local_commands.ml_check(url, model, True)
		await message.channel.send(msg)
		
	# if block trigger for an attachment
	if message.attachments:
		msg = local_commands.ml_check(message.attachments, model, False)
		await message.channel.send(msg)
	
	await bot.process_commands(message)

@bot.command()
async def foo(ctx, arg):
	await ctx.send(arg)
	
@bot.command()
async def info(ctx, *args):
	#trigger for !info
	author = ctx.message.author.mention
	if len(args) == 0:
		await ctx.send(local_commands.main_help(functions, author))
	else:
		for arg in args:
			await ctx.send(local_commands.specific_help(functions, arg))

@bot.command()
async def avatar(ctx):
	#trigger for !avatar
	await ctx.send(local_commands.avatar(ctx.message.author.mention))

@bot.command()
async def roll(ctx, *args):
	#trigger for !roll
	msg = "Your results:\n"
	author = ctx.message.author.mention
	for arg in args:
		msg += f"``{arg}``: " + local_commands.roll(arg, author) + "\n"
	if msg != "Your results:\n": await ctx.send(msg)

bot.run(token, reconnect=True)