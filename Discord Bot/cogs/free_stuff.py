import discord
from discord.ext import commands

class FreeStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.source_channel_id = 1400494569745023048  # Kanał źródłowy
        self.target_channel_id = 1400489307776749729  # Kanał docelowy

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignoruj wiadomości spoza źródłowego kanału i od botów
        if message.channel.id != self.source_channel_id or message.author.bot:
            return

        target_channel = self.bot.get_channel(self.target_channel_id)
        if not target_channel:
            print("❌ Nie znaleziono kanału docelowego.")
            return

        # 📝 Zbuduj wiadomość
        content = f"\n{message.content}"

        # 🖼️ Dodaj załączniki, jeśli są
        if message.attachments:
            files = []
            for attachment in message.attachments:
                file = await attachment.to_file()
                files.append(file)
            await target_channel.send(content, files=files)
        else:
            await target_channel.send(content)

async def setup(bot):
    await bot.add_cog(FreeStuff(bot))