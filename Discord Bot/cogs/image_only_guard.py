from discord.ext import commands
import discord
import re

URL_REGEX = re.compile(r"(https?://[^\s]+)")

# Tu dodajesz ID kanałów, które mają być chronione
PROTECTED_CHANNELS = [
    1400430912147292271,  # przykład: kanał #memy
    1400194390869414051,  # przykład: kanał #screeny
]

class ImageOnlyGuard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_image_or_link(self, message: discord.Message):
        has_attachment = len(message.attachments) > 0
        has_link = bool(URL_REGEX.search(message.content))
        return has_attachment or has_link

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id in PROTECTED_CHANNELS:
            if not self.is_image_or_link(message):
                await message.delete()
                warning = await message.channel.send(
                    f"{message.author.mention}, ten kanał akceptuje tylko obrazki lub linki! 🚫"
                )
                await warning.delete(delay=5)

async def setup(bot):
    await bot.add_cog(ImageOnlyGuard(bot))