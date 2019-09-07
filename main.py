import discord
import commands

#################/!\#################
#to remove before uploading to github
#################/!\#################
token = "PLACE TOKEN HERE"
#################/!\#################
#################/!\#################

client = discord.Client()

model = commands.run_model()

#List all the available commands in the dictionary below
functions = {
	"!help" : "Help, dah!",
	"?help" : "?help, followed by ``<function_name>``, provides you information on a specific bot function",
	"!avatar" : "So you may know who rebuilt my face.",
	"!roll" : "Let me roll dice for you by writing this command followed by ``***!roll 1d6***`` for instance. Go Fish!",
	"imgML" : "``not a callable function`` Whenever a picture (.jpg, .jpeg, or .png) is uploaded directly to discord, botjack runs a check against " + \
	"a ML-trained model to check whether or not it is Safe for Woona."
}

@client.event
async def on_ready():
	print("Logged in as",client.user.name,client.user.id,"------",sep="\n")
	print("I got my gun, my beer, a fire in my belly, and a grin on my face.")

@client.event
async def on_message(message):
	#if block to block the bot from responding to itself
	if message.author == client.user:
		return
	
	#if block trigger for !help
	if message.content.startswith("!help"):
		await message.channel.send(commands.main_help(message, functions))
	
	#if block trigger for ?help
	if message.content.startswith("?help "):
		await message.channel.send(commands.specific_help(message, functions))
	
	#if block trigger for !avatar
	if message.content.startswith("!avatar"):
		await message.channel.send(commands.avatar(message))
	
	# if block trigger for !r 'i.e dice'
	if message.content.startswith("!roll "):
		await message.channel.send(commands.roll(message))
		
	# if block trigger for an attachment
	if message.attachments:
		msg = commands.ml_check(message.attachments, model)
		await message.channel.send(msg)

@client.event
async def on_error(message, event, *args, **kwargs):
	await message.channel.send("I am dying--again--beep, boop!")

client.run(token, reconnect=True)