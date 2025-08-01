import discord
from discord.ext import commands
import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Lista cogów (modułów)
initial_extensions = [
    "cogs.responses",
    "cogs.activity",
    "cogs.media_handler",
    "cogs.admin_tools",
    "cogs.gpt_chat",
    "cogs.tracker_stats",
    "cogs.link_guard",
    "cogs.caps_guard",
    "cogs.image_only_guard",
    "cogs.event_log",
    "cogs.mod_log",
    "cogs.division_server_status",
    "cogs.anna_dialogue",
    "cogs.anna_alerts",
    "cogs.anna_random_responses",
    "cogs.online_counter",
    "cogs.moderation",
    "cogs.help_command",
    "cogs.command_error_handler",
    "cogs.division_stats_scraper",
    "cogs.channel_mirror",
    "cogs.member_logger",
    "cogs.free_stuff",
    "cogs.poll",
    "cogs.event_dm",
]

async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"✅ Załadowano {extension}")
        except Exception as e:
            print(f"⚠️ Błąd ładowania {extension}: {e}")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

async def main():
    await load_extensions()
    await bot.start(config.TOKEN)

asyncio.run(main())