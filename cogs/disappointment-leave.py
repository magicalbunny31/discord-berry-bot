from discord.ext import commands

class disapproveLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.channel.id == 802739811630841866 and message.author.id == 159985870458322944):
            await message.reply("https://www.youtube.com/watch?v=PqUenEMwsdQ")
            

async def setup(bot):
    await bot.add_cog(disapproveLeave(bot))
