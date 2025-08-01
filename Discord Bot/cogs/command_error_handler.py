import discord
from discord.ext import commands

class ANNACommandErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("📎 Brakuje argumentów. Czyżbyś stracił panowanie nad językiem? Wpisz `!pomoc` zanim ANNA wpisze Cię w rejestr nieudolności.")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("🔍 Komenda nieznana. ANNA nie rozpoznaje bełkotu. Sprawdź `!pomoc`.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("🔒 Brak uprawnień. ANNA nie ufa jednostkom bez kontroli dostępu.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚙️ Zły typ danych. ANNA nie toleruje niezgodności logicznych. Użyj `!pomoc`, jeśli kalkulacje przerastają Twoje możliwości.")
        else:
            await ctx.send("❗ Wystąpił nieoczekiwany błąd. ANNA analizuje... zalecam milczenie i wpisanie `!pomoc`.")

async def setup(bot):
    await bot.add_cog(ANNACommandErrors(bot))