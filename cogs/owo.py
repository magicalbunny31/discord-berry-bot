import random, re
from discord.ext import commands
from discord.commands import Option


class owo(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="owo", description="› owo-fy some text 💬")
   async def owo(self, ctx, text: Option(str, "› text to owo-fy 📝")):
      # rules defined from bun 🐰🐾 (my main bot)'s own owo command (excluding swears)
      # ..this is also pretty much copied code from bun 🐰🐾 lmao

      # you      => chu
      # yes      => yus
      # no       => nu
      # n<vowel> => ny<vowel>
      # hi       => hai
      # howdy    => meowdy
      # cool     => kewl
      # for      => fur
      # very     => ver
      # good     => gud
      # cheese   => sergal
      # r, l     => w
      # -ove     => -uv
      # th       => d
      # pos      => paws
      # !        => :3, ;3, èwé, uwu
      # ?        => owo
      # ome      => um

      
      split_spaces = re.split("\s", text)
      texts = []

      for text in split_spaces:
         split_regex = re.split("!|\?", text)
         for t in split_regex: texts.append(t)

      
      translated = []

      for text in texts:
         t = text

         t = re.sub("\byou", "chu", t)

         t = re.sub("\byes", "yus", t)

         t = re.sub("\bno", "nu", t)

         def ny(match): return f"{match.group()[0:1]}y{match.group()[1:2]}"
         t = re.sub("n[aeiou]", ny, t)

         t = re.sub("\bhi", "hai", t)

         t = re.sub("\bhowdy", "meowdy", t)

         t = re.sub("\bcool", "kewl", t)

         t = re.sub("\bfor", "fur", t)

         t = re.sub("\bvery", "ver", t)

         t = re.sub("\bgood", "gud", t)

         t = re.sub("\bcheese", "sergal", t)

         t = re.sub("[rl]", "w", t)

         t = re.sub("ove", "uv", t)

         t = re.sub("th", "d", t)

         t = re.sub("pos", "paws", t)

         t = re.sub("!", random.choice([":3", ";3", "èwé", "uwu"]), t)

         t = re.sub("\?", "owo", t)

         t = re.sub("ome", "um", t)

         translated.append(t.strip())

      translated = filter(None, translated)


      owo = " ".join(translated)

      if len(owo) > 2000:
         return await ctx.respond(content="the message is too long to translate! try making it shorter", ephemeral=True)

      return await ctx.respond(content=owo)


def setup(bot):
   bot.add_cog(owo(bot))