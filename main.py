#token: TOKEN_API

import discord
import random

token = "TOKEN_API"
client = discord.Client()

functions = [
	"**!help** - help, dah!\n",
	"**!avatar** - so you know who redid my face.\n",
	"**!r** - let me help you roll dice by writing '***!r 1d6***' for instance!\n"
]

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
		msg_1 = "Hello {0.author.mention}.\n".format(message)
		msg_2 = f"I currently have {len(functions)} commands.\n"
		msg_3 = ""
		for item in functions:
			msg_3 += item
		await message.channel.send(msg_1+msg_2+msg_3)
	#if block to trigger the !avatar functionality
	if message.content.startswith("!avatar"):
		msg_1 = "Hello {0.author.mention}.\n".format(message)
		msg_2 = "My avatar was made by: ScarfyAce. " + \
		"Please check their reddit:\n" + \
		"https://www.reddit.com/user/ScarfyAce/"
		await message.channel.send(msg_1 + msg_2)
	# if block to trigger the !r 'i.e dice' functionality
	if message.content.startswith("!r "):
		msg = "Beep, boop! I am a stupid pony!"
		split_msg = str(message.content).split(" ")
		print("{0.author.mention} requested a die throw.".format(message))
		for bit in split_msg:
			split = bit.split("d")
			if len(split) == 2:
				if split[0].isdigit() and split[1].isdigit():
					if msg == "Beep, boop! I am a stupid pony!":
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