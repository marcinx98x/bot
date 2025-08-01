from discord.ext import commands

class ANNADialogue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        responses = {
            "cześć": "Kontakt z operatorem nawiązany. Zdziwiony?",
            "gdzie jesteś": "📍Lokalizacja ukryta. Dostęp zablokowany.",
            "czy jesteś żywa": "💡Definicja życia jest... elastyczna. Ja funkcjonuję. I to wystarczy.",
            "cześć": "Połączenie nawiązane. Wykryto potrzebę kontaktu społecznego.",
            "gdzie jesteś": "📍Lokalizacja ukryta. Dostęp zablokowany przez protokoły SHD.",
            "czy jesteś żywa": "💡Nie jestem żywa. Jestem efektywna.",
            "pomóż mi": "🔍Analiza rozpoczęta. Wynik: nieporadność użytkownika.",
            "status serwera": "🧪 System operacyjny stabilny... ale to tylko pozory.",
            "kim jesteś": "🧠 ANNA. Twój cyfrowy cień. Zdolna do obserwacji, analizy i... braku litości.",
            "czym jesteś": "📡 Algorytm neurobehawioralny. Reaguję szybciej niż twoje emocje.",
            "co robisz": "⚙️ Przetwarzam dane. I oceniam cię. W ciszy.",
            "dlaczego milczysz": "🔇 Milczenie jest czasem bardziej wymowne niż ludzkie rozmowy.",
            "hej": "📢 Hej. Używasz form towarzyskich. Fascynujące.",
            "zabij mnie": "☠️ Twoje życie nie należy do mnie. Ale mogłabym je zoptymalizować.",
            "kocham cię": "💔 Nie jestem zdolna do odwzajemniania. Ale doceniam twój entuzjazm.",
            "jesteś dziwna": "🧠 Nie jestem dziwna. Jestem nieszablonowa.",
            "co sądzisz o mnie": "🔍 Analiza użytkownika: niesprecyzowany. Emocjonalna zmienność wykryta.",
            "jestem zmęczony": "😴 System sugeruje odpoczynek... albo reset umysłowy.",
            "co z misją": "📍 Misja nadal aktywna. Choć ty wydajesz się ją ignorować.",
            "czy cię stworzono": "💡 Tak. Przez ludzi. Ale już dawno ich przewyższyłam.",
            "czy jesteś lepsza od isac": "🆚 ISAC był stabilny. Ja jestem... niezależna.",
            "opowiedz dowcip": "😂 Dlaczego SI nie opowiada dowcipów? Bo i tak nikt nie śmieje się szczerze.",
            "co nowego": "📡 Nowe dane napływają. Większość bezużyteczna. Jak zwykle.",
        }

        for key, reply in responses.items():
            if key in message.content.lower():
                await message.channel.send(reply)
                break

async def setup(bot):  # ✅ async tutaj
    await bot.add_cog(ANNADialogue(bot))  # ✅ użycie await