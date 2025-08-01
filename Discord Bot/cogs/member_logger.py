import discord
from discord.ext import commands
from datetime import datetime

class MemberLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel_id = 1399757606196613150

    def format_date(self):
        return datetime.now().strftime("%d.%m.%Y • %H:%M")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            embed = discord.Embed(
                title="🎉 Nowe przybycie!",
                description=f"{member.mention} dołączył do serwera.",
                color=0x00ff00
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
            embed.set_footer(text=f"Nazwa: {member.display_name} • Data dołączenia: {self.format_date()}")

            await channel.send(embed=embed)

        try:
            dm_embed = discord.Embed(
                description="👋 Witaj na serwerze! Cieszymy się, że jesteś z nami.",
                color=0x00ff00
            )
            dm_embed.set_footer(text=f"Dołączyłeś: {self.format_date()}")
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            print(f"❌ Nie udało się wysłać wiadomości DM do {member.display_name}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(self.log_channel_id)
        if channel:
            embed = discord.Embed(
                title="📤 Wyjście z serwera",
                description=f"{member.display_name} opuścił serwer.",
                color=0xff0000
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else discord.Embed.Empty)
            embed.set_footer(text=f"Pożegnanie od ANNA.exe • Data opuszczenia: {self.format_date()}")

            await channel.send(embed=embed)

        try:
            dm_embed = discord.Embed(
                description="💌 Dziękujemy, że byłeś z nami. Do zobaczenia!",
                color=0xff0000
            )
            dm_embed.set_footer(text=f"Opuszczenie: {self.format_date()}")
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            print(f"❌ Nie udało się wysłać wiadomości pożegnalnej DM do {member.display_name}")

# 🔌 Setup rozszerzenia
async def setup(bot):
    await bot.add_cog(MemberLogger(bot))