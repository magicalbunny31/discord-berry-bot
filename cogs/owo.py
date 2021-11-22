import random, re
from discord.ext import commands
from discord.commands import Option

from assets.data.bad_words import bad_words


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


      if any(word in text for word in bad_words()):
         return await ctx.respond(content="i can't translate \\*that\\*; your content contains bad words!", ephemeral=True)

      
      split_spaces = re.split(r"\s", text, flags=re.M|re.I)
      texts = []

      for text in split_spaces:
         split_regex = re.split(r"(!|\?)", text, flags=re.M|re.I)
         for t in filter(None, split_regex): texts.append(t)

      
      translated = []

      for text in texts:
         t = text

         t = re.sub("you", "chu", t, flags=re.M|re.I)

         t = re.sub("yes", "yus", t, flags=re.M|re.I)

         t = re.sub("no", "nu", t, flags=re.M|re.I)

         def ny(match): return f"{match.group()[0:1]}y{match.group()[1:2]}"
         t = re.sub("n[aeiou]", ny, t, flags=re.M|re.I)

         t = re.sub("hi", "hai", t, flags=re.M|re.I)

         t = re.sub("howdy", "meowdy", t, flags=re.M|re.I)

         t = re.sub("cool", "kewl", t, flags=re.M|re.I)

         t = re.sub("for", "fur", t, flags=re.M|re.I)

         t = re.sub("very", "ver", t, flags=re.M|re.I)

         t = re.sub("good", "gud", t, flags=re.M|re.I)

         t = re.sub("cheese", "sergal", t, flags=re.M|re.I)

         t = re.sub("[rl]", "w", t, flags=re.M|re.I)

         t = re.sub("ove", "uv", t, flags=re.M|re.I)

         t = re.sub("th", "d", t, flags=re.M|re.I)

         t = re.sub("pos", "paws", t, flags=re.M|re.I)

         t = re.sub("!", random.choice([":3", ";3", "èwé", "uwu"]), t, flags=re.M|re.I)

         t = re.sub("\?", "owo", t, flags=re.M|re.I)

         t = re.sub("ome", "um", t, flags=re.M|re.I)

         translated.append(t.strip())

      translated = filter(None, translated)


      owo = " ".join(translated)

      if any(word in owo for word in bad_words()):
         return await ctx.respond(content="unfortunately, the translated content contains bad words so i won't send it", ephemeral=True)

      if len(owo) > 2000:
         return await ctx.respond(content="the message is too long to translate! try making it shorter", ephemeral=True)

      return await ctx.respond(content=owo)


def setup(bot):
   bot.add_cog(owo(bot))