import discord
import commands

#################/!\#################
#to remove before uploading to github
#################/!\#################
token = "API_TOKEN"
#################/!\#################
#################/!\#################

client = discord.Client()

#List all the available commands in the dictionary below
functions = {
	"!help" : "Help, dah!",
	"!avatar" : "So you may know who rebuilt my face.",
	"!roll" : "Let me roll dice for you by writing this command followed by '***!roll 1d6***' for instance. Go Fish!"
}

@client.event
async def on_ready():
	print("Logged in as",client.user.name,client.user.id,"------",sep="\n")
	print("I got my gun, my beer, a fire in my belly, and a grin on my face.")

@client.event
async def on_message(message):
	#if block to stop the bot from responding to itself
	if message.author == client.user:
		return
	
	#if block to trigger the !help functionality
	if message.content.startswith("!help"):
		await message.channel.send(commands.main_help(message, functions))
	
	#if block to trigger the ?help functionality
	if message.content.startswith("?help "):
		await message.channel.send(commands.specific_help(message, functions))
	
	#if block to trigger the !avatar functionality
	if message.content.startswith("!avatar"):
		await message.channel.send(commands.avatar(message))
	
	# if block to trigger the !r 'i.e dice' functionality
	if message.content.startswith("!roll "):
		await message.channel.send(commands.roll(message))

@client.event
async def on_error(event, *args, **kwargs):
	#Gets the message object
	message = args[0]
	#logs the error
	logging.warning(traceback.format_exc())
	#send the message to the channel
	await message.channel.send("I am dying--again--beep, boop!")

client.run(token, reconnect=True)