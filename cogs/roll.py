import discord, random
from discord.ext import commands
from discord.commands import Option

import json
emojis = json.loads(open("./emojis.json", "r").read())


class roll(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="roll", description="› roll a die! 🎲")
   async def roll(self, ctx, sides: Option(int, "› number if sides this die will have (minimum 2) 🔢", min_value=2)):
      emoji = emojis["d6"] if sides < 20 else emojis["d20"]
      rolled = random.randint(1, sides)

      if rolled == 1:
         return await ctx.respond(content=f"oof, you rolled **{rolled}** {emoji}")
      elif rolled == sides:
         return await ctx.respond(content=f"congratulations, {ctx.user.mention}! you rolled **{rolled}** {emoji}", allowed_mentions=discord.AllowedMentions(users=False))
      else:
         return await ctx.respond(content=f"you rolled **{rolled}** {emoji}")


def setup(bot):
   bot.add_cog(roll(bot))