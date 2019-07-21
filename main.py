# Goal: To create a discord bot, with 8ball and markov!
import discord
import random
import subprocess
import os

lines = open('/home/pi/Desktop/discordbot/8ball.txt').read().splitlines()

client = discord.Client()

#Figure out activity later
#client.user.setActivity("Testing")

def read_token():
    with open('/home/pi/Desktop/discordbot/token.txt', 'r') as f:
        text = f.readlines()
        return text[0].strip()

def beat_devil():
    with open('/home/pi/Desktop/discordbot/beatCount.txt', 'r+') as f:
        text = f.read()
        devil_count = int(text)
        devil_count += 1
    with open('/home/pi/Desktop/discordbot/beatCount.txt', 'w') as f:
        f.write(str(devil_count))
        return devil_count
 
def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    return (temp.replace("temp=",""))

token = read_token()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! :wave:')
    if message.content.startswith('$bye'):
        await message.channel.send('Bye! :wave:')
    if message.content.startswith('$ripdevil'):
        await message.channel.send('Bob Ross beats the devil out of it. Times beat: ' + str(beat_devil()))
    if message.content.startswith('$8ball'):
        myline = random.choice(lines)
        await message.channel.send(myline)
    if message.content.startswith('$temp'):
        await message.channel.send(measure_temp())




client.run(token)
