import random

def main_help(message, functions):
	"""
	Prints the !help message to the chat.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	:param <functions>: <class 'dict'> ; dictionary of available commands for botjack
	"""
	msg = "**Available Commands**\nHello {0.author.mention}. ".format(message)
	msg += f"I currently have {len(functions)} commands.```"
	for index, key in enumerate(functions.keys()):
		msg += key + ", " if index + 1 < len(functions) else key
	msg += "```\nFor help with a particular command, use ``?help`` followed by the command name."
	return msg

def specific_help(message, functions):
	"""
	Prints the specific ?help <command> message to the chat.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	:param <functions>: <class 'dict'> ; dictionary of available commands for botjack	
	"""
	msg = "Beep, boop! I'm not a smart pony!"
	split_msg = str(message.content).split(" ")
	if (split_msg[1] in functions.keys()) or ("!" + split_msg[1] in functions.keys()):
		if split_msg[1] in functions.keys():
			msg = functions[split_msg[1]]
		else:
			msg = functions["!" + split_msg[1]]
	return msg

def avatar(message):
	"""
	Cites the creator of botjack's avatar.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	"""
	msg = "Hello {0.author.mention}.\n".format(message)
	msg += "My avatar was made by: ScarfyAce. " + \
	"Please check their reddit:\n" + \
	"https://www.reddit.com/user/ScarfyAce/"
	return msg

def roll(message):
	"""
	Rolls dice requested by a user.
	:param <message>: <class 'discord.message.Message'> ; user message triggering a bot event
	"""
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
	return msg