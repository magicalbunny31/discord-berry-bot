import discord
from discord.ext import commands

import re

import time

from assets.data.strip_indents import strip_indents

import json
config = json.loads(open("./config.json", "r").read())



class View(discord.ui.View):
   def __init__(self):
      super().__init__(timeout=None)


   @discord.ui.button(
      custom_id = "submit-fe2cm-map-id:button",
      label = "Submit FE2CM Map ID",
      emoji = discord.PartialEmoji.from_str("<:envelope_with_arrow:846798115184705566>"),
      style = discord.ButtonStyle.primary,
   )
   async def button(self, button: discord.ui.Button, interaction: discord.Interaction):
      class Modal(discord.ui.Modal):
         def __init__(self):
            super().__init__("Submit FE2CM Map ID 📩", "submit-fe2cm-map-id:submit-id")
            self.add_item(
               discord.ui.InputText(
                  style = discord.InputTextStyle.short,
                  custom_id = "id",
                  label = "Map ID 🆔",
                  placeholder = "What is this FE2CM Map's ID? 📝",
                  min_length = 6,
                  max_length = 7,
                  required = True
               )
            )


         # when the modal is submitted
         async def callback(self, interaction: discord.Interaction):
            id = self.children[0].value.strip()


            # defer the interaction
            await interaction.response.defer(ephemeral=True)


            # start the database connection
            import sqlite3
            connection = sqlite3.connect("./assets/database/fe2cm-map-ids.db")
            cursor = connection.cursor()


            # check if this a valid id
            fe2cm_map_id_regex = re.compile("^[a-z\d\-+=\/*]{6,7}$", re.I)
            is_fe2cm_map_id = bool(fe2cm_map_id_regex.match(id))

            if not is_fe2cm_map_id:
               return await interaction.edit_original_message(content=f"**`{id}`** isn't a valid fe2cm id!")


            # too many ids, max 25
            cursor.execute("""
               SELECT COUNT(map_id)
               FROM fe2cm_map_ids
            """)
            number_of_ids = cursor.fetchone()[0]

            if number_of_ids >= 25:
               return await interaction.edit_original_message(content=f"there's can only be 25 ids in the list at a time, come back later when some ids are removed!")


            # check if this id isn't in the database
            cursor.execute("""
               SELECT map_id
               FROM fe2cm_map_ids
               WHERE map_id = ?
            """, (id,))
            data = cursor.fetchone()

            if data is not None:
               return await interaction.edit_original_message(content=f"**`{id}`** is already in the list, sorry!")


            # add it to the database
            cursor.execute("""
               INSERT INTO fe2cm_map_ids
               VALUES (?, ?, ?)
            """, (id, int(time.time()), interaction.user.id))


            # update the message
            query = cursor.execute("SELECT * FROM fe2cm_map_ids AS data")
            column = [ d[0] for d in query.description ]
            data = [ dict(zip(column, r)) for r in query.fetchall() ]

            await interaction.message.edit(
               embeds = [
                  discord.Embed(
                     colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
                     title = "Submit your FE2CM Map IDs here!",
                     description = strip_indents(f"""
                        Here for the stream?
                        Want <@434894511571730433> to play a map?
                        Well, you've come to the right place!

                        Just press the <:envelope_with_arrow:846798115184705566> **Submit FE2CM Map ID** button to submit a map..
                        ..And watch it appear in the list below!

                        The list can only hold up to 25 IDs,
                        So please be considerate and don't flood the list with only your submissions.
                        
                        Make sure to submit real maps, or else they may risk removal from the list.
                        All rules in <#488229821105831936> apply to all submissions.
                        Happy submitting! <:happ:906683365791502366>
                     """)
                  ) \
                     .set_footer(text="bunny was here haii", icon_url=(await interaction.client.fetch_user(config["developer"])).avatar.url),
                  discord.Embed(
                     colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
                     title = "Map Ids",
                     description = "\n".join(
                        map(
                           lambda map: strip_indents(f"**`{map['map_id']}`** (<@{map['submitter_id']}> › <t:{map['submitted_at_timestamp']}:R>)").strip(),
                           data
                        )
                     ) or "**`There are no IDs to show..`**"
                  )
               ]
            )


            # save and end the database connection
            connection.commit()
            connection.close()


            # edit the deferred interaction
            return await interaction.edit_original_message(content=f"thanks for adding **`{id}`** to the list, {interaction.user.mention}!", allowed_mentions=discord.AllowedMentions.none())



      # send the modal
      return await interaction.response.send_modal(Modal())



   @discord.ui.button(
      custom_id = "submit-fe2cm-map-id:remove_id",
      emoji = discord.PartialEmoji.from_str("<:bomb:792165588209762325>"),
      style = discord.ButtonStyle.danger
   )
   async def configure(self, button: discord.ui.Button, interaction: discord.Interaction):
      # only give staff (or "literal fox lord 🦊") the ability to remove any id
      allowed_roles = [630185268267450369, 469194125086818316, 630170084991696927, 719619795581927434]
      member_roles = list(map(lambda role: role.id, interaction.user.roles))


      # function for this owo
      async def remove_id(can_remove_any_id):
         # defer the interaction
         await interaction.response.defer(ephemeral=True)


         # start the database connection
         import sqlite3
         connection = sqlite3.connect("./assets/database/fe2cm-map-ids.db")
         cursor = connection.cursor()


         # get the data
         query = cursor.execute("SELECT * FROM fe2cm_map_ids AS data") if can_remove_any_id else cursor.execute("SELECT * FROM fe2cm_map_ids AS data WHERE submitter_id = ?", (interaction.user.id,))
         column = [ d[0] for d in query.description ]
         data = [ dict(zip(column, r)) for r in query.fetchall() ]


         # no ids to remove
         if not len(data):
            return await interaction.edit_original_message(
               content = "there are no ids in the list!" if can_remove_any_id else "you can only remove ids from this list that you have submitted!"
            )


         # create a view to remove an id from the database
         class RemoveId(discord.ui.View):
            def __init__(self):
               super().__init__(timeout=600) # 10 minutes


            @discord.ui.select(
               custom_id = f"{interaction.id}:remove_id",
               min_values = 1,
               max_values = len(data),
               placeholder = "Select the FE2CM Map ID(s) to remove..",
               options = list(
                  map(
                     lambda map: discord.SelectOption(
                        label = map["map_id"],
                        value = map["map_id"]
                     ),
                     data
                  )
               )
            )
            async def remove_id(self, select: discord.ui.Select, i: discord.Interaction):
               # list of selected ids to remove
               ids_to_remove = select.values

               # stop the select menu
               self.stop()

               # remove them from the database
               for id in ids_to_remove:
                  cursor.execute("DELETE FROM fe2cm_map_ids WHERE map_id = ?", (id,))

               # update the message
               query = cursor.execute("SELECT * FROM fe2cm_map_ids AS data")
               column = [ d[0] for d in query.description ]
               data = [ dict(zip(column, r)) for r in query.fetchall() ]

               await interaction.message.edit(
                  embeds = [
                     discord.Embed(
                        colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
                        title = "Submit your FE2CM Map IDs here!",
                        description = strip_indents(f"""
                           Here for the stream?
                           Want <@434894511571730433> to play a map?
                           Well, you've come to the right place!

                           Just press the <:envelope_with_arrow:846798115184705566> **Submit FE2CM Map ID** button to submit a map..
                           ..And watch it appear in the list below!

                           The list can only hold up to 25 IDs,
                           So please be considerate and don't flood the list with only your submissions.
                           
                           Make sure to submit real maps, or else they may risk removal from the list.
                           All rules in <#488229821105831936> apply to all submissions.
                           Happy submitting! <:happ:906683365791502366>
                        """)
                     ) \
                        .set_footer(text="bunny was here haii", icon_url=(await interaction.client.fetch_user(config["developer"])).avatar.url),
                     discord.Embed(
                        colour = discord.Colour.from_rgb(15, 135, 240), # #0f87f0
                        title = "Map Ids",
                        description = "\n".join(
                           map(
                              lambda map: strip_indents(f"**`{map['map_id']}`** (<@{map['submitter_id']}> › <t:{map['submitted_at_timestamp']}:R>)").strip(),
                              data
                           )
                        ) or "**`There are no IDs to show..`**"
                     )
                  ]
               )

               # save and end the database connection
               connection.commit()
               connection.close()

               # edit the original interaction
               return await i.response.edit_message(content=f"removed ids: {', '.join(map(lambda id: f'**`{id}`**', ids_to_remove))}!", view=None)


            async def on_timeout(self):
               # save and end the database connection
               connection.commit()
               connection.close()

               # disable the menu and show the timed out message
               self.children[0].disabled = True
               return await interaction.edit_original_message(
                  content = "looks like you've timed out the menu! press the button again to recreate the menu",
                  view = self
               )

         
         # edit the deferred interaction
         await interaction.edit_original_message(
            content = "select the FE2CM Map Id(s) you want to remove from the list below..",
            view = RemoveId()
         )


      can_remove_any_id = any(allowed_role in member_roles for allowed_role in allowed_roles)
      await remove_id(can_remove_any_id)
      


class submit_fe2cm_map_id(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.added = False


   @commands.Cog.listener()
   async def on_ready(self):
      if not self.added:
         self.bot.add_view(View())
         self.added = True



def setup(bot):
   bot.add_cog(submit_fe2cm_map_id(bot))