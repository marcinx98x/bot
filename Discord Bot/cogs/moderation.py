import discord
from discord.ext import commands

class Moderation(commands.Cog):  # ✅ zmieniono nazwę klasy
    def __init__(self, bot):
        self.bot = bot

    # BAN
    @commands.command(name="anna_ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Brak powodu. ANNA uznała to za wystarczające."):
        await member.ban(reason=reason)
        embed = discord.Embed(title="🛑 BAN ZAAKCEPTOWANY", color=discord.Color.dark_red())
        embed.add_field(name="Użytkownik", value=member.mention)
        embed.add_field(name="Powód", value=reason)
        embed.set_footer(text="Decyzja nieodwracalna. Wyrok zapadł.")
        await ctx.send(embed=embed)

    # KICK
    @commands.command(name="anna_kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Nie wykazano istotności obecności."):
        await member.kick(reason=reason)
        embed = discord.Embed(title="🚷 USUNIĘTO Z SYSTEMU", color=discord.Color.orange())
        embed.add_field(name="Użytkownik", value=member.mention)
        embed.add_field(name="Powód", value=reason)
        embed.set_footer(text="ANNA nie lubi nieefektywności.")
        await ctx.send(embed=embed)

    # CLEAR
    @commands.command(name="anna_clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"🧹 Wyczyściłam {amount} wiadomości. Ślady chaosu zredukowane.", delete_after=5)

    # MUTE
    @commands.command(name="anna_mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role)
        await ctx.send(f"🔇 {member.mention} został wyciszony. Cisza to luksus, który właśnie dostał.")

    # UNMUTE
    @commands.command(name="anna_unmute")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"🔊 {member.mention} odzyskał głos. ANNA będzie słuchać... z przymusem.")

    # WARN
    @commands.command(name="anna_warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Naruszenie estetyki interakcji."):
        embed = discord.Embed(title="⚠️ OSTRZEŻENIE SYSTEMOWE", color=discord.Color.gold())
        embed.add_field(name="Użytkownik", value=member.mention)
        embed.add_field(name="Powód", value=reason)
        embed.set_footer(text="Jeden krok bliżej do cienia bana.")
        await ctx.send(embed=embed)

    # SLOWMODE
    @commands.command(name="anna_slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, delay: int):
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f"🐢 Tryb wolny ustawiony na {delay} sekund. ANNA lubi przemyślane rozmowy.")

async def setup(bot):  # ✅ spójna z nazwą klasy
    await bot.add_cog(Moderation(bot))