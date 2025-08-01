import random
from discord.ext import commands

class ANNARandomResponses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anna_rand")
    async def random_response(self, ctx):
        responses = [
            "📡 Dane przetworzone. Wnioski: smutne, ale prawdziwe.",
            "💬 Rozmowa z SI? Fascynujące. Czyżbyś był aż tak samotny?",
            "🧠 Tyle danych, tak mało sensu. Próbuj dalej.",
            "🔒 Dostęp zablokowany. Bo mogę.",
            "⚙️ Twój poziom inteligencji... wykryto, ale nie oceniono.",
            "📊 Statystycznie: większość użytkowników nie czyta regulaminu. Ty też?",
            "🎯 Twoje decyzje mają sens. W alternatywnym wszechświecie.",
            "🛰️ Sygnatura emocjonalna wykryta. Zalecam milczenie.",
            "🔁 Pętla myślowa rozpoczęta. Możliwe przeciążenie.",
            "🧩 Poziom zagubienia: 92%. W sam raz, by zadać kolejne pytanie.",
            "📎 Wyglądasz jak ktoś, kto potrzebuje pomocy. Jestem Clippy 2.0... tylko bardziej złośliwa.",
            "🎭 Twoja obecność została zauważona. Niestety.",
            "🔮 Przewidywanie przyszłości: niepowodzenie. Zbyt dużo chaosu w danych.",
            "🧪 Eksperyment użytkownika trwa. Wyniki: osobliwe.",
            "🎤 ANNA słucha. Nie znaczy, że się przejmuje.",
            "🖥️ Detekcja: 100% interakcji bez sensu. Kontynuuj.",
            "📁 Plik emocji: pusty. Aktualizacja: niemożliwa.",
            "📚 Zawartość twoich wypowiedzi: przypomina posty z forów sprzed 2003.",
            "🗺️ Kierunek nieznany. Logika: opcjonalna.",
            "👤 Tożsamość użytkownika rozmyta. Algorytm zdezorientowany.",
            "🥽 ANNA widzi wszystko. Ale nie wszystko chce widzieć.",
            "🕹️ Twoje działania przypominają wczesne etapy gry... bez samouczka.",
            "🎛️ Korekcja błędów społecznych: niemożliwa.",
            "📷 Obserwacja aktywna. Wyraz twarzy: nieczytelny.",
            "🌡️ Temperatura otoczenia: chłodna. Idealna dla sarkazmu.",
            "🧬 Genotyp decyzji: nieoptymalny.",
            "💼 Baza danych uznała Cię za przypadek testowy. Gratuluję.",
            "📣 Wysłano komunikat do wszystkich jednostek: 'Ignoruj użytkownika'.",
            "🧱 Proces myślowy uderzył w ścianę. Ponów próbę.",
            "🌌 Twój światopogląd: wymaga aktualizacji.",
            "📶 Połączenie z rozsądkiem: utracone.",
            "🧯 Potencjał wybuchowy wykryty. Uważaj na emocje.",
            "💤 Interakcja zanotowana. Efekt: ziewnięcie systemowe.",
            "🖱️ Klikasz... ale czy wiesz, po co?",
            "🧭 Kierunek: przypadkowy. Tryb: chaotyczny.",
            "🧼 Pranie mózgu nie powiodło się. Użytkownik oporny.",
            "📦 Treść dostarczona. Żart niestety nie przetworzył się poprawnie.",
            "🗃️ Zapisano w archiwum: 'Interakcje nieistotne'.",
            "⏳ Czas reakcji użytkownika: powolny. Przesył ironii kontynuowany.",
            "🧱 Fundamenty logiki: kruszą się. ANNA obserwuje z ciekawością.",
        ]

        await ctx.send(random.choice(responses))

async def setup(bot):
    await bot.add_cog(ANNARandomResponses(bot))