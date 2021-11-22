import discord
from discord.ext import commands
from discord.commands import Option, permissions


class say(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   # slash command options: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py
   # slash command permissions: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_perms.py
   @commands.slash_command(name="say", description="› make me say something 💬", default_permission=False)
   @permissions.has_any_role("🦊", "Moderators", "Admins")
   async def say(self, ctx, content: Option(str, "› what should i say? 📝"), channel: Option(discord.TextChannel, "› what channel should i say this in? 💬")):
      if len(content) > 2000:
         return await ctx.respond(content="that message is too long! it can only be under 2000 characters", ephemeral=True)

      await ctx.defer(ephemeral=True)

      await channel.send(content=content, allowed_mentions=discord.AllowedMentions(users=False))

      return await ctx.interaction.edit_original_message(content=f"sent message in {channel.mention}!")
      


def setup(bot):
   bot.add_cog(say(bot))