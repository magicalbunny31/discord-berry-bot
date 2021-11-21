import discord, random, os
from discord.ext import commands


class berry(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="berry", description="› random berry picture 📷")
   async def berry(self, ctx):
      await ctx.defer()

      berry_picture = random.choice(os.listdir("./assets/berries"))
      attachment = discord.File(filename=f"berry.{berry_picture.split('.')[1]}", fp=f"./assets/berries/{berry_picture}")

      return await ctx.interaction.edit_original_message(files=[attachment])


def setup(bot):
   bot.add_cog(berry(bot))