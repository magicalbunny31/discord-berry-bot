import discord, emoji
from discord.ext import commands

import json
config = json.loads(open("./config.json", "r").read())
emojis = json.loads(open("./assets/data/emojis.json", "r").read())

from textwrap import dedent
def strip_indents(text): return dedent(text).strip()



class help(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="help", description="› help with berry bot 🍓")
   async def help(self, ctx):
      def replace_emoji(match): return f"\\{match.group()}" 
      def name(command): return f"› `/{command.name}` - {emoji.get_emoji_regexp().sub(replace_emoji, command.description)}"
      commands = "\n".join(list(map(name, self.bot.commands)))

      developer = await self.bot.fetch_user(config["developer"])

      embed = discord.Embed(
         colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
         description = strip_indents(f"""
            {self.bot.user.mention} : **[Gentle Berry's Server]({config["invite"]} "{config["invite"]} 🔗")**

            **commands** {emojis["yellow_book"]}
            {commands}

            `developer` › {developer.mention} 2021-present {emojis["happ"]}
            `github` › [link to repository]({config["github"]} "{config["github"]} 🔗")
         """)
      )

      print(embed.description)

      return await ctx.respond(embeds=[embed])


def setup(bot):
   bot.add_cog(help(bot))