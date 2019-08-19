#!/usr/bin/env python3

import discord
import json
import os
import random
import urllib.request

balllines = open('/home/pi/Desktop/discordbot/8ball.txt').read().splitlines()



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

    elif message.content.startswith('$bye'):
        await message.channel.send('Bye! :wave:')
        print('Bye ran')

    elif message.content.startswith('$ripdevil'):
        await message.channel.send('Bob Ross beats the devil out of it. Times beat: ' + str(beat_devil()))
        print('Ripdevil ran')

    elif message.content.startswith('$8ball'):
        myline = random.choice(balllines)
        await message.channel.send(myline)
        print('8ball ran')

    elif message.content.startswith('$temp'):
        temporary = measure_temp()
        await message.channel.send(temporary)
        print(temporary)

    elif message.content.startswith('$weather '):
        tobestripped = message.content
        location = tobestripped.replace('$weather ', '')
        with urllib.request.urlopen("https://api.openweathermap.org/data/2.5/weather?q=" + location + "&APPID=" + apiweather) as url:
            data = json.load(url)
            print(data)
            toprocess = data.get('main').get('temp')
            await message.channel.send(str((round((toprocess - 273.15) * 10) / 10)) + ' C')

    elif message.content.startswith('$quote '):
        tobeid = str(message.raw_mentions)
        print('Accessing ' + tobeid + '\'s quote file.')
        userid = tobeid.replace('[', '').replace(']', '')
        if len(userid) == 18:
            if message.content.startswith('$quote add '):
                text = message.content.replace('$quote add ', '').replace('<@' + userid + '>', '')
                with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'a+') as f:
                    quotenumber = 1
                    for i in enumerate(f):
                        quotenumber += 1
                    f.write(str(quotenumber) + ': ' + text + '\n')
                    await message.channel.send('Quote recorded for: <@' + userid + '>: ' + text)
            elif message.content.startswith('$quote rm #'):
                number = int(message.content.replace('$quote rm #', '').replace('<@' + userid + '>', '').replace(' ',''))
                number -= 1
                try:
                    with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'r') as f:
                        lines = f.readlines()
                    with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'w') as f:
                        for pos, line in enumerate(lines):
                            if pos != number:
                                f.write(line)
                except:
                    try:
                        f = open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'r')
                        await message.channel.send('Error')
                    except:
                        await message.channel.send('No quotes on file')
            elif message.content.startswith('$quote #'):
                try:
                    with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'r') as f:
                        quotechoice = f.read().splitlines()
                        myline = int(message.content.replace('$quote #', '').replace('<@!' + userid + '>', '').replace(' ',''))
                        await message.channel.send(myline)
                except:
                    await message.channel.send('No quotes on file')
            else:
                try:
                    with open('/home/pi/Desktop/discordbot/' + userid + '.txt', 'r') as f:
                        quotechoice = f.read().splitlines()
                        myline = random.choice(quotechoice)
                        await message.channel.send(myline)
                except:
                    await message.channel.send('No quotes on file')
        else:
                await message.channel.send('Too many @\'s!')
    elif message.content.startswith('$help'):
        await message.channel.send('Commands ($): hello, bye, 8ball [Question], ripdevil, quote #[number] [@], quote add [@] [text], quote rm #[number] [@], weather [city]')

    elif message.content.startswith('$contact'):
        await message.channel.send('For issues, feedback, or questions contact: Serah The Lioness#5408')

    elif message.content.startswith('$version'):
        await message.channel.send('0.2.3a: Added support for quote removal(rm), and selection')

client.run(token)
