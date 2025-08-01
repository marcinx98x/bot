from discord.ext import commands
import discord
from datetime import datetime

LOG_CHANNEL_ID = 1399767145000472646

class ModLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_log(self, action: str, target: discord.Member | discord.User, moderator: discord.Member | discord.User, reason: str = "Brak powodu"):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not channel:
            return

        is_punishment = action.lower() in ["ban", "mute", "timeout"]
        color = discord.Color.red() if is_punishment else discord.Color.green()

        embed = discord.Embed(
            title=f"{'🚨' if is_punishment else '✅'} {action.upper()}",
            description=(
                f"👤 **Użytkownik:** {target.mention} (`{target.id}`)\n"
                f"🛡️ **Moderator:** {moderator.mention} (`{moderator.id}`)\n"
                f"📄 **Powód:** {reason}"
            ),
            color=color,
            timestamp=datetime.utcnow()
        )
        embed.set_thumbnail(url=target.avatar.url if target.avatar else None)
        await channel.send(embed=embed)

    async def get_moderator_from_audit(self, guild: discord.Guild, action: discord.AuditLogAction, target_id: int):
        async for entry in guild.audit_logs(limit=5, action=action):
            if entry.target.id == target_id:
                return entry.user
        return guild.me  # fallback: bot jako wykonawca

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        moderator = await self.get_moderator_from_audit(guild, discord.AuditLogAction.ban, user.id)
        await self.send_log("Ban", user, moderator)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        moderator = await self.get_moderator_from_audit(guild, discord.AuditLogAction.unban, user.id)
        await self.send_log("Unban", user, moderator)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.timed_out_until != after.timed_out_until:
            guild = after.guild
            action = (
                "Timeout" if after.timed_out_until else "Timeout End"
            )
            audit_action = discord.AuditLogAction.member_update
            moderator = await self.get_moderator_from_audit(guild, audit_action, after.id)
            await self.send_log(action, after, moderator)

async def setup(bot):
    await bot.add_cog(ModLog(bot))