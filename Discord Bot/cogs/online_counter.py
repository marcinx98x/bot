import discord
from discord.ext import tasks, commands

class OnlineCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1400447191037906987  # ID kanału głosowego
        self.guild_id = 1399661646674395176  # <--- Zamień na ID Twojego serwera
        self.update_online_count.start()

    def cog_unload(self):
        self.update_online_count.cancel()

    @tasks.loop(minutes=1)
    async def update_online_count(self):
        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return

        online_members = [
            member for member in guild.members
            if member.status in (discord.Status.online, discord.Status.idle, discord.Status.dnd)
            and not member.bot
        ]

        channel = guild.get_channel(self.channel_id)
        if channel:
            new_name = f"🧭 Online: {len(online_members)}"
            if channel.name != new_name:
                await channel.edit(name=new_name)

    @update_online_count.before_loop
    async def before_update_online_count(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(OnlineCounter(bot))