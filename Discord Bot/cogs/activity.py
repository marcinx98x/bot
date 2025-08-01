from discord.ext import commands
from database import db

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        db.add_points(user_id, 1)  # Dodaj punkt za każdą wiadomość

    @commands.command(name="punkty")
    async def check_points(self, ctx):
        user_id = str(ctx.author.id)
        points = db.get_points(user_id)
        await ctx.send(f"Masz {points} punktów 🧠")

async def setup(bot):
    await bot.add_cog(Activity(bot))