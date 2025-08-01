import discord
from discord.ext import commands
import requests

class DivisionStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = "5b13e0be-b31d-461a-8be6-9673db01c7e0"
        self.nick_list = ["Xandess", "marcinx98x", "krzych501"]
        self.channel_id = 1400038001341628487

    @commands.command()
    async def divisionstats(self, ctx):
        channel = self.bot.get_channel(self.channel_id)
        headers = {"TRN-Api-Key": self.api_key}

        for nick in self.nick_list:
            url = f"https://public-api.tracker.gg/v2/division-2/standard/profile/ubi/{nick}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                await channel.send(f"❌ Nie udało się pobrać danych dla `{nick}`")
                continue

            data = response.json()
            stats = data["data"]["segments"][0]["stats"]

            shd = stats.get("shdLevel", {}).get("displayValue", "Brak")
            time_played = stats.get("timePlayed", {}).get("displayValue", "Brak")
            kills_npc = stats.get("killsNpc", {}).get("displayValue", "Brak")
            kills_pvp = stats.get("killsPvP", {}).get("displayValue", "Brak")

            embed = discord.Embed(title=f"📍 Profil Division 2: `{nick}`", color=0x00ff88)
            embed.add_field(name="SHD", value=shd, inline=True)
            embed.add_field(name="Czas gry", value=time_played, inline=True)
            embed.add_field(name="PvE", value=f"{kills_npc} NPC", inline=False)
            embed.add_field(name="PvP", value=f"{kills_pvp} graczy", inline=False)
            embed.set_footer(text="Tracker.gg API • ANNA approved 😏")

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DivisionStats(bot))