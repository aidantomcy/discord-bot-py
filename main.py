import discord
import requests
import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
whatami = [
  "Potato Person 🥔",
  "Chocolate Lover 💩",
  "Funky Monkey 🐒",
  "Vain Brain 🧠",
  "Cosmic Cuttlefish 🦑",
  "Groovy Gorilla 🦍",
  "Perky Penguin 🐧",
  "Swift Snail 🐌",
  "Fancy Frog 🐸",
  "Sassy Snake 🐍",
  "Lazy Lion 🦁",
  "Auspicious Alien 👽",
  "Tame Tomato 🍅",
  "Smelly Socks 🧦",
  "Elegant Elephant 🐘",
  "Dumb Dolphin 🐬",
]


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    
    return quote


@client.event
async def on_ready():
    print('Logged in')


@client.event
async def on_message(msg):
    tokens = msg.content.split()
    if msg.author == client.user:
        return

    if tokens[0] == '!hello':
        await msg.channel.send('Hello!')

    if tokens[0] == '!quote':
        quote = get_quote()
        await msg.channel.send(quote)

    if tokens[0] == '!whatami':
        await msg.channel.send(random.choice(whatami))

    if tokens[0] == '!time':
        timezone_db_key = os.getenv('TIMEZONE_DB_KEY')
        response = requests.get(f'https://api.timezonedb.com/v2.1/get-time-zone?key={timezone_db_key}&format=json&by=zone&zone=Asia/Kolkata')
        json_data = json.loads(response.text)
        await msg.channel.send(json_data['formatted'])

    if tokens[0] == '!gif':
        api_key = os.getenv('TENOR_KEY')
        keywords = 'dog'
        url = f"https://g.tenor.com/v1/search?q={keywords}&key={api_key}&contentfilter=high"
        gifs = []
        response = requests.get(url)

        if len(tokens) > 1:
            # keywords = tokens.slice(1, len(tokens)).join(" ")
            keywords = tokens[1:len(tokens)].join(" ")
        keywords = ' '.join(tokens[1:len(tokens)])
            

        if response.status_code == 200:
            data = response.json()
            for item in data['results']:
                gifs.append(item['media'][0]['gif']['url'])
            await msg.channel.send(random.choice(gifs))
        else:
            await msg.channel.send('Something went wrong')

    if tokens[0] == '!help':
        await msg.channel.send(
            """
!hello   - Say Hello
!quote   - Get a random quote
!whatami - Tell what you are
!time    - Get the current time
!gif     - Get a random gif
!help    - Show this message

More features coming soon!
            """
        )


client.run(os.getenv('BOT_TOKEN'))
