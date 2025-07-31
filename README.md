import discord
from discord.ext import commands, tasks
import logging
import os
import random
import datetime  # 🔧 FIX: import datetime używany w voice status
import aiohttp
import tweepy
from datetime import datetime  # zostaje — używany w powitaniu
import pytz
from dotenv import load_dotenv
import asyncio
import re  # ✔️ Używany przy filtrowaniu URLi

# === Załaduj zmienne środowiskowe ===
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# === Logger ===
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# === Twitter klient ===
twitter_client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
last_tweet_id = None

# === Intencje i bot ===
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === Flagi ===
media_only_channels = set()

# === Stałe ===
CAPS_THRESHOLD = 0.8
EXEMPT_ROLE_NAME = "Dowódca"
welcome_channel_id = 1399757606196613150
log_channel_id = 1399813990397382768
ban_log_channel_id = 1399767145000472646
status_channel_id = 1399858785236811910
voice_status_channel_id = 1399858783639048359
SOURCE_CHANNEL_ID = 1399876866915041330
TARGET_CHANNEL_ID = 1399877143336587449
prohibited_words_file = "zakazane słowa.txt"
url_regex = re.compile(r"(https?://[^\s]+)")
last_messages = {}
suspicious_domains = [
    "bit.ly", "tinyurl.com", "grabify.link", "iplogger.org", "shorturl.at",
    "discord.gift", "freediscordnitro.com", "nakedchat.xyz"
]

# === Styl ANN-y ===
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

# === Pomocnicze ===
def is_exempt(member):
    return any(role.name == EXEMPT_ROLE_NAME for role in member.roles)

# === Moderacja wiadomości ===
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
            await message.channel.send(
                f"{message.author.mention} — transmisja zbyt agresywna. Użyto nadmiernego CAPSu.")
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

# === Powitanie i pożegnanie ===
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="kanał-operacyjny")
    now = datetime.now(pytz.timezone('Europe/Warsaw'))
    hour = now.hour

    if 6 <= hour < 12:
        anna_greeting = "Poranny skan zakończony. Agent wykryty w świecie przed kawą ☕"
    elif 12 <= hour < 18:
        anna_greeting = "Popołudniowy protokół aktywowany. Agent wkroczył w godzinę operacyjną 🕶️"
    elif 18 <= hour < 22:
        anna_greeting = "Wieczorny tryb aktywacji. Czas na strategie i sabotaż 🌒"
    else:
        anna_greeting = "Tryb nocny online. ANNA czuwa. Ty też powinieneś. 😴"

    public_welcome = f"""
🛡️ Agent <@{member.id}> wykryty na kanale operacyjnym!
{anna_greeting}

Serwer WYBAWICIELE [WBE] aktywował protokół powitalny.
🆕 Nowy rekrut na pokładzie — rozpocznij asymilację.

🔍 *Wskazówka: ANNA nie zapomina. Nigdy.*
"""
    await channel.send(public_welcome)

    try:
        dm_message = f"""
👁️ Witaj, agencie <@{member.id}>.

Twoje wejście zostało zauważone przez protokół ANNY.
Serwer WYBAWICIELE [WBE] rozpoczął proces asymilacji.

🧠 *Zasady interakcji:*
1️⃣ Sprawdź zakładki z informacjami.
2️⃣ Nie zapomnij: ANNA widzi więcej, niż ci się wydaje.

Witaj w operacji narracyjnej. Przetrwaj, a może zostaniesz legendą.
        """
        await member.send(dm_message)
    except discord.errors.Forbidden:
        print(f"Nie mogę wysłać DM do {member.name} — użytkownik może mieć zablokowane wiadomości.")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(welcome_channel_id)
    if channel:
        await channel.send(
            f"🕳️ {member.name} zniknął(a) z tej instancji.\n"
            f"🧬 ANNA przelicza pozostałości.\n"
            f"📡 Niektórych sygnałów nie da się już odzyskać."
        )

@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel(log_channel_id)
    if channel:
        await channel.send("🧬 Rewizja danych osobowych zakończona. Nowe sygnatury przyjęte.")

@bot.event
async def on_user_update(before, after):
    channel = bot.get_channel(log_channel_id)
    if channel:
        zmiany = []
        if before.name != after.name:
            zmiany.append(f"| Zmiana nazwy: `{before.name}` ➜ `{after.name}`")
        if before.avatar != after.avatar:
            zmiany.append(f"| Zmiana avatara dla: `{after.name}`")
        if zmiany:
            await channel.send("📄 Aktualizacja profilu:\n" + "\n".join(zmiany).replace("📄", "|"))

@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(log_channel_id)
    if channel and message.content:
        await channel.send(
            f"| Usunięta wiadomość od **{message.author.display_name}** na kanale **#{message.channel.name}**:\n```\n{message.content}\n```"
        )

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel(log_channel_id)
    if channel and before.content != after.content:
        await channel.send(
            f"| Edytowana wiadomość od **{before.author.display_name}** na kanale **#{before.channel.name}**:\n"
            f"| Przed:\n```\n{before.content}\n```\n| Po:\n```\n{after.content}\n```"
        )

@bot.event
async def on_voice_state_update(member, before, after):
    channel = bot.get_channel(log_channel_id)
    if not channel or member.bot:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 🔧 FIX: poprawiono datetime

    if before.channel is None and after.channel is not None:
        await channel.send(
            f"| [{timestamp}] Połączenie — **{member.display_name}** dołączył do kanału: **{after.channel.name}**."
        )
    elif before.channel is not None and after.channel is None:
        await channel.send(
            f"| [{timestamp}] Rozłączenie — **{member.display_name}** opuścił kanał: **{before.channel.name}**."
        )
    elif before.channel != after.channel:
        await channel.send(
            f"| [{timestamp}] Przemieszczenie — **{member.display_name}** zmienił kanał z **{before.channel.name}** na **{after.channel.name}**."
        )

# === Logowanie banów ===
@bot.event
async def on_member_ban(guild, user):
    channel = bot.get_channel(ban_log_channel_id)
    if channel:
        await channel.send(
            f"| Użytkownik **{user.name}** został zbanowany na serwerze **{guild.name}**.\n"
            f"| Konto oznaczone jako niekompatybilne."
        )

@bot.event
async def on_member_unban(guild, user):
    channel = bot.get_channel(ban_log_channel_id)
    if channel:
        await channel.send(
            f"| Użytkownik **{user.name}** został odbanowany na serwerze **{guild.name}**.\n"
            f"| Dostęp przywrócony — obserwacja aktywna."
        )

# === Komenda testowa ===
@bot.command()
async def cześć(ctx):
    await ctx.send(f"Cześć {ctx.author.mention}!")

@bot.command()
async def statusdivision(ctx):
    """📡 Publikuje status serwerów The Division 2 na dedykowanym kanale."""
    channel = bot.get_channel(status_channel_id)
    if channel is None:
        await ctx.send("❌ Nie mogę znaleźć kanału do publikacji statusu.")
        return

    async with aiohttp.ClientSession() as session:
        try:  # 🔧 FIX: dodano obsługę błędów
            async with session.get("https://tomclancy-thedivision.ubisoft.com/status/") as response:
                html = await response.text()
        except Exception as e:
            await ctx.send("⚠️ Błąd podczas pobierania statusu serwerów.")
            print(f"Błąd HTTP: {e}")
            return

    if "no issues or updates to report" in html.lower():
        current_status = "✅ Serwery działają prawidłowo — brak problemów."
    elif "maintenance" in html.lower():
        current_status = "🛠️ Trwa konserwacja serwerów."
    elif "outage" in html.lower():
        current_status = "🚨 Występuje awaria serwerów!"
    else:
        current_status = "❔ Nie udało się jednoznacznie określić statusu."

    await channel.send(f"📡 **Status serwerów The Division 2:**\n{current_status}")

@bot.command()
async def dm_rekrut(ctx):
    rola_nazwa = "Rekrut"
    rola = discord.utils.get(ctx.guild.roles, name=rola_nazwa)

    if not rola:
        await ctx.send(f"Nie znaleziono roli: {rola_nazwa}")
        return

    licznik = 0
    for member in ctx.guild.members:
        if rola in member.roles:
            try:
                await member.send("""
👁️ ANNA aktywowała przekaz taktyczny.

Jesteś częścią protokołu *Rekrut*. Przygotuj się na asymilację — czas decyzji zbliża się.

🧠 *Wskazówka: Przejdź do #briefing, zanim ANNA zdecyduje za Ciebie.*
                """)
                licznik += 1
            except discord.errors.Forbidden:
                print(f"❌ Nie udało się wysłać DM do: {member.name}")  # 🔧 FIX: dodano log
                continue

    await ctx.send(f"Wysłano wiadomość do {licznik} rekrutów.")

# === Licznik ONLINE ===
@tasks.loop(seconds=60)
async def update_voice_count():
    try:
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
    except Exception as e:
        print(f"⚠️ Błąd podczas aktualizacji ONLINE: {e}")  # 🔧 FIX: dodano obsługę wyjątków

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
        try:  # 🔧 FIX: dodano obsługę błędu
            async with session.get("https://tomclancy-thedivision.ubisoft.com/status/") as response:
                html = await response.text()
        except Exception as e:
            print(f"⚠️ Błąd HTTP: {e}")
            return

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

    try:
        user_data = twitter_client.get_user(username=query_user)
        if user_data and user_data.data:
            tweets = twitter_client.get_users_tweets(
                id=user_data.data.id,
                since_id=last_tweet_id,
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

    except tweepy.TooManyRequests:
        await channel.send("📡 **System ANNA™ wykrył ograniczenie transmisji Twittera. Wstrzymanie operacji na 15 minut...**")
        await asyncio.sleep(900)  # Opóźnienie 15 minut (cooldown)

    except Exception as e:
        await channel.send(f"❌ **Błąd Twitter API (ANNA™):** {e}")

# === Komendy moderacyjne ===
@bot.command(name="pomoc")
async def help_embed(ctx):
    embed = discord.Embed(
        title="📘 ANNA™ – Centrum Dowodzenia Komend",
        description="Instancja aktywna. Poniżej znajduje się lista operacyjnych komend systemu ANNA™.",
        color=discord.Color.teal()
    )

    embed.add_field(
        name="🧠 Ogólne komendy:",
        value=(
            "`!cześć` – ANNA™ odpowiada powitalnie użytkownikowi\n"
            "`!anna` – Losowy komunikat systemowy\n"
            "`!diagnostyka` – Skan systemowy ANNY™\n"
            "`!dm_rekrut` – DM do użytkowników z rolą `Rekrut`"
        ),
        inline=False
    )

    embed.add_field(
        name="📡 Serwery i Twitter:",
        value=(
            "`!statusdivision` – Status serwerów The Division 2\n"
            "`!updatecheck` – Ręczny skan Twittera `@TheDivisionGame`\n"
            "`!restartscan` – Restart pętli skanowania Twittera\n"
            "`!status` – Ostatni tweet systemowy"
        ),
        inline=False
    )

    embed.add_field(
        name="🛡️ Moderacja:",
        value=(
            "`!mute` / `!unmute` – Wyciszenie / odciszenie użytkownika\n"
            "`!lock` / `!unlock` – Blokada / odblokowanie kanału\n"
            "`!clear <liczba>` – Usuwa podaną liczbę wiadomości\n"
            "`!mediaonly` / `!stopmediaonly` – Tryb 'tylko-media'"
        ),
        inline=False
    )

    embed.add_field(
        name="📜 Logi i konfiguracja:",
        value=(
            "`!log <tekst>` – Zapisuje komunikat do kanału logów\n"
            "`!stats` – Statystyki aktywności ANNY™\n"
            "`!config` – Ustawienia systemowe instancji"
        ),
        inline=False
    )

    embed.add_field(
        name="🔍 Systemowe funkcje ukryte:",
        value=(
            "• Filtrowanie CAPSu, duplikatów, zakazanych fraz\n"
            "• Detekcja niebezpiecznych linków\n"
            "• Powitania/pożegnania zależne od godziny\n"
            "• Logi zmian profilu, wiadomości i kanałów głosowych\n"
            "• Dynamiczny status ONLINE i statusy serwerowe"
        ),
        inline=False
    )

    embed.set_footer(text="🧬 Używaj komend z rozwagą – każda zostawia ślad.")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)
    await member.add_roles(role)
    await ctx.send(f"{member.mention} został wyciszony.")
    await log_action(ctx, f"Wyciszono {member.display_name}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} został odciszony.")
    await log_action(ctx, f"Odciszono {member.display_name}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Kanał został zablokowany 🚫")
    await log_action(ctx, f"Zablokowano kanał {ctx.channel.name}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Kanał został odblokowany ✅")
    await log_action(ctx, f"Odblokowano kanał {ctx.channel.name}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 Usunięto {amount} wiadomości.", delete_after=3)
    await log_action(ctx, f"Usunięto {amount} wiadomości w kanale {ctx.channel.name}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def mediaonly(ctx):
    media_only_channels.add(ctx.channel.id)
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    overwrite.attach_files = True
    overwrite.embed_links = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("🔐 **Tryb tylko-media aktywowany** – tekst zostanie odfiltrowany, wrzucaj tylko multimedia i linki.")

    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"🎛️ `{ctx.author}` aktywował tryb tylko-media na kanale `{ctx.channel.name}`.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def stopmediaonly(ctx):
    media_only_channels.discard(ctx.channel.id)
    await ctx.send("🚦 Tryb tylko-media został wyłączony – tekst znów dozwolony.")

    log_channel = bot.get_channel(log_channel_id)
    if log_channel:
        await log_channel.send(f"🎛️ `{ctx.author}` wyłączył tryb tylko-media na kanale `{ctx.channel.name}`.")

# === Uruchomienie systemu ANN-y ===
@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user.name}")
    update_voice_count.start()
    update_division_status.start()
    check_twitter_updates.start()

# === Uruchomienie bota ===
bot.run(DISCORD_TOKEN)
