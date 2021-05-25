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
bot = commands.Bot(command_prefix="~", case_insensitive=True)
sleep_time = 0.2
mongoclient = MongoClient(os.environ['MONGO_URL'])
mongodb = mongoclient.test
doge_db = mongodb.doge
bat_db = mongodb.bat
ltc_db = mongodb.ltc

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot));

@bot.event
async def on_message(message):
   if message.author.id != client.user.id:
      message_cont = message.content
      await message.channel.send(message_cont)

  
# @bot.command(name='chess', description="ChessBot")
# async def chess(ctx)
#    final_lst = []
#    msg = message.content
#    msg = msg.split()
#    msg_length = len(msg)
#    if msg[1] == "user":
#       username = msg[2]
#       profile = get_player_stats(username).json
#       categories = ['chess_blitz', 'chess_rapid', 'chess_bullet']
#       for category in categories:
#          category_print = str("Variation: " + category)
#          last_rating = profile['stats'][category]['last']['rating']
#          final_rating = "Latest Rating: " + str(last_rating)
#          final_send = category_print + "\n\t" + final_rating
#          final_lst.append(final_send)
#       list_format = final_lst[0] + "\n" + final_lst[1] + "\n" + final_lst[2]
#       await message.channel.send(list_format)
#    elif msg[1] == "users":
#       with open("file.txt", 'r') as f:
#          users = {'author': [], 'chess': []}
#          for line in f:
#             line_stripped = line.strip()
#             line_split = line_stripped.split()
#             users['author'].append(line_split[0])
#             users['chess'].append(line_split[2])
#          author_ids = users['author']
#          author_usrnm = users['chess']
#          f.close()
#       if msg[2] == "show":
#          if msg_length == 3:
#             user_id = '<@!' + str(message.author.id) + '>'
#             for idx, author_id in enumerate(author_ids):
#                if user_id == author_id:
#                   user_same = users['chess'][idx]
#                   await message.channel.send(user_same)
#          elif msg_length == 4:
#             for idx, author_id in enumerate(author_ids):
#                if msg[3] == author_id:
#                   user_diff = users['chess'][idx]
#                   await message.channel.send(user_diff)
#       elif msg[2] == "add":
#          chess_user = msg[3]
#          user_id = '<@!' + str(message.author.id) + '>'
#          print(user_id)
#          if user_id in author_ids:
#             for idx, author_id in enumerate(author_ids):
#                if user_id == author_id:
#                print(idx)
#                user_tobe_replaced = str(users['chess'][idx])
#                print(to_be_replaced)
#                user_replace = str(msg[3])
#                fin = open('file.txt', 'r')
#                file = fin.read()
#                file = file.replace(user_tobe_replaced, user_replace)
#                fin.close()
#                fout = open('file.txt','w')
#                fout.write(file)
#                fout.close()
#                print(user_tobe_replaced)
#                await message.channel.send("UserName Updated!")
#          elif user_id not in author_ids:
#             if chess_user not in author_usrnm:
#             with open("file.txt", 'a') as fa:
#                new = str(user_id + ' - ' +  msg[3])
#                print(new)
#                fa.write(new + '\n')
#                await message.channel.send("Added User Successfully.")
#                fa.close()
#             else:
#                await message.channel.send("Someone has Already Registered this Username")
#    else:
#       await message.channel.send("Wrong Syntax!!")

@bot.command(name='doge', description="Give DogeCoin Price")
async def doge(ctx):
   response = requests.get("https://api.wazirx.com/api/v2/tickers/dogeinr.json").json()
   ticker_buy = response['ticker']['buy']
   ticker_rounded = round(float(ticker_buy), 2)
   ticker_format = "Rs. " + str(ticker_rounded)
   await ctx.channel.send(ticker_format)

@bot.command(name='bat', description="Give BAT Price")
async def bat(ctx):
   response = requests.get("https://api.wazirx.com/api/v2/tickers/batinr.json").json()
   ticker_buy = response['ticker']['buy']
   ticker_rounded = round(float(ticker_buy), 2)
   ticker_format = "Rs. " + str(ticker_rounded)
   await ctx.channel.send(ticker_format)

@bot.command(name='ltc', description="Give LiteCoin Price")
async def ltc(ctx):
   response = requests.get("https://api.wazirx.com/api/v2/tickers/ltcinr.json").json()
   ticker_buy = response['ticker']['buy']
   ticker_rounded = round(float(ticker_buy), 2)
   ticker_format = "Rs. " + str(ticker_rounded)
   await ctx.channel.send(ticker_format)

@bot.command(name='setmydoge', description="Set the number of doge you have")
async def setmydoge(ctx):
   msg_splitted = message_cont.split()
   msg_len = len(msg_splitted)
   user_id = '<@!' + str(ctx.author.id) + '>'
   print(user_id)
   print (msg_len)
   if msg_len >= 2:
      try:
         print (msg_splitted[1])
         msg_intted = float(msg_splitted[1])
      except:
         await ctx.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")
      users = doge_db.find_one({"user_id" : user_id})
      await ctx.channel.send(users)
      if user_id in users['user_id']:
         for idx, user in enumerate(users['user_id']):
            if user_id == user:
               # doge_to_be_replaced = user + ' - ' + users['coins'][idx]
               # doge_replace =  str(user_id) + ' - ' + str(msg_intted)
               # fin = open('doge.txt', 'r')
               # file = fin.read()
               # file = file.replace(doge_to_be_replaced, doge_replace)
               # fin.close()
               # fout = open('doge.txt', 'w')
               # fout.write(file)
               # fout.close()
               #replace_one
               await ctx.channel.send("Doge coins updated for " + str(user_id))
      elif user_id not in users['user_id']:
         # with open('doge.txt', 'a') as f:
         #    f.write(str(user_id) + " - " + str(msg_intted) + "\n")
         #    f.close()
         # add_one
         await ctx.channel.send("Doge Coins Updated Successfully")
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")


#   elif message.content.startswith("~setmybat"):
#      msg = message.content
#      msg_splitted = msg.split()
#      msg_len = len(msg_splitted)
#      user_id = '<@!' + str(message.author.id) + '>'
#      print(user_id)
#      print (msg_len)
#      if msg_len >= 2:
#         try:
#            print (msg_splitted[1])
#            msg_intted = float(msg_splitted[1])
#         except:
#            await message.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")
#         with open("bat.txt", 'r') as f:
#            users = {'user_id': [], 'coins': []}
#            for line in f:
#               line_stripped = line.strip()
#               line_split = line_stripped.split()
#               print(line_split)
#               users['user_id'].append(line_split[0])
#               users['coins'].append(line_split[2])
#            f.close()
#         if user_id in users['user_id']:
#            for idx, user in enumerate(users['user_id']):
#               if user_id == user:
#                  bat_to_be_replaced = user + ' - ' + users['coins'][idx]
#                  bat_replace =  str(user_id) + ' - ' + str(msg_intted)
#                  fin = open('bat.txt', 'r')
#                  file = fin.read()
#                  file = file.replace(bat_to_be_replaced, bat_replace)
#                  fin.close()
#                  fout = open('bat.txt', 'w')
#                  fout.write(file)
#                  fout.close()
#                  await message.channel.send("BAT updated for " + str(user_id))
#         elif user_id not in users['user_id']:
#             with open('bat.txt', 'a') as f:
#                f.write(str(user_id) + " - " + str(msg_intted) + "\n")
#                f.close()
#             await message.channel.send("BAT User Account Created")
#      else:
#         await message.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")

#   elif message.content.startswith("~mydoge"):
#      response_inr = requests.get("https://api.wazirx.com/api/v2/tickers/dogeinr.json").json()
#      ticker_inr = response_inr['ticker']['buy']
#      response_usd = requests.get("https://api.wazirx.com/api/v2/tickers/dogeusdt.json").json()
#      ticker_usd = response_usd['ticker']['buy']
#      user_id = '<@!' + str(message.author.id) + '>'
#      with open("doge.txt", 'r') as f:
#           users = {'user_id': [], 'coins': []}
#           for line in f:
#               line_stripped = line.strip()
#               line_split = line_stripped.split()
#               print(line_split)
#               users['user_id'].append(line_split[0])
#               users['coins'].append(line_split[2])
#           f.close()
#      if user_id in users['user_id']:
#         for idx, user in enumerate(users['user_id']):
#             if user_id == user:
#                user_doge = users['coins'][idx]
#                doge_inr = float(user_doge) * float(ticker_inr)
#                doge_usd = float(user_doge) * float(ticker_usd)
#                doge_formatted = "You have " + str(user_doge) + " dogecoins \nIts value in **INR** is ₹ " + str(round(doge_inr, 4)) + "\nIts value in **USD** is $ " + str(round(doge_usd, 4))
#                await message.channel.send(doge_formatted)
#      else:
#         await message.channel.send("You do not have a Account. Please register by `~setmydoge <no. of doge coins>`")
#   elif message.content.startswith("~mybat"):
#      response_inr = requests.get("https://api.wazirx.com/api/v2/tickers/batinr.json").json()
#      ticker_inr = response_inr['ticker']['buy']
#      response_usd = requests.get("https://api.wazirx.com/api/v2/tickers/batusdt.json").json()
#      ticker_usd = response_usd['ticker']['buy']
#      user_id = '<@!' + str(message.author.id) + '>'
#      with open("bat.txt", 'r') as f:
#           users = {'user_id': [], 'coins': []}
#           for line in f:
#               line_stripped = line.strip()
#               line_split = line_stripped.split()
#               print(line_split)
#               users['user_id'].append(line_split[0])
#               users['coins'].append(line_split[2])
#           f.close()
#      if user_id in users['user_id']:
#         for idx, user in enumerate(users['user_id']):
#             if user_id == user:
#                user_bat = users['coins'][idx]
#                bat_inr = float(user_bat) * float(ticker_inr)
#                bat_usd = float(user_bat) * float(ticker_usd)
#                bat_formatted = ">>> You have `" + str(user_bat) + "` BAT \nIts value in **INR** is ***₹*** `" + str(round(bat_inr, 4)) + "`\nIts value in **USD** is ***$*** `" + str(round(bat_usd, 4)) + "`"

#                await message.channel.send(bat_formatted)
#      else:
#         await message.channel.send("You do not have a Account. Please register by `~setmybat <no. of BATs>`")
@bot.command(name='ping')
async def ping(ctx):
      before = time.monotonic()
      message = await ctx.channel.send("Pong:ping_pong:!")
      ping = (time.monotonic() - before) * 1000
      await message.edit(content=f"Pong:ping_pong: **`{int(ping)}ms`**")

@bot.command(name='hello')
async def hello(ctx):
   await ctx.send(f"Hey {ctx.author.name}!")

@bot.command(name='embed')
async def embed(ctx):
    embed=discord.Embed(
    title="Text Formatting",
        url="https://realdrewdata.medium.com/",
        description="Here are some ways to format text",
        color=discord.Color.green())
    embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData", icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
    #embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
    embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
    embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
    embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
    embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
    embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
    embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
    embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
    embed.set_footer(text="Learn more here: realdrewdata.medium.com")
    await ctx.send(embed=embed)


bot.run(os.environ['TOKEN'])

# apply mongodb on all code
# do graph shit
