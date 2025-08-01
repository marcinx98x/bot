import discord
from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def poll(self, ctx, multiple: bool, question: str, *options):
        """
        Komenda do tworzenia głosowania.
        multiple: True/False – czy można głosować wielokrotnie
        question: Treść pytania
        options: Lista opcji (max 10)
        """

        if len(options) < 2 or len(options) > 10:
            await ctx.send("Podaj od 2 do 10 opcji do głosowania.")
            return

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        embed = discord.Embed(
            title="📊 Głosowanie",
            description=question,
            color=discord.Color.blurple()
        )

        for i, option in enumerate(options):
            embed.add_field(name=f"{emojis[i]} {option}", value="\u200b", inline=False)

        footer_text = "Możesz wybrać wiele odpowiedzi" if multiple else "Wybierz jedną odpowiedź"
        embed.set_footer(text=footer_text)

        poll_msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await poll_msg.add_reaction(emojis[i])

async def setup(bot):
    await bot.add_cog(Poll(bot))