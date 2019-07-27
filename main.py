#!/usr/bin/env python3

# Goal: To create a discord bot, with 8ball and markov!
import discord
import json
import os
import random
import urllib.request

lines = open('/home/pi/Desktop/discordbot/8ball.txt').read().splitlines()

client = discord.Client()

#Figure out activity later
#client.user.setActivity("Testing")
#^ dosent work
#client.change_status(game=discord.Game(name="with yarn!"))
#^ neither do you

def read_token():
    with open('/home/pi/Desktop/discordbot/token.txt', 'r') as f:
        text = f.readlines()
        return text[0].strip()

def getweatherapi():
    with open('/home/pi/Desktop/discordbot/weather.txt', 'r') as f:
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
    return (temp.replace("temp=", ""))

apiweather = getweatherapi()
token = read_token()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello! :wave:')
        print('Hello ran')

    if message.content.startswith('$bye'):
        await message.channel.send('Bye! :wave:')
        print('Bye ran')

    if message.content.startswith('$ripdevil'):
        await message.channel.send('Bob Ross beats the devil out of it. Times beat: ' + str(beat_devil()))
        print('Ripdevil ran')

    if message.content.startswith('$8ball'):
        myline = random.choice(lines)
        await message.channel.send(myline)
        print('8ball ran')

    if message.content.startswith('$temp'):
        temporary = measure_temp()
        await message.channel.send(temporary)
        print(temporary)

    if message.content.startswith('$weather '):
        tobestripped = message.content
        location = tobestripped.replace('$weather ', '')
        with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=" + location + "&APPID=" + apiweather) as url:
            data = json.load(url)
            print(data)
            toprocess = data.get('main').get('temp')
            await message.channel.send(str((round((toprocess - 273.15) * 2) / 2)) + ' C')

    if message.content.startswith('$quote '):
        tobeid = str(message.raw_mentions)
        print('Accessing ' + tobeid + '\'s quote file.')
        userid = tobeid.replace('[', '').replace(']', '')
        if message.content.startswith('$quote add '):
            if len(userid) == 18:
                text = message.content.replace('$quote add ', '').replace('<@' + userid + '>', '')
                with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'a+') as f:
                    f.write(text + '\n')
                    await message.channel.send('Quote recorded for: ' + userid + ': ' + text)
            else:
                await message.channel.send('Too many @\'s!')
        else:
            if len(userid) == 18:
                try:
                    with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'r') as f:
                        quotechoice = f.read().splitlines()
                        myline = random.choice(quotechoice)
                        await message.channel.send(myline)
                except:
                    await message.channel.send('No quotes on file')
            else:
                await message.channel.send('Too many @\'s!')

    if message.content.startswith('$help'):
        await message.channel.send('Commands ($): hello, bye, 8ball [Question], ripdevil, quote [@], quote add [@] [text], weather [city]')
    
    if message.content.startswith('$contact'):
        await message.channel.send('For issues, feedback, or questions contact: Serah The Lioness#5408')
    
client.run(token)
