import discord
from discord.ext import commands
from discord.commands import Option, permissions

import requests, os
from io import BytesIO

import json
config = json.loads(open("./config.json", "r").read())


class say(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   # slash command options: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_options.py
   # slash command permissions: https://github.com/Pycord-Development/pycord/blob/master/examples/app_commands/slash_perms.py
   @commands.slash_command(name="say", description="make me say something 💬", default_permission=False)
   @permissions.has_any_role(817623935805292564, 719619795581927434, 894387548992962650, 630170084991696927, 469194125086818316, 630185268267450369) # "owner 🐰🦊🐺🦌", "literal fox lord 🦊", "🦊", "Admins", "Moderators", "Trial Mods"
   async def say(self, ctx, content: Option(str, "what should i say? 💭"), channel: Option(discord.TextChannel, "what channel should i say this in? 📩", required=False), reply_to: Option(str, "the id of the message to reply to in the channel ✉️", name="reply-to-message-id", required=False), attachment: Option(discord.Attachment, "an attachment to send with the message 🖼️", required=False)):
      # message content is too long, max 2000 characters
      if len(content) > 2000:
         return await ctx.respond(content="that message is too long! it can only be under 2000 characters", ephemeral=True)


      # attachment is too large, max 8mb
      to_megabytes = lambda bytes: bytes / 1e+6
      
      if attachment and to_megabytes(attachment.size) > 8:
         return await ctx.respond(content="the attachment's file size is too large! it can only be under 8 megabytes in size", ephemeral=True)


      # defer interaction reply while we wait
      await ctx.defer(ephemeral=True)


      # since ephemeral attachments don't exist forever, we need to get the attachment's buffer instead
      def get_image():
         # we're not sending an attachment
         if not attachment:
            return None

         # get the buffer
         r = requests.get(
            attachment.url,
            headers = {
               "User-Agent": f"discord-berry-bot/{config['version']} ({os.getenv('AGENT')}) ({config['github']})"
            }
         )

         # make this into an attachment
         image = BytesIO(r.content)
         file = discord.File(image, filename=f"{attachment.filename}.png")
         
         # return the attachment
         return file

      file = get_image()


      # send this message in the channel specified, or in the channel this interaction was sent in
      ch = channel or ctx.channel


      # replying to a message
      if reply_to:
         try:
            message = await ch.fetch_message(int(reply_to)) # get the message to reply to

            if file:
               await message.reply(content=content, file=file, allowed_mentions=discord.AllowedMentions.none()) # send a message (with attachment)
            else:
               await message.reply(content=content, allowed_mentions=discord.AllowedMentions.none()) # send a message

         except:
            return await ctx.interaction.edit_original_message(content=f"the provided `reply-to-message-id` isn't a valid message in {ch.mention}!") # this message doesn't exist

      # sending a message
      else:
         if file:
            await ch.send(content=content, file=file, allowed_mentions=discord.AllowedMentions.none()) # send a message (with attachment)
         else:
            await ch.send(content=content, allowed_mentions=discord.AllowedMentions.none()) # send a message


      # edit the deferred interaction of completion
      return await ctx.interaction.edit_original_message(content=f"sent message in {ch.mention}!")
      


def setup(bot):
   bot.add_cog(say(bot))