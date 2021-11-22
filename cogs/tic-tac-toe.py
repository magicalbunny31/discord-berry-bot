import discord, random
from discord.ext import commands
from discord.commands import Option

from assets.data.strip_indents import strip_indents


class tic_tac_toe(commands.Cog):
   def __init__(self, bot):
      self.bot = bot


   @commands.slash_command(name="tic-tac-toe", description="› play tic-tac-toe with another user! 🎮")
   async def tic_tac_toe(self, ctx, user: Option(discord.User, "› user to play against 👥")):
      user_x = ctx.author
      user_o = user

      if user_x.id == user_o.id:
         return await ctx.respond(content="you can't play this game by yourself, duh", ephemeral=True)

      if user_o.id == self.bot.user.id:
         return await ctx.respond(content="i'd win every game of tic-tac-toe if you played with me! i'll spare you for now", ephemeral=True)

      if user_o.bot:
         return await ctx.respond(content="bots don't like playing tic-tac-toe, so i hear", ephemeral=True)

      #                              x, o
      first_player = random.choice([-1, 1])

      class Button(discord.ui.Button):
         def __init__(self, x, y): # x and y are type int
            super().__init__(style=discord.ButtonStyle.primary, label="\u200b", row=y)
            self.x = x
            self.y = y

         async def callback(self, interaction: discord.Interaction):
            view: View = self.view

            state = view.board[self.y][self.x]
            if state in (view.x, view.o): return

            if view.turn == view.x:
               if interaction.user.id == user_o.id:
                  return await interaction.response.send_message(
                     content = strip_indents(f"""
                        hey! it's not your turn yet!
                     """),
                     ephemeral = True
                  )

               self.style = discord.ButtonStyle.secondary
               self.label = "x"
               self.disabled = True
               
               view.board[self.y][self.x] = view.x
               view.turn = view.o
               content = strip_indents(f"""
                  **`tic-tac-toe`**
                  {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                  > {user_o.mention}'s turn
               """)

            else:
               if interaction.user.id == user_x.id:
                  return await interaction.response.send_message(
                     content = strip_indents(f"""
                        hey! it's not your turn yet!
                     """),
                     ephemeral = True
                  )

               self.style = discord.ButtonStyle.secondary
               self.label = "o"
               self.disabled = True
               
               view.board[self.y][self.x] = view.o
               view.turn = view.x
               content = strip_indents(f"""
                  **`tic-tac-toe`**
                  {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                  > {user_x.mention}'s turn
               """)

            winner = view.check_winner()
            if winner is not None:
               if winner == view.x:
                  content = strip_indents(f"""
                     **`tic-tac-toe`**
                     {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                     > {user_x.mention} wins! \\🎉
                  """)
               elif winner == view.o:
                  content = strip_indents(f"""
                     **`tic-tac-toe`**
                     {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                     > {user_o.mention} wins! \\🎉
                  """)

               else:
                  content = strip_indents(f"""
                     **`tic-tac-toe`**
                     {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                     > it's a draw
                  """)

               for button in view.children: button.disabled = True

               view.stop()

            return await interaction.response.edit_message(content=content, view=view)


      class View(discord.ui.View):
         # to determine the winner, it'll work with a bit of maths rather than manually checking each button's state
         x = -1
         o = 1
         is_tie = 2

         def __init__(self):
            super().__init__(timeout=840)
            self.turn = first_player
            self.board = [ # each button will correspond to a number, which state's will be affected
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]
            ]

            for x in range(3):
               for y in range(3):
                  self.add_item(Button(x, y))

         def check_winner(self):
            # across ⬆
            for across in self.board:
               value = sum(across)
               if   value ==  3: return self.o
               elif value == -3: return self.x

            # vertical ➡
            for line in range(3):
               value = self.board[0][line] + self.board[1][line] + self.board[2][line]
               if   value ==  3: return self.o
               elif value == -3: return self.x

            # diagonal ↗
            right_diagonal = self.board[0][2] + self.board[1][1] + self.board[2][0]
            if   right_diagonal ==  3: return self.o
            elif right_diagonal == -3: return self.x

            # diagonal ↖
            left_diagonal = self.board[0][0] + self.board[1][1] + self.board[2][2]
            if   left_diagonal ==  3: return self.o
            elif left_diagonal == -3: return self.x

            # check if draw
            if all(i != 0 for row in self.board for i in row): return self.is_tie

            # the game is still going!
            return None

         async def on_timeout(self):
            for button in self.children: button.disabled = True
            await ctx.interaction.edit_original_message(
               content = strip_indents(f"""
                  **`tic-tac-toe`**
                  {user_x.mention} (`x`) vs {user_o.mention} (`o`)
                  > game timed out
               """),
               view = self,
               allowed_mentions = discord.AllowedMentions.none()
            )

      return await ctx.respond(
         content = strip_indents(f"""
            **`tic-tac-toe`**
            {user_x.mention} (`x`) vs {user_o.mention} (`o`)
            > {user_x.mention if first_player == -1 else user_o.mention}'s turn
         """),
         view = View()
      )


def setup(bot):
   bot.add_cog(tic_tac_toe(bot))