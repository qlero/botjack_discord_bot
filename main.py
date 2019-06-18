import discord
import random

#################/!\#################
#to remove before uploading to github
#################/!\#################
token = "API TOKEN"
#################/!\#################
#################/!\#################

client = discord.Client()

functions = {
	"!help" : "Help, dah!",
	"!avatar" : "So you may know who rebuilt my face.",
	"!roll" : "Let me roll dice for you by writing this command followed by '***!r 1d6***' for instance. Go Fish!"
}

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print("I got my gun, my beer, a fire in my belly, and a grin on my face.")

@client.event
async def on_message(message):
	#if block to stop the bot from responding to itself
	if message.author == client.user:
		return
	
	#if block to trigger the !help functionality
	if message.content.startswith("!help"):
		msg_1 = "**Available Commands**\nHello {0.author.mention}. ".format(message)
		msg_2 = f"I currently have {len(functions)} commands."
		msg_3 = ""
		msg_4 = "\nFor help with a particular command, use ``?help`` followed by the command name."
		for index, key in enumerate(functions.keys()):
			msg_3 += key + ", " if index + 1 < len(functions) else key
		await message.channel.send(msg_1+msg_2+"```"+msg_3+"```"+msg_4)
	
	#if block to trigger the ?help functionality
	if message.content.startswith("?help "):
		msg = "Beep, boop! I'm not a smart pony!"
		split_msg = str(message.content).split(" ")
		if (split_msg[1] in functions.keys()) or ("!" + split_msg[1] in functions.keys()):
			if split_msg[1] in functions.keys():
				msg = functions[split_msg[1]]
			else:
				msg = functions["!" + split_msg[1]]
		await message.channel.send(msg)
	
	#if block to trigger the !avatar functionality
	if message.content.startswith("!avatar"):
		msg_1 = "Hello {0.author.mention}.\n".format(message)
		msg_2 = "My avatar was made by: ScarfyAce. " + \
		"Please check their reddit:\n" + \
		"https://www.reddit.com/user/ScarfyAce/"
		await message.channel.send(msg_1 + msg_2)
	
	# if block to trigger the !r 'i.e dice' functionality
	if message.content.startswith("!roll "):
		msg = "Beep, boop! I'm not a smart pony!"
		split_msg = str(message.content).split(" ")
		print("{0.author.mention} requested a die throw.".format(message))
		for bit in split_msg:
			split = bit.split("d")
			if len(split) == 2:
				if split[0].isdigit() and split[1].isdigit():
					if msg == "Beep, boop! I'm not a smart pony!":
						msg = "Your results, {0.author.mention}!\n".format(message)
						msg += f"{random.randrange(0, int(split[0]) * int(split[1]) + 1)}\n"
					else:
						msg += f"{random.randrange(0, int(split[0]) * int(split[1]) + 1)}\n"
		await message.channel.send(msg)

@client.event
async def on_error(event, *args, **kwargs):
	#Gets the message object
	message = args[0]
	#logs the error
	logging.warning(traceback.format_exc())
	#send the message to the channel
	await message.channel.send("I am dying--again--beep, boop!")

client.run(token, reconnect=True)