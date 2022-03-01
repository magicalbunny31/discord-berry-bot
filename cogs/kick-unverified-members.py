from datetime import datetime
from discord.ext import tasks, commands


class kick_unverified_members(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.kick_unverified_members.start()


   def cog_unload(self):
      self.kick_unverified_members.cancel()


   @tasks.loop(seconds=3600) # run this every hour
   async def kick_unverified_members(self):
      guild = await self.bot.fetch_guild(438534833921064972) # get this guild (gb server)

      everyone_role_id = guild.id # @everyone role id (it's always the id of the guild!)
      unverified_role_id = 733273608272740353 # unverified role id


      async for member in guild.fetch_members(limit=None): # loop all members in the guild
         member_roles_ids = [role.id for role in member.roles] # map out all the member's roles by their ids
         is_unverified_by_roles = member_roles_ids == [everyone_role_id, unverified_role_id] # if they --only-- have @everyone and unverified role, they're unverified

   
         if not is_unverified_by_roles: # let's filter out the verified members by roles
            continue


         joined_at = member.joined_at # the timestamp that this member joined the server at


         if joined_at is None: # uh oh! looks like we don't know this join time so return early
            continue


         one_week_ago = datetime.now().timestamp() - 604800 # the timestamp this time but one week ago
         joined_at_timestamp = joined_at.timestamp() # the timestamp of this member's join

         is_week_old = one_week_ago > joined_at_timestamp # this member joined over a week ago

         
         if not is_week_old: # this member is unverified but they joined within the past week
            continue


         await member.kick(reason="didn't verify in the past week") # kick this member, bai bai!



def setup(bot):
   bot.add_cog(kick_unverified_members(bot))