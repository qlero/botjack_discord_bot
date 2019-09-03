import os
import discord
import asyncio
import commands
import logging
from keras.models import load_model
from keras.preprocessing import image
import cv2
import numpy as np

#################/!\#################
#to remove before uploading to github
#################/!\#################
token = "PLACE TOKEN HERE"
#################/!\#################
#################/!\#################

client = discord.Client()

dirname, filename = os.path.split(os.path.abspath(__file__))
model = load_model(dirname + "\\model.h5")
model.compile(loss = "binary_crossentropy",
			optimizer = "rmsprop",
			metrics = ["accuracy"])
			
def load_image(img_path):
	img = cv2.imread(img_path)
	img = cv2.resize(img, (224,224))
	img = np.reshape(img, [1, 224, 224, 3])
	return img

pic_ext = [".jpg", ".png", ".jpeg"]

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
	
	try:
		print(type(message.attachments), message.attachments, list(message.attachments))
		attachment = message.attachments[0]
		print(attachment)
		for ext in pic_ext:
			if attachment.endswith(ext):
				img = load_image(attachment)
				classes = model.predict_classes(img)
				if classes[0][0] == 0:
					await message.channel.send("This image is safe.")
				else:
					await message.channel.send("This image is unsafe.")
	except IndexError:
		pass
	
@client.event
async def on_error(event, *args, **kwargs):
	#send the message to the channel
	await message.channel.send("I am dying--again--beep, boop!")

client.run(token, reconnect=True)