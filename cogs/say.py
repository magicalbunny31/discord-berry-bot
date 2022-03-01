import discord
from discord.ext import commands
from discord.commands import Option, permissions


class say(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   # slash command options: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py
   # slash command permissions: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_perms.py
   @commands.slash_command(name="say", description="make me say something 💬", default_permission=False)
   @permissions.has_any_role("owner 🐰🦊🐺🦌", "literal fox lord 🦊", "🦊", "Moderators", "Admins")
   async def say(self, ctx, content: Option(str, "what should i say? 💭"), channel: Option(discord.TextChannel, "what channel should i say this in? 📩", required=False), reply_to: Option(str, "the id of the message to reply to in the channel ✉️", name="reply-to-message-id", required=False)):
      if len(content) > 2000:
         return await ctx.respond(content="that message is too long! it can only be under 2000 characters", ephemeral=True)

      await ctx.defer(ephemeral=True)

      ch = channel or ctx.channel

      if reply_to:
         try:
            message = await ch.fetch_message(int(reply_to))
            await message.reply(content=content, allowed_mentions=discord.AllowedMentions.none())
         except:
            return await ctx.interaction.edit_original_message(content=f"the provided `reply-to-message-id` isn't a valid message in {ch.mention}!")

      else:
         await ch.send(content=content, allowed_mentions=discord.AllowedMentions.none())

      return await ctx.interaction.edit_original_message(content=f"sent message in {ch.mention}!")
      


def setup(bot):
   bot.add_cog(say(bot))