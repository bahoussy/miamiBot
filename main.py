import os
import requests
import discord
from dotenv import load_dotenv 
from bs4 import BeautifulSoup
from datetime import datetime
import pymongo

load_dotenv()
TOKEN = os.getenv('TOKEN')


async def daily_log(message):
  
  client = pymongo.MongoClient("mongodb+srv://houssem:bahoussykouki38@cluster0.igw9k.mongodb.net/?retryWrites=true&w=majority")
  client.test
  print(client)
  db = client.discord_logs
  log_collection = db.log

  entry = {}
  entry['timestamp'] = datetime.now()
  entry['msg'] = message.content
  entry['user'] = message.author.name
  entry['user_id'] = message.author.id
  log_collection.insert_one(entry)
  print("logged :",entry)

client = discord.Client(intents=discord.Intents.all())
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  try:
    if message.author == client.user:
      return
    print("Message : ",message.content)
    await daily_log(message)
    if client.user.mentioned_in(message):
        await message.channel.send(file=discord.File('Miami.mp4'))


    if message.content == '!miami':
      print("Message received")
      news =''
      rsp = requests.get("https://www.local10.com")
      soup = BeautifulSoup(rsp.text, 'html.parser')
      blog_titles = soup.findAll('figure')
      for title in range(len(blog_titles[6:15])):
        news += '- '+blog_titles[title].findChildren("div")[0].findChildren("div")[0]['aria-label'] +'\n'
      response = "<@{}> **Here is what the fuck going on in miami : **".format(message.author.id)
      
      await message.channel.send(response)
      await message.channel.send(news)
  except Exception as e:
        print(e)
        await message.channel.send("<@{}> Can't fetch Miami news for you. Could be either an internal error or my code is shit. Either way go goole it yourself.".format(message.author.id))
  

client.run(TOKEN)
