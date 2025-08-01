import discord
from discord.ext import commands

class ANNAHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pomoc")
    async def help_command(self, ctx):
        embed = discord.Embed(title="📖 CENTRUM OPERACYJNE ANNY", color=discord.Color.teal())
        embed.set_footer(text="Pomoc techniczna? ANNA oceni, czy zasługujesz.")

        # Systemowe
        embed.add_field(name="🔔 !anna_alert [status]", value="Zwraca alert systemowy w zależności od statusu SHD. Statusy: maintenance, outage, operational, degraded, echo_detected, itd.", inline=False)
        embed.add_field(name="🎲 !anna_rand", value="Losowa odpowiedź ANNY. Sarkastyczna. Statystycznie nieprzydatna.", inline=False)
        embed.add_field(name="🧭 Kanał 'Online:'", value="Automatyczny licznik aktywnych użytkowników, aktualizowany co minutę.", inline=False)

        # Moderacyjne
        embed.add_field(name="🛡️ !anna_ban [@user] [powód]", value="Banuje użytkownika. Ostateczna decyzja.", inline=False)
        embed.add_field(name="🚷 !anna_kick [@user] [powód]", value="Wyrzuca delikwenta. Powód: ANNA wie najlepiej.", inline=False)
        embed.add_field(name="🧹 !anna_clear [liczba]", value="Usuwa określoną liczbę wiadomości. Przywraca porządek.", inline=False)
        embed.add_field(name="🔇 !anna_mute [@user]", value="Wycisza użytkownika. Cisza to świętość.", inline=False)
        embed.add_field(name="🔊 !anna_unmute [@user]", value="Przywraca głos. ANNA będzie słuchać... z przymusem.", inline=False)
        embed.add_field(name="⚠️ !anna_warn [@user] [powód]", value="Wysyła ostrzeżenie. Zapisz to w swoim emocjonalnym systemie.", inline=False)
        embed.add_field(name="🐢 !anna_slowmode [sekundy]", value="Ustawia tryb wolny na kanale. Dla przemyślanych jednostek.", inline=False)

        # Głosowania i inne
        embed.add_field(name="🗳️ !poll <True/False> <pytanie> <opcja1> <opcja2> ...", value="Tworzy głosowanie. `True` = wiele głosów, `False` = jeden głos. ANNA monitoruje wynik.", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ANNAHelp(bot))