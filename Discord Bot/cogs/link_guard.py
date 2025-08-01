from discord.ext import commands
import re

SUSPICIOUS_DOMAINS = [
    "bit.ly", "tinyurl.com", "grabify.link", "iplogger.org",
    "shorturl.at", "discord.gift", "freediscordnitro.com", "nakedchat.xyz"
]

URL_REGEX = re.compile(r"(https?://[^\s]+)")

class LinkGuard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        urls = URL_REGEX.findall(message.content)
        for url in urls:
            if any(domain in url for domain in SUSPICIOUS_DOMAINS):
                await message.delete()
                return  # Nie wysyłamy żadnego komunikatu

async def setup(bot):
    await bot.add_cog(LinkGuard(bot))