from discord.ext import commands


class uwu(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="uwu", description="› hehe murr")
   async def uwu(self, ctx):
      return await ctx.respond("uwu", ephemeral=True)


def setup(bot):
   bot.add_cog(uwu(bot))