from discord.ext import commands

class AdminTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Usunięto {amount} wiadomości 🧹", delete_after=5)

async def setup(bot):
    await bot.add_cog(AdminTools(bot))