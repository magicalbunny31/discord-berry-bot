#########################################
#                                       #
#   code by magicalbunny31              #
#   https://github.com/magicalbunny31   #
#                                       #
#########################################


# https://docs.pycord.dev/en/master/api.html

# pycord installation!!
# win: py -m pip install -U git+https://github.com/Pycord-Development/pycord
# lin: pip install -U git+https://github.com/Pycord-Development/pycord
# mac: why would i use that lmao

import discord, os

from dotenv import load_dotenv
load_dotenv()

# the bot
bot = discord.Bot(
   # debug_guild = 859172731386986516,
   activity = discord.Activity(
      name = "berry berry berry 🍓",
      type = discord.ActivityType.watching
   ),
   status = discord.Status.idle
)


# load cogs
for file in os.listdir("./cogs"):
   if not file.endswith(".py"): continue
   if not bot.debug_guild and file == "uwu.py": continue # if this isn't in debug, don't use the test command

   bot.load_extension(f"cogs.{file[0:-3]}")


# run the bot
print("🦊")

token = os.getenv("TOKEN")
bot.run(token)