import discord, random
from discord.ext import commands

import json
emojis = json.loads(open("./assets/data/emojis.json", "r").read())

from assets.data.strip_indents import strip_indents


class berry_joke(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="berry-joke", description="› fresh berry jokes from jojo 💬")
   async def berry_joke(self, ctx):
      jokes = [
         [ "what do you call a sad strawberry?", "a blue berry 😔" ],
         [ "what do you call berries in the wind?", "\"blewberries\"! 🌬" ],
         [ "how do you fix a blueberry?", "with a blueberry patch 🩹" ],
         [ "what do you call a russian raspberry dipped in lighter fluid?", "rasp-butane 🔥" ],
         [ "what did one cranberry say to another at christmas?", "'tis the season to be jelly! 🎄" ],
         [ "what kind of fruit is a crook?", "a strobbery! 🍓" ],
         [ "what is the difference between a pirate and a cranberry farmer?", "a pirate buries his treasure while a cranberry farmer treasures his berries! 🏴‍☠️" ],
         [ "what do you get when you walk around with berries in your shoes?", "toe jam! 🐾" ],
         [ "how can blueberries talk on the phone if they have no hands?", "they use bluetooth! 📳" ],
         [ "how do berries appear?", "they come out of the blue! 🔷" ],
         [ "why were the little strawberries upset?", "because their parents were in a jam! 🔪" ],
         [ "why can't you make a crumble with 3.14 blackberries?", "because that'd be a pi! 🥧" ],
         [ "why was the raspberry by himself?", "because the banana split! 🍌" ],
         [ "what do you call a magic berry?", "cherry potter! 🍒" ],
         [ "why did the strawberry stop in the middle of the road?", "because it ran out of juice! 🥤" ],
         [ "what is a scarecrow's favourite fruit?", "straw-berries! 🦅" ],
         [ "what is red, made of strawberries, and sucks your blood?", "a jam-pire! 🦇" ],
         [ "what do you do to a dead berry?", "you \\*berry\\* it ⚰️" ],
         [ "what is it called when a raspberry is late to class?", "they're tarty! 🥧" ],
         [ "what did the blueberry pie say to the pecan pie?", "\"you're nuts!\" 🥜" ],
         [ "why did the blueberry go out with the fig?", "because it couldn't find a date.. 💘" ]
      ]
      joke = random.choice(jokes)


      class View(discord.ui.View):
         def __init__(self):
            super().__init__(timeout=120)
            self.pressed = False

         @discord.ui.button(style=discord.ButtonStyle.primary, custom_id=f"{ctx.interaction.id}:why", label=f"{joke[0].split()[0]}?", emoji=discord.PartialEmoji.from_str(emojis["speech_bubble_left"]))
         async def button(self, button: discord.Button, interaction: discord.Interaction):
            if interaction.user.id != ctx.user.id:
               return await interaction.response.send_message(
                  content = strip_indents(f"""
                     since {ctx.user.mention} used this command, only they can reveal the answer!
                     prefer to press the button? use the command `/berry-joke`
                  """),
                  ephemeral = True
               )

            self.pressed = True
            self.stop()
            await interaction.response.edit_message(
               content = f"**{joke[0]}**\n> {joke[1]}",
               view = None
            )

         async def on_timeout(self):
            if not self.pressed:
               self.children[0].disabled = True
               await ctx.interaction.edit_original_message(view=self)


      return await ctx.respond(
         content = f"**{joke[0]}**",
         view = View()
      )


def setup(bot):
   bot.add_cog(berry_joke(bot))