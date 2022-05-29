import os
import requests
import discord
from dotenv import load_dotenv 
from keep_alive import keep_alive
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Timer
from replit import db

load_dotenv()
TOKEN = os.getenv('TOKEN')
x=datetime.today()
y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.seconds+1

def daily_log():
  logs =''
  rsp = requests.get("https://www.local10.com")
  soup = BeautifulSoup(rsp.text, 'html.parser')
  blog_titles = soup.findAll('figure')
  for title in range(len(blog_titles[6:15])):
    logs += '- '+blog_titles[title].findChildren("div")[0].findChildren("div")[0]['aria-label'] +'\n'
  db["{}".format(x)] = logs
  print(db.keys())
  
client = discord.Client()
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if client.user.mentioned_in(message):
        await message.channel.send(file=discord.File('Miami.mp4'))
    if message.author == client.user:
        return
    news =''
    if message.content == '!miami':
      
      rsp = requests.get("https://www.local10.com")
      soup = BeautifulSoup(rsp.text, 'html.parser')
      blog_titles = soup.findAll('figure')
      for title in range(len(blog_titles[6:15])):
        
        news += '- '+blog_titles[title].findChildren("div")[0].findChildren("div")[0]['aria-label'] +'\n'
      response = "<@{}> **Here is what the fuck going on in miami : **".format(message.author.id)
      try: 
        await message.channel.send(response)
        await message.channel.send(news)
      except Exception as e:
        print(e)
        await message.channel.send("<@{}> Can't fetch Miami news for you. Could be either an internal error or my code is shit. Either way go goole it yourself.".format(message.author.id))
keep_alive()
t = Timer(secs, daily_log)
t.start()
client.run(TOKEN)