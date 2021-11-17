# https://docs.pycord.dev/en/master/api.html

# cogs example https://github.com/Skullbite/owopup-v3

# pycord installation!!
# win: py -m pip install -U git+https://github.com/Pycord-Development/pycord
# lin: pip install -U git+https://github.com/Pycord-Development/pycord

import discord
import random
import datetime

import json
config = json.loads(open("./config.json", "r").read())
emojis = json.loads(open("./emojis.json", "r").read())

from textwrap import dedent
def strip_indents(text): return dedent(text).strip()

import os
from dotenv import load_dotenv
load_dotenv()

# the bot
bot = discord.Bot(debug_guild=516701797411323915,
   activity = discord.Activity(
      name = "berry berry berry 🍓",
      type = discord.ActivityType.watching
   ),
   status = discord.Status.idle
)





# /help
@bot.slash_command(name="help", description="help with berry bot 🍓")
async def help(ctx):
   def name(command): return f"/{command.name}"
   commands = "`\n`".join(list(map(name, bot.commands)))
   
   developer = await bot.fetch_user(config["developer"])

   embed = discord.Embed(
      colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
      description = strip_indents(f"""
         {bot.user.mention} : **[Gentle Berry's Server]({config['invite']} "{config['invite']} 🔗")**

         **commands** {emojis['yellow_book']}
         `{commands}`

         `developer` › {developer.mention}
         `github` › [link]({config['github']} "{config['github']} 🔗")
      """)
   )

   return await ctx.respond(embeds=[embed], ephemeral=True)





# # /uwu
# @bot.slash_command(name="uwu", description="hehe murr")
# async def uwu(ctx):
#    await ctx.respond("uwu", ephemeral=True)





# /berry-joke
@bot.slash_command(name = "berry-joke", description = "fresh berry jokes from jojo 💬")
async def berry_joke(ctx):
   jokes = [
      [ "what do you call a sad strawberry?", "a blue berry 😔" ],
      [ "what do you call berries in the wind?", "\"blewberries\"! 🌬" ],
      [ "how do you fix a blueberry?", "with a blueberry patch 🩹" ],
      [ "what do you call a russian raspberry dipped in lighter fluid?", "rasp-butane 🔥" ],
      [ "what did one cranberry say to another at christmas?", "'tis the season to be jelly! 🎄" ],
      [ "what kind of fruit is a crook?", "a strobbery! 🍓" ],
      [ "what is the difference between a pirate and a cranberry farmer?", "a pirate buries his treasure while a cranberry farmer treasures his berries! 🏴‍☠️" ],
      [ "what do you get when you walk around with berries in your shoes?", "toe jam! 🐾" ],
      [ "how can blueberries talk on the phone if they have no hands?", "they use bluetooth! 📳" ],
      [ "how do berries appear?", "they come out of the blue! 🔷" ],
      [ "why were the little strawberries upset?", "because their parents were in a jam! 🔪" ],
      [ "why can't you make a crumble with 3.14 blackberries?", "because that'd be a pi! 🥧" ],
      [ "why was the raspberry by himself?", "because the banana split! 🍌" ],
      [ "how do you call a magic berry?", "cherry potter! 🍒" ],
      [ "why did the strawberry stop in the middle of the road?", "because it ran out of juice! 🥤" ],
      [ "what is a scarecrow's favourite fruit?", "straw-berries! 🦅" ],
      [ "what's red, made of strawberries, and sucks your blood?", "a jam-pire! 🦇" ],
      [ "what do you do to a dead berry?", "you \\*berry\\* it ⚰️" ],
      [ "what is it called when a raspberry is late to class?", "they're tarty! 🥧" ],
      [ "what did the blueberry pie say to the pecan pie?", "\"you're nuts!\" 🥜" ],
      [ "why did the blueberry go out with the fig?", "because it couldn't find a date.. 💘" ]
   ]
   joke = random.choice(jokes)


   class View(discord.ui.View):
      def __init__(self):
         super().__init__(timeout=5)
         self.pressed = False

      @discord.ui.button(style=discord.ButtonStyle.primary, custom_id=f"{ctx.interaction.id}:why", label="why?", emoji=discord.PartialEmoji.from_str(emojis["speech_bubble_left"]))
      async def button(self, button: discord.Button, interaction: discord.Interaction):
         self.pressed = True
         self.stop()
         await interaction.response.edit_message(
            content = f"**{joke[0]}**\n> {joke[1]}",
            view = None
         )

      async def on_timeout(self):
         if not self.pressed:
            print("hewwo")
            self.children[0].disabled = True
            await ctx.interaction.edit_original_message(view=self)


   await ctx.respond(
      content = f"**{joke[0]}**",
      view = View(),
      ephemeral = True
   )





# /berry
@bot.slash_command(name = "berry", description = "random berry picture 📷")
async def berry(ctx):
   await ctx.defer(ephemeral=True)

   berry_picture = random.choice(os.listdir("./assets/berries"))
   attachment = discord.File(filename=f"berry.{berry_picture.split('.')[1]}", fp=f"./assets/berries/{berry_picture}")

   return await ctx.interaction.edit_original_message(files=[attachment])





# creates a thread if the message is "uwu" and it was sent in channel #berry-bot (910267354104070164)
@bot.listen()
async def on_message(message):
   if message.channel.type != discord.ChannelType.text: return
   if message.channel.id != 910267354104070164: return
   if message.content != "uwu": return

   await message.create_thread(name=f"❕aotd {datetime.datetime.now().strftime('%m-%d')}❗")





# run the bot
print("🦊")

token = os.getenv("TOKEN")
bot.run(token)