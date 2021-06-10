import nest_asyncio
import json
import requests
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
# from chessdotcom import get_player_stats\
from concurrent.futures import ThreadPoolExecutor
import pprint
import os
import re
import time
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime
import pytz

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
mhm_list = ["mhm", "mhhm", "mhhhm", "mmhm", "mkm", "mlm", "hmm"]

def check_time():
   IST = pytz.timezone('Asia/Kolkata')
   t = datetime.now(IST)
   current_time = t.strftime("%I:%M%p | %d, %b, %Y")
   return current_time

def int_check(amount):
   if amount - int(amount) == 0.0:
      amount = int(amount)
      return amount
   else:
      amount = f"{amount:.2f}"
      return amount

def coin_int(amount):
   if amount - int(amount) == 0.0:
      amount = int(amount)
      return amount
   else:
      return amount


@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot));
  DiscordComponents(bot)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Crypto Prices"))

@bot.event
async def on_message(message):
   message_content = message.content.lower()
   for i in mhm_list:
      if i in message_content:
         await message.channel.send(f"Testing!{message.author.mention}", delete_after=3)
   await bot.process_commands(message)

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
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "dogeinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "dogeusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
      
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/dogeinr.json",
   "https://api.wazirx.com/api/v2/tickers/dogeusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = "₹" + str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_format_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = "$" + str(crypto_values["valueusd"])
   str_remove = "[\[\'\]]"
   ticker_format_usd = re.sub(str_remove, "", ticker_format_usd)
   time_now = check_time()
   embed = discord.Embed(
   color = 	0xba9f33)
   embed.set_author(name="Dogecoin")
   embed.add_field(name= f"{ticker_format_inr}\n{ticker_format_usd}", value = f"{time_now}")
   embed.set_thumbnail(url="https://i.imgur.com/z1FHjgP.png")
   await ctx.channel.send(embed=embed)

@bot.command(name='bat', description="Give BAT Price")
async def bat(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "batinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "batusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/batinr.json",
   "https://api.wazirx.com/api/v2/tickers/batusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = "₹" + str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_format_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = "$" + str(crypto_values["valueusd"])
   str_remove = "[\[\'\]]"
   ticker_format_usd = re.sub(str_remove, "", ticker_format_usd)
   time_now = check_time()
   embed = discord.Embed(
   color = 	0xFF5000)
   embed.set_author(name="Basic Attention Token")
   embed.add_field(name= f"{ticker_format_inr}\n{ticker_format_usd}", value = f"{time_now}")
   embed.set_thumbnail(url="https://cryptologos.cc/logos/basic-attention-token-bat-logo.png")
   await ctx.channel.send(embed=embed)

@bot.command(name='ltc', description="Give LTC Price")
async def ltc(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "ltcinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "ltcusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/ltcinr.json",
   "https://api.wazirx.com/api/v2/tickers/ltcusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = "₹" + str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_format_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = "$" + str(crypto_values["valueusd"])
   str_remove = "[\[\'\]]"
   ticker_format_usd = re.sub(str_remove, "", ticker_format_usd)
   time_now = check_time()
   embed = discord.Embed(
   color = 	0x345D9D)
   embed.set_author(name="Litecoin")
   embed.add_field(name= f"{ticker_format_inr}\n{ticker_format_usd}", value = f"{time_now}")
   embed.set_thumbnail(url="https://cryptologos.cc/logos/litecoin-ltc-logo.png")
   await ctx.channel.send(embed=embed)

@bot.command(name='setmydoge', description="Set the number of doge you have")
async def setmydoge(ctx):
   message_cont = ctx.message.content
   msg_splitted = message_cont.split()
   msg_len = len(msg_splitted)
   user_id = '<@!' + str(ctx.author.id) + ">"
   print(user_id)
   print (msg_len)
   if msg_len >= 2:
      try:
         print (msg_splitted[1])
         msg_intted = float(msg_splitted[1])
      except:
         await ctx.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")
      users = doge_db.find_one({"user_id": user_id})
      time.sleep(0.4)
      print(users)
      if users != None:
         coins_set = users["amount"]
         doge_db.replace_one({"user_id": user_id}, {"user_id": user_id, "amount" : str(msg_intted)})
         await ctx.channel.send("Doge Coins Updated Successfully for " + user_id)
      elif users == None:
         new_user = {"user_id": user_id, "amount": msg_intted}
         doge_db.insert_one(new_user)
         time.sleep(0.2)
         await ctx.channel.send("Doge Coins Updated Successfully " + user_id)
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmydoge `number`")


@bot.command(name='setmybat', description="Set the number of BAT you have")
async def setmybat(ctx):
   message_cont = ctx.message.content
   msg_splitted = message_cont.split()
   msg_len = len(msg_splitted)
   user_id = '<@!' + str(ctx.author.id) + ">"
   print(user_id)
   print (msg_len)
   if msg_len >= 2:
      try:
         print (msg_splitted[1])
         msg_intted = float(msg_splitted[1])
      except:
         await ctx.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")
      users = bat_db.find_one({"user_id": user_id})
      time.sleep(0.4)
      print(users)
      if users != None:
         coins_set = users["amount"]
         bat_db.replace_one({"user_id": user_id}, {"user_id": user_id, "amount" : str(msg_intted)})
         await ctx.channel.send("BAT Updated Successfully for " + user_id)
      elif users == None:
         new_user = {"user_id": user_id, "amount": msg_intted}
         bat_db.insert_one(new_user)
         time.sleep(0.2)
         await ctx.channel.send("BAT Updated Successfully " + user_id)
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmybat `number`")

@bot.command(name='setmyltc', description="Set the number of LTC you have")
async def setmyltc(ctx):
   message_cont = ctx.message.content
   msg_splitted = message_cont.split()
   msg_len = len(msg_splitted)
   user_id = '<@!' + str(ctx.author.id) + ">"
   print(user_id)
   print (msg_len)
   if msg_len >= 2:
      try:
         print (msg_splitted[1])
         msg_intted = float(msg_splitted[1])
      except:
         await ctx.channel.send("Wrong Syntax \n Syntax: ~setmyltc `number`")
      users = ltc_db.find_one({"user_id": user_id})
      time.sleep(0.4)
      print(users)
      if users != None:
         coins_set = users["amount"]
         ltc_db.replace_one({"user_id": user_id}, {"user_id": user_id, "amount" : str(msg_intted)})
         await ctx.channel.send("LTC Updated Successfully for " + user_id)
      elif users == None:
         new_user = {"user_id": user_id, "amount": msg_intted}
         ltc_db.insert_one(new_user)
         time.sleep(0.2)
         await ctx.channel.send("LTC Updated Successfully " + user_id)
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmyltc `number`")

@bot.command(name='mydoge')
async def mydoge(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "dogeinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "dogeusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/dogeinr.json",
   "https://api.wazirx.com/api/v2/tickers/dogeusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = str(crypto_values["valueusd"])
   ticker_usd = re.sub(str_remove, "", ticker_format_usd)
   user_id = '<@!' + str(ctx.author.id) + '>'
   coins_show = doge_db.find_one({"user_id": user_id})
   if coins_show != None:
      user_doge = coins_show["amount"]
      doge_inr = float(user_doge) * float(ticker_inr)
      doge_usd = float(user_doge) * float(ticker_usd)
      embed = discord.Embed(color = 0xba9f33)
      doge_formatted = str(coin_int(float(user_doge))) + " Dogecoins \n₹" + str(int_check(doge_inr)) + "\n$" + str(int_check(doge_usd))
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url="https://i.imgur.com/z1FHjgP.png")
      embed.add_field(name=doge_formatted, value=check_time())
      await ctx.channel.send(embed=embed)
   else:
      await ctx.channel.send("You do not have a Account. Please register by `~setmydoge <no. of doge coins>`")

@bot.command(name='mybat')
async def mybat(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "batinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "batusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/batinr.json",
   "https://api.wazirx.com/api/v2/tickers/batusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = str(crypto_values["valueusd"])
   ticker_usd = re.sub(str_remove, "", ticker_format_usd)
   user_id = '<@!' + str(ctx.author.id) + '>'
   coins_show = bat_db.find_one({"user_id": user_id})
   if coins_show != None:
      user_bat = coins_show["amount"]
      bat_inr = float(user_bat) * float(ticker_inr)
      bat_usd = float(user_bat) * float(ticker_usd)
      embed = discord.Embed(color = 0xFF5000)
      doge_formatted = str(coin_int(float(user_bat))) + " BAT\n₹" + str(int_check(bat_inr)) + "\n$" + str(int_check(bat_usd))
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url="https://cryptologos.cc/logos/basic-attention-token-bat-logo.png")
      embed.add_field(name=doge_formatted, value=check_time())
      await ctx.channel.send(embed=embed)
   else:
      await ctx.channel.send("You do not have a Account. Please register by `~setmydoge <no. of doge coins>`")
@bot.command(name='myltc')
async def myltc(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "ltcinr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "ltcusdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/ltcinr.json",
   "https://api.wazirx.com/api/v2/tickers/ltcusdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = str(crypto_values["valueusd"])
   ticker_usd = re.sub(str_remove, "", ticker_format_usd)
   user_id = '<@!' + str(ctx.author.id) + '>'
   coins_show = ltc_db.find_one({"user_id": user_id})
   if coins_show != None:
      user_ltc = coins_show["amount"]
      ltc_inr = float(user_ltc) * float(ticker_inr)
      ltc_usd = float(user_ltc) * float(ticker_usd)
      embed=discord.Embed(
      color = 	0x345D9D)
      ltc_formatted = str(coin_int(float(user_ltc))) + " LTC \n₹" + str(int_check(ltc_inr)) + "\n$" + str(int_check(ltc_usd))
      embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
      embed.set_thumbnail(url="https://cryptologos.cc/logos/litecoin-ltc-logo.png")
      embed.add_field(name=ltc_formatted, value=check_time())
      await ctx.channel.send(embed=embed)
   else:
      await ctx.channel.send("You do not have a Account. Please register by `~setmyltc <no. of LTC>`")

@bot.command(name='ping')
async def ping(ctx):
      before = time.monotonic()
      message = await ctx.channel.send("Pong:ping_pong:!")
      ping = (time.monotonic() - before) * 1000
      await message.edit(content=f"Pong:ping_pong: **`{int(ping)}ms`**")

@bot.command(name='hello')
async def hello(ctx):
   await ctx.send(f"Hey {ctx.author.name}!")

@bot.command(name="testapi", description="This is testing api fetch speed")
async def testapi(ctx):
   await ctx.channel.send(f"Dont use that word <@!{ctx.author.id}>! ", delete_after=5)

@bot.command(name="testbuttons")
async def testbuttons(ctx):
   await ctx.channel.send("Context", components = [Button(style=ButtonStyle.blue, label="Test")]) #Blue button with button label of "Test"
   res = await bot.wait_for("button_click") #Wait for button to be clicked
   await res.respond(type=InteractionType.ChannelMessageWithSource, content=f'Button Clicked') #Responds to the button click by printing out a message only user can see #In our case, its "Button Clicked"

bot.run(os.environ['TOKEN'])
# apply mongodb on all code
# do graph shit
