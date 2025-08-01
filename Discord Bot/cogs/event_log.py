from discord.ext import commands
import discord
from datetime import datetime
import asyncio

LOG_CHANNEL_ID = 1399813990397382768

class EventLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, action, user, moderator, details, is_alert=True):
        color = discord.Color.red() if is_alert else discord.Color.green()
        embed = discord.Embed(
            title=f"{'🔴' if is_alert else '🟢'} {action}",
            description=(
                f"👤 **Użytkownik:** {user.mention} (`{user.id}`)\n"
                f"🛡️ **Wykonane przez:** {moderator.mention if moderator else 'Nieznane (Cień?)'}\n"
                f"📄 **Szczegóły:** {details}"
            ),
            color=color,
            timestamp=datetime.utcnow()
        )
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)
        return embed

    async def send_log(self, action, user, moderator=None, details="", is_alert=True):
        channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if channel:
            embed = self.build_embed(action, user, moderator, details, is_alert)
            await channel.send(embed=embed)
        else:
            print(f"[LOG ERROR] Nie znaleziono kanału o ID: {LOG_CHANNEL_ID}")

    @commands.command(name="dodajrole")
    @commands.has_permissions(manage_roles=True)
    async def dodaj_role_command(self, ctx, member: discord.Member, *, role: discord.Role):
        if role not in ctx.guild.roles:
            await ctx.send("❌ Nie znaleziono takiej roli na serwerze.")
            return
        try:
            await member.add_roles(role)
            await self.send_log(
                "Dodanie Roli (komenda)",
                member,
                ctx.author,
                f"✅ Ręcznie dodano rolę: **{role.name}** przez {ctx.author.display_name}.",
                is_alert=False
            )
            await ctx.send(f"🔧 Rola **{role.name}** została dodana użytkownikowi {member.mention}.")
        except discord.Forbidden:
            await ctx.send("❌ Bot nie ma uprawnień do nadania tej roli.")
        except Exception as e:
            await ctx.send("❌ Wystąpił błąd przy dodawaniu roli.")
            print(f"[ROLE ERROR] {e}")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            await self.send_log(
                "Zmiana Nicku",
                after,
                None,
                f"**Z:** {before.nick or before.name}\n**Na:** {after.nick or after.name}",
                is_alert=True
            )

        added_roles = [r for r in after.roles if r not in before.roles]
        removed_roles = [r for r in before.roles if r not in after.roles]

        moderator = None
        if added_roles or removed_roles:
            await asyncio.sleep(3)
            try:
                async for entry in after.guild.audit_logs(limit=25):
                    if entry.action != discord.AuditLogAction.member_role_update:
                        continue
                    if entry.target.id != after.id:
                        continue
                    if (datetime.utcnow() - entry.created_at).total_seconds() > 20:
                        continue
                    for change in entry.changes:
                        if change.key == "roles":
                            before_ids = {r.id for r in change.before or []}
                            after_ids = {r.id for r in change.after or []}
                            added_match = any(r.id not in before_ids for r in added_roles)
                            removed_match = any(r.id not in after_ids for r in removed_roles)
                            if added_match or removed_match:
                                moderator = entry.user
                                break
                    if moderator:
                        break
            except Exception as e:
                print(f"[AUDYT ERROR] {e}")

            for role in added_roles:
                await self.send_log(
                    "Dodanie Roli",
                    after,
                    moderator,
                    f"✅ Dodano rolę: **{role.name}**",
                    is_alert=False
                )

            for role in removed_roles:
                await self.send_log(
                    "Usunięcie Roli",
                    after,
                    moderator,
                    f"❌ Usunięto rolę: **{role.name}**",
                    is_alert=True
                )

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            await self.send_log(
                "Wejście na Kanał Głosowy",
                member,
                None,
                f"**Kanał:** {after.channel.name}",
                is_alert=False
            )
        elif before.channel and after.channel and before.channel != after.channel:
            await self.send_log(
                "Zmiana Kanału Głosowego",
                member,
                None,
                f"**Z:** {before.channel.name}\n**Na:** {after.channel.name}",
                is_alert=False
            )
        elif before.channel and after.channel is None:
            await self.send_log(
                "Wyjście z Kanału Głosowego",
                member,
                None,
                f"**Kanał:** {before.channel.name}",
                is_alert=True
            )

async def setup(bot):
    await bot.add_cog(EventLog(bot))