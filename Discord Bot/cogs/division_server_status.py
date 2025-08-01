from discord.ext import commands, tasks
import discord
import aiohttp

STATUS_CHANNEL_ID = 1399858785236811910
DIVISION_STATUS_URL = "https://tomclancy-thedivision.ubisoft.com/status/"

class DivisionStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_status = None
        self.check_status.start()

    def cog_unload(self):
        self.check_status.cancel()

    def parse_status(self, html):
        html = html.lower()
        if "no issues or updates" in html:
            return "OK"
        elif "maintenance" in html or "outage" in html:
            return "PROBLEM"
        else:
            return "UNKNOWN"

    @tasks.loop(minutes=5)
    async def check_status(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(DIVISION_STATUS_URL) as response:
                html = await response.text()

        current_status = self.parse_status(html)

        if current_status != self.last_status:
            self.last_status = current_status
            await self.post_status_embed(current_status)

    async def post_status_embed(self, status):
        channel = self.bot.get_channel(STATUS_CHANNEL_ID)
        if not channel:
            return

        if status == "OK":
            embed = discord.Embed(
                title="✅ Serwery The Division działają poprawnie",
                description="Brak zgłoszonych problemów.",
                color=discord.Color.green()
            )
        elif status == "PROBLEM":
            embed = discord.Embed(
                title="🚨 Problemy z serwerami The Division",
                description="Serwery mogą być niedostępne lub w trakcie konserwacji.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="❓ Nieznany status serwera",
                description="Nie udało się jednoznacznie określić statusu. Sprawdź ręcznie:\n[Ubisoft Status](https://tomclancy-thedivision.ubisoft.com/status/)",
                color=discord.Color.orange()
            )

        embed.set_footer(text="Status sprawdzany co 5 minut.")
        await channel.send(embed=embed)

    @commands.command(name="division")
    async def division_status_command(self, ctx):
        await ctx.send("⏳ Sprawdzam aktualny status serwera...")

        async with aiohttp.ClientSession() as session:
            async with session.get(DIVISION_STATUS_URL) as response:
                html = await response.text()

        status = self.parse_status(html)
        await self.post_status_embed(status)

async def setup(bot):
    await bot.add_cog(DivisionStatus(bot))