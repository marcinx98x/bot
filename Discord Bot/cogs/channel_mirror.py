import discord
from discord.ext import commands

class ChannelMirror(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.source_channel_id = 1399876866915041330  # Kanał źródłowy
        self.target_channel_id = 1399877143336587449  # Kanał docelowy

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

# 🔌 Setup dla rozszerzenia
async def setup(bot):
    await bot.add_cog(ChannelMirror(bot))