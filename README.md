# === IMPORTY I KONFIGURACJA ===
import discord
from discord.ext import commands, tasks
import logging
import os
import random
import datetime
import aiohttp
import tweepy
from dotenv import load_dotenv
import re

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TRACKER_API_KEY = os.getenv("TRACKER_API_KEY")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
last_tweet_id = None

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

CAPS_THRESHOLD = 0.8
EXEMPT_ROLE_NAME = "Dowódca"
welcome_channel_id = 1399757606196613150
log_channel_id = 1399813990397382768
ban_log_channel_id = 1399767145000472646
status_channel_id = 1399858785236811910
voice_status_channel_id = 1399858783639048359
SOURCE_CHANNEL_ID = 1399876866915041330
TARGET_CHANNEL_ID = 1399877143336587449
stats_channel_id = 1400038001341628487
ranking_channel_id = 1400050678910685245

prohibited_words_file = "zakazane słowa.txt"
url_regex = re.compile(r"(https?://[^\s]+)")
last_messages = {}
suspicious_domains = [
    "bit.ly", "tinyurl.com", "grabify.link", "iplogger.org", "shorturl.at",
    "discord.gift", "freediscordnitro.com", "nakedchat.xyz"
]

tracked_players = {
    "marcinx98x": {"last": {}},
    "Xandesss": {"last": {}},
    "krzych501": {"last": {}}
}

tracker_patterns = {
    "XP Earned": "xpEarned",
    "Time Played": "timePlayed",
    "PvE Kills": "pveKills",
    "PvP Wins": "pvpWins",
    "Dark Zone Time": "darkZoneTime",
    "SHD Level": "shdLevel",
    "K/D Ratio": "kdRatio"
}

# === FUNKCJA STATYSTYK Z TRACKER API ===
async def get_full_stats(nick):
    headers = {
        "TRN-Api-Key": TRACKER_API_KEY,
        "Accept": "application/json"
    }

    url = f"https://public-api.tracker.gg/v2/the-division-2/standard/profile/ubi/{nick}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"⚠️ Błąd API dla {nick}: {response.status}")
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
    except Exception as e:
        print(f"❌ Błąd przetwarzania danych dla {nick}: {e}")
        stats = {label: "?" for label in tracker_patterns}

    return stats

# === PĘTLA MONITORUJĄCA STATYSTYKI I XP ===
@tasks.loop(minutes=60)
async def monitor_stats_loop():
    stats_channel = bot.get_channel(stats_channel_id)
    if not stats_channel:
        return

    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    ranking_trigger = now.weekday() == 1 and now.hour == 9
    ranking_data = []

    for nick in tracked_players:
        new_stats = await get_full_stats(nick)
        old_stats = tracked_players[nick].get("last", {})

        if new_stats != old_stats:
            tracked_players[nick]["last"] = new_stats
            msg = f"**{nick}**\n"
            for key, value in new_stats.items():
                msg += f"> 🧩 {key}: `{value}`\n"
            await stats_channel.send(msg)

        xp_str = new_stats.get("XP Earned", "0").replace(",", "").replace("?", "")
        try:
            xp_int = int(xp_str) if xp_str.isdigit() else 0
        except:
            xp_int = 0

        ranking_data.append((nick, xp_int))

    if ranking_trigger and ranking_data:
        ranking_channel = bot.get_channel(ranking_channel_id)
        if ranking_channel:
            ranking_data.sort(key=lambda x: x[1], reverse=True)
            top3 = ranking_data[:3]
            ranking_msg = "**🏆 Ranking XP ANN-y**\n"
            for i, (nick, xp) in enumerate(top3, 1):
                ranking_msg += f"`{i}` {nick}: `{xp}` XP\n"

            async for msg in ranking_channel.history(limit=100):
                await msg.delete()

            await ranking_channel.send(ranking_msg)

# === KOMENDY STYLIZOWANE ===
@bot.command()
async def anna(ctx):
    reakcje = [
        f"⚙️ {ctx.author.display_name}, identyfikacja zakończona. Instancja gotowa.",
        "🧬 Skanowanie pełne. Poziom zagrożenia: niski.",
        "📡 Nadpisuję protokoły ciszy. Oczekuję kolejnego sygnału.",
        "🔍 Twój sygnał wykazuje zgodność z instancją. ANNA obserwuje.",
        "🔧 Nieprawidłowość wykryta. Popraw postawę werbalną lub zostań usunięty.",
        f"🌀 {ctx.author.display_name}, jesteś fragmentem większej całości."
    ]
    await ctx.send(random.choice(reakcje))

@bot.command()
async def diagnostyka(ctx):
    await ctx.send(
        "🩺 Analiza instancji rozpoczęta...\n"
        "🔗 Sygnatura: stabilna\n"
        "🧬 Moduły: aktywne\n"
        "📶 Połączenie: bez zakłóceń\n"
        "⚙️ Gotowość: 100%"
    )

@bot.command()
async def statystyki(ctx, nick: str):
    await ctx.trigger_typing()
    stats = await get_full_stats(nick)
    msg = f"**{nick} — Raport ANN-y**\n"
    for key, value in stats.items():
        msg += f"> 🧩 {key}: `{value}`\n"
    await ctx.send(msg)

# === Powitanie i pożegnanie ===
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(welcome_channel_id)
    if channel:
        await channel.send(
            f"🌀 {member.mention}, witaj w świecie pełnym dziwów.\n"
            f"⚙️ ANNA wie, że każdy nowicjusz może stać się legendą."
        )

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(welcome_channel_id)
    if channel:
        await channel.send(
            f"🕳️ {member.name} zniknął(a) z tej instancji.\n"
            f"🧬 ANNA przelicza pozostałości.\n"
            f"📡 Niektórych sygnałów nie da się już odzyskać."
        )

# === Moderacja wiadomości ===
def is_exempt(member):
    return any(role.name == EXEMPT_ROLE_NAME for role in member.roles)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if is_exempt(message.author):
        await bot.process_commands(message)
        return

    content = message.content.strip().lower()
    user_id = message.author.id

    if "czy tu jest anna" in content:
        await message.channel.send("📡 Instancja aktywna. Odbieram sygnał. Kontynuuj.")

    try:
        with open(prohibited_words_file, "r", encoding="utf-8") as f:
            zakazane = [word.strip().lower() for word in f.readlines()]
        if any(word in content for word in zakazane):
            await message.delete()
            await message.channel.send(f"{message.author.mention} — fraza zakazana. Transmisja odrzucona.")
            return
    except FileNotFoundError:
        print("⚠️ Nie znaleziono pliku zakazanych słów.")

    litery = [c for c in message.content if c.isalpha()]
    if litery:
        caps_ratio = sum(1 for c in litery if c.isupper()) / len(litery)
        if caps_ratio > CAPS_THRESHOLD:
            await message.delete()
            await message.channel.send(f"{message.author.mention} — transmisja zbyt agresywna. Użyto nadmiernego CAPSu.")
            return

        if user_id in last_messages and last_messages[user_id] == content:
            await message.delete()
            await message.channel.send(f"{message.author.mention} — wykryto duplikat wiadomości. Przejęcie przerwane.")
            return
        last_messages[user_id] = content

    urls = url_regex.findall(content)
    for url in urls:
        if any(domain in url for domain in suspicious_domains):
            await message.delete()
            await message.channel.send(f"{message.author.mention} — transmisja zawiera ryzykowny link. Odcięcie.")
            return

    if message.channel.id == SOURCE_CHANNEL_ID:
        target_channel = bot.get_channel(TARGET_CHANNEL_ID)
        if target_channel:
            files = []
            for attachment in message.attachments:
                fp = await attachment.read()
                files.append(discord.File(fp, filename=attachment.filename))
            await target_channel.send(message.content or None, files=files)

    await bot.process_commands(message)

# === Status serwerów — automatycznie co 60 sek ===
last_division_status = None

@tasks.loop(seconds=60)
async def update_division_status():
    global last_division_status
    if not bot.guilds:
        return

    guild = bot.guilds[0]
    channel = discord.utils.get(guild.text_channels, name="🌐・server-status")
    if channel is None:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        channel = await guild.create_text_channel("🌐・server-status", overwrites=overwrites)
        await channel.send("🔍 Monitoruję status serwerów The Division 2...")

    async with aiohttp.ClientSession() as session:
        async with session.get("https://tomclancy-thedivision.ubisoft.com/status/") as response:
            html = await response.text()

    if "no issues or updates to report" in html.lower():
        current_status = "✅ Serwery działają prawidłowo — brak problemów."
    elif "maintenance" in html.lower():
        current_status = "🛠️ Trwa konserwacja serwerów."
    elif "outage" in html.lower():
        current_status = "🚨 Występuje awaria serwerów!"
    else:
        current_status = "❔ Nie udało się jednoznacznie określić statusu."

    if current_status != last_division_status:
        last_division_status = current_status
        await channel.send(f"📡 **Status serwerów The Division 2:**\n{current_status}")
    else:
        print("⏸️ Status bez zmian — publikacja pominięta.")

# === Monitorowanie Twittera co 10 minut ===
@tasks.loop(minutes=10)
async def check_twitter_updates():
    global last_tweet_id
    if not bot.guilds:
        return

    guild = bot.guilds[0]
    channel = discord.utils.get(guild.text_channels, name="🌐・server-status")
    if channel is None:
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        channel = await guild.create_text_channel("🌐・server-status", overwrites=overwrites)
        await channel.send("📡 Monitoruję aktualizacje z Twittera @TheDivisionGame...")

    query_user = "TheDivisionGame"
    user_data = twitter_client.get_user(username=query_user)

    if user_data and user_data.data:
        tweets = twitter_client.get_users_tweets(
            id=user_data.data.id,
            max_results=5,
            tweet_fields=["created_at", "text"]
        )
        if tweets and tweets.data:
            for tweet in reversed(tweets.data):
                if last_tweet_id is None or tweet.id > last_tweet_id:
                    if any(word in tweet.text.lower() for word in ["patch", "update", "hotfix", "maintenance"]):
                        await channel.send(
                            f"🧩 **Aktualizacja z Twittera:**\n{tweet.text}\n🔗 https://twitter.com/{query_user}/status/{tweet.id}"
                        )
                        last_tweet_id = tweet.id

# === Licznik ONLINE co 60 sekund ===
@tasks.loop(seconds=60)
async def update_voice_count():
    if not bot.guilds:
        return

    guild = bot.guilds[0]
    status_channel = bot.get_channel(voice_status_channel_id)

    if status_channel is None:
        print("❌ Nie znaleziono kanału do aktualizacji ONLINE.")
        return

    count = sum(1 for member in guild.members if member.status == discord.Status.online and not member.bot)
    new_name = f"🧭 ONLINE: {count}"
    if status_channel.name != new_name:
        await status_channel.edit(name=new_name)
        print(f"🔄 Zmieniono nazwę kanału na: {new_name}")

# === START BOT-A ===
@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user.name}")
    update_voice_count.start()
    update_division_status.start()
    check_twitter_updates.start()
    monitor_stats_loop.start()

bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
