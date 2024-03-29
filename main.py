import nest_asyncio
import json
import requests
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
from concurrent.futures import ThreadPoolExecutor
import pprint
import os
import re
import time
from discord.ext import commands
from datetime import datetime
import pytz
from deta import Deta

printer = pprint.PrettyPrinter()
nest_asyncio.apply()
client = discord.Client()
bot = commands.Bot(command_prefix="~", case_insensitive=True)
sleep_time = 0.2
deta = Deta(os.environ['DETA_KEY'])
db = deta.Base("discord-bot")
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

@bot.command(name='doge', description="Give Dogecoin Price")
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

@bot.command(name='ada', description="Give ADA Price")
async def ada(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "adainr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "adausdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/adainr.json",
   "https://api.wazirx.com/api/v2/tickers/adausdt.json"]
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
   color = 	0x3468D1)
   embed.set_author(name="Cardano")
   embed.add_field(name= f"{ticker_format_inr}\n{ticker_format_usd}", value = f"{time_now}")
   embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/crypto-currency-and-coin-2/256/cardano_ada-512.png")
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
      users = db.fetch({"user": user_id})
      time.sleep(0.4)
      print(users.items)
      if users.items:
         coins_set = users.items[0]["doge"]
         db.update({"user": user_id, "doge" : str(msg_intted)}, users.items[0]["key"])
         await ctx.channel.send("Doge Coins Updated Successfully for " + user_id)
      elif not users.items:
         new_user = {"user": user_id, "doge": msg_intted, "bat": 0, "ltc": 0, "ada": 0}
         db.put(new_user)
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
      users = db.fetch({"user": user_id})
      time.sleep(0.4)
      print(users.items)
      if users.items:
         coins_set = users.items[0]["bat"]
         db.update({"user": user_id, "bat" : str(msg_intted)}, users.items[0]["key"])
         await ctx.channel.send("BAT Updated Successfully for " + user_id)
      elif not users.items:
         new_user = {"user": user_id, "doge": 0, "bat": msg_intted, "ltc": 0, "ada": 0}
         db.put(new_user)
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
      users = db.fetch({"user": user_id})
      time.sleep(0.4)
      print(users.items)
      if users.items:
         coins_set = users.items[0]["ltc"]
         db.update({"user": user_id, "ltc" : str(msg_intted)}, users.items[0]["key"])
         await ctx.channel.send("LTC Updated Successfully for " + user_id)
      elif not users.items:
         new_user = {"user": user_id, "doge": 0, "bat": 0, "ltc": msg_intted, "ada": 0}
         db.put(new_user)
         time.sleep(0.2)
         await ctx.channel.send("LTC Updated Successfully " + user_id)
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmyltc `number`")

@bot.command(name='setmyada', description="Set the number of ADA you have")
async def setmyada(ctx):
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
         await ctx.channel.send("Wrong Syntax \n Syntax: ~setmyada `number`")
      users = db.fetch({"user": user_id})
      time.sleep(0.4)
      print(users.items)
      if users.items:
         coins_set = users.items[0]["ada"]
         db.update({"user": user_id, "ada" : str(msg_intted)}, users.items[0]["key"])
         await ctx.channel.send("ADA Updated Successfully for " + user_id)
      elif not users.items:
         new_user = {"user": user_id, "doge": 0, "bat": 0, "ltc": 0, "ada": msg_intted}
         db.put(new_user)
         time.sleep(0.2)
         await ctx.channel.send("ADA Updated Successfully " + user_id)
   else:
      await ctx.channel.send("Wrong Syntax \n Syntax: ~setmyada `number`")

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
   coins_show = db.fetch({"user": user_id})
   print(coins_show.items)
   if coins_show.items:
      if coins_show.items[0]["doge"] != 0:
         user_doge = coins_show.items[0]["doge"]
         doge_inr = float(user_doge) * float(ticker_inr)
         doge_usd = float(user_doge) * float(ticker_usd)
         embed = discord.Embed(color = 0xba9f33)
         doge_formatted = str(coin_int(float(user_doge))) + " Dogecoins \n₹" + str(int_check(doge_inr)) + "\n$" + str(int_check(doge_usd))
         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
         embed.set_thumbnail(url="https://i.imgur.com/z1FHjgP.png")
         embed.add_field(name=doge_formatted, value=check_time())
         await ctx.channel.send(embed=embed)
      elif int_check(coins_show.items[0]["doge"]) == 0:
         embed = discord.Embed(color = 0xba9f33)
         embed.set_author(name=bot.display_name, icon_url=bot.avatar_url)
         await ctx.channel.send(embed=embed)
         await ctx.channel.send("You have `0` Doge. Use `~setmydoge` to update your Doge")
   elif not coins_show.items:
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
   coins_show = db.fetch({"user": user_id})
   if coins_show.items:
      if coins_show.items[0]["bat"] != 0:
         user_bat = coins_show.items[0]["bat"]
         bat_inr = float(user_bat) * float(ticker_inr)
         bat_usd = float(user_bat) * float(ticker_usd)
         embed = discord.Embed(color = 0xFF5000)
         doge_formatted = str(coin_int(float(user_bat))) + " BAT\n₹" + str(int_check(bat_inr)) + "\n$" + str(int_check(bat_usd))
         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
         embed.set_thumbnail(url="https://cryptologos.cc/logos/basic-attention-token-bat-logo.png")
         embed.add_field(name=doge_formatted, value=check_time())
         await ctx.channel.send(embed=embed)
      elif coins_show.items[0]["bat"] == 0:
         await ctx.channel.send("You have `0` BAT. Use `~setmybat` to update your BAT")
   elif not coins_show.items:
      await ctx.channel.send("You do not have a Account. Please register by `~setmybat <no. of BAT coins>`")

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
   coins_show = db.fetch({"user": user_id})
   if coins_show.items:
      if coins_show.items[0]["ltc"] != 0:
         user_ltc = coins_show.items[0]["ltc"]
         ltc_inr = float(user_ltc) * float(ticker_inr)
         ltc_usd = float(user_ltc) * float(ticker_usd)
         embed=discord.Embed(
         color = 	0x345D9D)
         ltc_formatted = str(coin_int(float(user_ltc))) + " LTC \n₹" + str(int_check(ltc_inr)) + "\n$" + str(int_check(ltc_usd))
         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
         embed.set_thumbnail(url="https://cryptologos.cc/logos/litecoin-ltc-logo.png")
         embed.add_field(name=ltc_formatted, value=check_time())
         await ctx.channel.send(embed=embed)
      elif coins_show.items[0]["ltc"] == 0:
         await ctx.channel.send("You have `0` LTC. Use `~setmyltc` to update your LTC")
   elif not coins_show.items:
      await ctx.channel.send("You do not have a Account. Please register by `~setmyltc <no. of LTC>`")

@bot.command(name='myada')
async def myada(ctx):
   def jsonconvert(link):
      response = requests.get(link).json()
      ticker_buy = response['ticker']['buy']
      ticker_rounded = round(float(ticker_buy), 2)
      ticker_rounded = int_check(ticker_rounded)
      link_split = link.split("/")
      if link_split[-1] == "adainr.json":
         crypto_values["valueinr"].append(ticker_rounded)
      elif link_split[-1] == "adausdt.json":
         crypto_values["valueusd"].append(ticker_rounded)
   
   crypto_values = {"valueinr": [], "valueusd": []}
   inputs = ["https://api.wazirx.com/api/v2/tickers/adainr.json",
   "https://api.wazirx.com/api/v2/tickers/adausdt.json"]
   with ThreadPoolExecutor(2) as thread_pool:
      results = thread_pool.map(jsonconvert, inputs)
   ticker_format_inr = str(crypto_values["valueinr"])
   str_remove = "[\[\'\]]"
   ticker_inr = re.sub(str_remove, "", ticker_format_inr)
   ticker_format_usd = str(crypto_values["valueusd"])
   ticker_usd = re.sub(str_remove, "", ticker_format_usd)
   user_id = '<@!' + str(ctx.author.id) + '>'
   coins_show = db.fetch({"user": user_id})
   if coins_show.items:
      if coins_show.items[0]["ada"] != 0:
         user_ada = coins_show.items[0]["ada"]
         ada_inr = float(user_ada) * float(ticker_inr)
         ada_usd = float(user_ada) * float(ticker_usd)
         embed=discord.Embed(
         color = 	0x3468D1)
         ada_formatted = str(coin_int(float(user_ada))) + " ADA \n₹" + str(int_check(ada_inr)) + "\n$" + str(int_check(ada_usd))
         embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
         embed.set_thumbnail(url="https://cdn4.iconfinder.com/data/icons/crypto-currency-and-coin-2/256/cardano_ada-512.png")
         embed.add_field(name=ada_formatted, value=check_time())
         await ctx.channel.send(embed=embed)
      elif coins_show.items[0]["ada"] == 0:
         await ctx.channel.send("You have `0` ADA. Use `~setmyada` to update your ADA")
   elif not coins_show.items:
      await ctx.channel.send("You do not have a Account. Please register by `~setmyada <no. of ADA>`")

@bot.command(name='portfolio')
async def portfolio(ctx):
   message_cont = ctx.message.content
   msg_splitted = message_cont.split()
   msg_len = len(msg_splitted)
   user_id = '<@!' + str(ctx.author.id) + ">"
   print(user_id)
   values = db.fetch({"user": user_id})
   print(values.items)
   if values.items:
      doge, bat, ltc, ada = values.items[0]["doge"], values.items[0]["bat"], values.items[0]["ltc"], values.items[0]["ada"]
      # if doge == 0 and bat == 0 and ltc == 0 and ada == 0:
      #    # You dont have a Account. Add atleast one currency with ~setmy`coin`
      print(f"{doge} {bat} {ltc} {ada}")
      #omit 0s
      #call api values
      #add all
      #embed
      #send
   elif not values.items:
      # You dont have a Account. Add atleast one currency with ~setmy`coin`
      pass


@bot.command(name='ping')
async def ping(ctx):
      before = time.monotonic()
      message = await ctx.channel.send("Pong:ping_pong:!")
      ping = (time.monotonic() - before) * 1000
      await message.edit(content=f"Pong:ping_pong: **`{int(ping)}ms`**")

@bot.command(name='hello')
async def hello(ctx):
   await ctx.send(f"Hey {ctx.author.name}!")

@bot.command(name="testbuttons")
async def testbuttons(ctx):
   await ctx.channel.send("Context", components = [Button(style=ButtonStyle.blue, label="Test")]) #Blue button with button label of "Test"
   res = await bot.wait_for("button_click") #Wait for button to be clicked
   await res.respond(type=InteractionType.ChannelMessageWithSource, content=f'Button Clicked') #Responds to the button click by printing out a message only user can see #In our case, its "Button Clicked"

bot.run(os.environ['TOKEN'])


#take all values
#omit 0s
#call api values
#add all
#embed
#send
