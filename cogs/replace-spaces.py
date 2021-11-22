import discord
from discord.ext import commands
from discord.commands import Option


class replace_spaces(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="replace-spaces", description="› replace the spaces in a content with a character or emoji 💬")
   async def replace_spaces(self, ctx, content: Option(str, "› content of the message to replace spaces 📝"), separator: Option(str, "› a character or emoji (or anything) to replace spaces with")):
      formatted_content = content.replace(" ", separator)
      return await ctx.respond(content=formatted_content, allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
   bot.add_cog(replace_spaces(bot))