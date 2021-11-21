import random
from discord.ext import commands


class flip(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="flip", description="› flip a coin 👛")
   async def flip(self, ctx):
      side = random.choice(["heads", "tails"])
      return await ctx.respond(content=f"the coin reads **{side}**! 🪙")


def setup(bot):
   bot.add_cog(flip(bot))