import discord
from discord.ext import commands

def load_banned_words():
    try:
        with open("zakazane słowa.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.banned_words = load_banned_words()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        lower_msg = message.content.lower()

        # 🔒 Sprawdź zakazane słowa
        for word in self.banned_words:
            if word in lower_msg:
                await message.delete()
                await message.channel.send(f"🚫 {message.author.mention}, to słowo jest zakazane!")
                return

        # 💬 Reakcje ANNY
        responses = {
            "hej": "No siema! 👋",
            "anna": "Królowa jest tylko jedna 💅",
            "bot": "Ktoś mnie wołał?"
        }

        for trigger, reply in responses.items():
            if trigger in lower_msg:
                await message.channel.send(reply)
                break

async def setup(bot):
    await bot.add_cog(Responses(bot))