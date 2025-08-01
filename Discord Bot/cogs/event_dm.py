import discord, json, asyncio
from discord.ext import commands, tasks
from datetime import datetime, timedelta

EVENT_FILE = "event_data.json"

class EventView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__(timeout=None)
        self.author_id = author_id
        self.roles = {
            "TANK": [],
            "HEALLER": [],
            "DPS": [],
            "OCZEKUJĄCY": [],
            "NIE WIEM": [],
            "NIE": []
        }

    async def handle_rsvp(self, interaction, role):
        username = interaction.user.display_name

        for r in self.roles:
            if username in self.roles[r]:
                self.roles[r].remove(username)
        self.roles[role].append(username)
        await self.save_data()
        await self.update_embed(interaction)

        await interaction.response.send_message(f"Zapisano jako **{role}**!", ephemeral=True)

    async def save_data(self):
        with open(EVENT_FILE, "w") as f:
            json.dump(self.roles, f, indent=2)

    async def update_embed(self, interaction):
        embed = discord.Embed(
            title="📆 Raid Event",
            description="Wybierz swoją rolę, zobacz kto dołączył i przygotuj się!",
            color=discord.Color.dark_gray()
        )
        for role, users in self.roles.items():
            embed.add_field(
                name=f"{role} ({len(users)})",
                value="\n".join(users) if users else "Brak zapisów",
                inline=True
            )
        embed.set_footer(text=f"Utworzone przez: {interaction.guild.get_member(self.author_id).display_name}")
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="🛡️ TANK", style=discord.ButtonStyle.green)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "TANK")

    @discord.ui.button(label="💉 HEALLER", style=discord.ButtonStyle.red)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "HEALLER")

    @discord.ui.button(label="⚔️ DPS", style=discord.ButtonStyle.blurple)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "DPS")

    @discord.ui.button(label="🕒 OCZEKUJĄCY", style=discord.ButtonStyle.gray)
    async def oczekujacy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "OCZEKUJĄCY")

    @discord.ui.button(label="❔ NIE WIEM", style=discord.ButtonStyle.gray)
    async def nie_wiem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "NIE WIEM")

    @discord.ui.button(label="❌ NIE", style=discord.ButtonStyle.gray)
    async def nie(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.handle_rsvp(interaction, "NIE")


class EventDM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder_sent = False
        self.event_time = None

    @commands.command(name="event")
    async def create_event(self, ctx):
        view = EventView(author_id=ctx.author.id)
        embed = discord.Embed(
            title="📆 Raid Event",
            description="Kliknij swoją rolę poniżej i zapisz się na wydarzenie!",
            color=discord.Color.dark_gray()
        )
        embed.add_field(name="🕒 Czas", value="Sobota, 3 sierpnia 2025\n20:30 – 23:00\n⏳ Przypomnienie 15 minut przed")
        embed.set_footer(text=f"Utworzone przez: {ctx.author.display_name}")

        msg = await ctx.send(embed=embed, view=view)
        self.event_time = datetime.now() + timedelta(hours=2)  # przykład
        self.event_reminder.start(ctx.channel, msg)

    @tasks.loop(minutes=1)
    async def event_reminder(self, channel, msg):
        if self.event_time and not self.reminder_sent:
            now = datetime.now()
            if now >= self.event_time - timedelta(minutes=15):
                await channel.send("⏰ Przypomnienie: Wydarzenie zaczyna się za **15 minut**!")
                self.reminder_sent = True
                self.event_reminder.stop()

    @commands.command(name="delete_event")
    async def delete_event(self, ctx):
        try:
            open(EVENT_FILE, "w").close()
            await ctx.send("🗑️ Wydarzenie zostało usunięte.")
        except:
            await ctx.send("Coś poszło nie tak podczas usuwania wydarzenia.")

async def setup(bot):
    await bot.add_cog(EventDM(bot))