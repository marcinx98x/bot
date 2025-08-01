from discord.ext import commands, tasks
import aiohttp
import datetime
import config  # zakładam, że masz tam TRACKER_API_KEY
import re

tracker_patterns = {
    "XP Earned": "xpEarned",
    "Time Played": "timePlayed",
    "PvE Kills": "pveKills",
    "PvP Wins": "pvpWins",
    "Dark Zone Time": "darkZoneTime",
    "SHD Level": "shdLevel",
    "K/D Ratio": "kdRatio"
}

class TrackerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_full_stats(self, nick):
        headers = {
            "TRN-Api-Key": config.TRACKER_API_KEY,
            "Accept": "application/json"
        }
        url = f"https://public-api.tracker.gg/v2/the-division-2/standard/profile/ubi/{nick}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    return {label: "?" for label in tracker_patterns}
                data = await response.json()

        stats = {}
        try:
            segments = data.get("data", {}).get("segments", [])
            for segment in segments:
                stats_obj = segment.get("stats", {})
                for label in tracker_patterns:
                    field = tracker_patterns[label]
                    value = stats_obj.get(field, {}).get("value", "?")
                    stats[label] = str(value)
        except Exception:
            stats = {label: "?" for label in tracker_patterns}

        return stats

    @commands.command(name="staty")
    async def show_stats(self, ctx, nick: str):
        stats = await self.get_full_stats(nick)
        embed = discord.Embed(title=f"Statystyki dla {nick}", color=discord.Color.orange())
        for label, value in stats.items():
            embed.add_field(name=label, value=value, inline=True)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TrackerStats(bot))