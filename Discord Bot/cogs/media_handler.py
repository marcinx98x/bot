from discord.ext import commands
import random

MEDIA = [
    "https://media.tenor.com/FUNNY1.gif",
    "https://media.tenor.com/FUNNY2.gif",
    "https://media.tenor.com/FUNNY3.gif"
]

class MediaHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gif")
    async def send_gif(self, ctx):
        await ctx.send(random.choice(MEDIA))

async def setup(bot):
    await bot.add_cog(MediaHandler(bot))