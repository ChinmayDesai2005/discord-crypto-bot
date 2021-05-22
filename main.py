import nest_asyncio 
import json
import requests
import discord
from chessdotcom import get_player_stats
import pprint
import os
import time
from discord.ext import commands
from pymongo import MongoClient
from deta import Deta

printer = pprint.PrettyPrinter()
nest_asyncio.apply()
client = discord.Client()
sleep_time = 0.2

deta = Deta(os.environ['DETA_KEY'])
deta_db = deta.Base("main")
deta_db.insert({
    "name": "Geordi",
    "title": "Chief Engineer"
})
geordi = next(deta_db.fetch({"name": "Geordi"}))[0]
print(geordi['title'])
deta_db.delete(geordi['key'])
time.sleep(sleep_time)
try:
        temp = next(deta_db.fetch({"name": "Geordi"}))[0]
        print(temp)
except:
        print("none")

mongoclient = MongoClient(os.environ['MONGO_URL'])
mongodb = mongoclient.test
collection = mongodb.main
post = {"author": "Mike",             # json format, dictionary
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"]}
collection.insert_one(post).inserted_id
mike = collection.find_one({"author": "Mike"})
print(mike["text"])
collection.delete_one(mike)
time.sleep(sleep_time)
temp = collection.find_one({"author": "Mike"})
print(temp)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client));

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('&chess'):
    final_lst = []
    msg = message.content
    msg = msg.split()
    msg_length = len(msg)
    if msg[1] == "user":
      username = msg[2]
      profile = get_player_stats(username).json
      categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
      for category in categories:
         category_print = str("Variation: " + category)
         last_rating = profile['stats'][category]['last']['rating']
         final_rating = "Latest Rating: " + str(last_rating)
         final_send = category_print + "\n\t" + final_rating
         final_lst.append(final_send)
      list_format = final_lst[0] + "\n" + final_lst[1] + "\n" + final_lst[2]
      await message.channel.send(list_format)
    elif msg[1] == "users":
       with open("file.txt", 'r') as f:
           users = {'author': [], 'chess': []}
           for line in f:
              line_stripped = line.strip()
              line_split = line_stripped.split()
              users['author'].append(line_split[0])
              users['chess'].append(line_split[2])
           author_ids = users['author']
           author_usrnm = users['chess']
           f.close()
       if msg[2] == "show":
         if msg_length == 3:
           user_id = '<@!' + str(message.author.id) + '>'
           for idx, author_id in enumerate(author_ids):
              if user_id == author_id:
                user_same = users['chess'][idx]
                await message.channel.send(user_same)
         elif msg_length == 4:
             for idx, author_id in enumerate(author_ids):
                if msg[3] == author_id:
                  user_diff = users['chess'][idx]
                  await message.channel.send(user_diff)
       elif msg[2] == "add":
         chess_user = msg[3]
         user_id = '<@!' + str(message.author.id) + '>'
         print(user_id)
         if user_id in author_ids:
           for idx, author_id in enumerate(author_ids):
              if user_id == author_id:
                 print(idx)
                 user_tobe_replaced = str(users['chess'][idx])
                 print(to_be_replaced)
                 user_replace = str(msg[3])
                 fin = open('file.txt', 'r')
                 file = fin.read()
                 file = file.replace(user_tobe_replaced, user_replace)
                 fin.close()
                 fout = open('file.txt','w')
                 fout.write(file)
                 fout.close()
                 print(user_tobe_replaced)
                 await message.channel.send("UserName Updated!")
         elif user_id not in author_ids:
            if chess_user not in author_usrnm:
              with open("file.txt", 'a') as fa:
                new = str(user_id + ' - ' +  msg[3])
                print(new)
                fa.write(new + '\n')
                await message.channel.send("Added User Successfully.")
                fa.close()
            else:
               await message.channel.send("Someone has Already Registered this Username")
    else:
      await message.channel.send("Wrong Syntax!!")
  elif message.content.startswith("~doge"):
     response = requests.get("https://api.wazirx.com/api/v2/tickers/dogeinr.json").json()
     ticker_buy = response['ticker']['buy']
     ticker_rounded = round(float(ticker_buy), 2)
     ticker_format = "Rs. " + str(ticker_rounded)
     await message.channel.send(ticker_format)
  elif message.content.startswith("~bat"):
     response = requests.get("https://api.wazirx.com/api/v2/tickers/batinr.json").json()
     ticker_buy = response['ticker']['buy']
     ticker_rounded = round(float(ticker_buy), 2)
     ticker_format = "Rs. " + str(ticker_rounded)
     await message.channel.send(ticker_format)
  elif message.content.startswith("~ltc"):
     response = requests.get("https://api.wazirx.com/api/v2/tickers/ltcinr.json").json()
     ticker_buy = response['ticker']['buy']
     ticker_rounded = round(float(ticker_buy), 2)
     ticker_format = "Rs. " + str(ticker_rounded)
     await message.channel.send(ticker_format)
  elif message.content.startswith("~setmydoge"):
     msg = message.content
     msg_splitted = msg.split()
     msg_len = len(msg_splitted)
     user_id = '<@!' + str(message.author.id) + '>'
     print(user_id)
     print (msg_len)
     if msg_len >= 2:
        try:
           print (msg_splitted[1])
           msg_intted = float(msg_splitted[1])
        except:
           await message.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")
        with open("doge.txt", 'r') as f:
           users = {'user_id': [], 'coins': []}
           for line in f:
              line_stripped = line.strip()
              line_split = line_stripped.split()
              print(line_split)
              users['user_id'].append(line_split[0])
              users['coins'].append(line_split[2])
           f.close()
        if user_id in users['user_id']:
           for idx, user in enumerate(users['user_id']):
              if user_id == user:
                 doge_to_be_replaced = user + ' - ' + users['coins'][idx]
                 doge_replace =  str(user_id) + ' - ' + str(msg_intted)
                 fin = open('doge.txt', 'r')
                 file = fin.read()
                 file = file.replace(doge_to_be_replaced, doge_replace)
                 fin.close()
                 fout = open('doge.txt', 'w')
                 fout.write(file)
                 fout.close()
                 await message.channel.send("Doge coins updated for " + str(user_id))
        elif user_id not in users['user_id']:
            with open('doge.txt', 'a') as f:
               f.write(str(user_id) + " - " + str(msg_intted) + "\n")
               f.close()
            await message.channel.send("Doge Coins Updated Successfully")
     else:
        await message.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")
  elif message.content.startswith("~setmybat"):
     msg = message.content
     msg_splitted = msg.split()
     msg_len = len(msg_splitted)
     user_id = '<@!' + str(message.author.id) + '>'
     print(user_id)
     print (msg_len)
     if msg_len >= 2:
        try:
           print (msg_splitted[1])
           msg_intted = float(msg_splitted[1])
        except:
           await message.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")
        with open("bat.txt", 'r') as f:
           users = {'user_id': [], 'coins': []}
           for line in f:
              line_stripped = line.strip()
              line_split = line_stripped.split()
              print(line_split)
              users['user_id'].append(line_split[0])
              users['coins'].append(line_split[2])
           f.close()
        if user_id in users['user_id']:
           for idx, user in enumerate(users['user_id']):
              if user_id == user:
                 bat_to_be_replaced = user + ' - ' + users['coins'][idx]
                 bat_replace =  str(user_id) + ' - ' + str(msg_intted)
                 fin = open('bat.txt', 'r')
                 file = fin.read()
                 file = file.replace(bat_to_be_replaced, bat_replace)
                 fin.close()
                 fout = open('bat.txt', 'w')
                 fout.write(file)
                 fout.close()
                 await message.channel.send("BAT updated for " + str(user_id))
        elif user_id not in users['user_id']:
            with open('bat.txt', 'a') as f:
               f.write(str(user_id) + " - " + str(msg_intted) + "\n")
               f.close()
            await message.channel.send("BAT User Account Created")
     else:
        await message.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")

  elif message.content.startswith("~mydoge"):
     response_inr = requests.get("https://api.wazirx.com/api/v2/tickers/dogeinr.json").json()
     ticker_inr = response_inr['ticker']['buy']
     response_usd = requests.get("https://api.wazirx.com/api/v2/tickers/dogeusdt.json").json()
     ticker_usd = response_usd['ticker']['buy']
     user_id = '<@!' + str(message.author.id) + '>'
     with open("doge.txt", 'r') as f:
          users = {'user_id': [], 'coins': []}
          for line in f:
              line_stripped = line.strip()
              line_split = line_stripped.split()
              print(line_split)
              users['user_id'].append(line_split[0])
              users['coins'].append(line_split[2])
          f.close()
     if user_id in users['user_id']:
        for idx, user in enumerate(users['user_id']):
            if user_id == user:
               user_doge = users['coins'][idx]
               doge_inr = float(user_doge) * float(ticker_inr)
               doge_usd = float(user_doge) * float(ticker_usd)
               doge_formatted = "You have " + str(user_doge) + " dogecoins \nIts value in **INR** is ₹ " + str(round(doge_inr, 4)) + "\nIts value in **USD** is $ " + str(round(doge_usd, 4))
               await message.channel.send(doge_formatted)
     else:
        await message.channel.send("You do not have a Account. Please register by `~setmydoge <no. of doge coins>`")
  elif message.content.startswith("~mybat"):
     response_inr = requests.get("https://api.wazirx.com/api/v2/tickers/batinr.json").json()
     ticker_inr = response_inr['ticker']['buy']
     response_usd = requests.get("https://api.wazirx.com/api/v2/tickers/batusdt.json").json()
     ticker_usd = response_usd['ticker']['buy']
     user_id = '<@!' + str(message.author.id) + '>'
     with open("bat.txt", 'r') as f:
          users = {'user_id': [], 'coins': []}
          for line in f:
              line_stripped = line.strip()
              line_split = line_stripped.split()
              print(line_split)
              users['user_id'].append(line_split[0])
              users['coins'].append(line_split[2])
          f.close()
     if user_id in users['user_id']:
        for idx, user in enumerate(users['user_id']):
            if user_id == user:
               user_bat = users['coins'][idx]
               bat_inr = float(user_bat) * float(ticker_inr)
               bat_usd = float(user_bat) * float(ticker_usd)
               bat_formatted = ">>> You have `" + str(user_bat) + "` BAT \nIts value in **INR** is ***₹*** `" + str(round(bat_inr, 4)) + "`\nIts value in **USD** is ***$*** `" + str(round(bat_usd, 4)) + "`"

               await message.channel.send(bat_formatted)
     else:
        await message.channel.send("You do not have a Account. Please register by `~setmybat <no. of BATs>`")
  if message.content.startswith("&ping"):
        before = time.monotonic()
        message = await message.channel.send("Pong:ping_pong:!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong:ping_pong: **`{int(ping)}ms`**")



client.run(os.environ['TOKEN'])

# apply mongodb on all code
# use ctx
# do graph shit
