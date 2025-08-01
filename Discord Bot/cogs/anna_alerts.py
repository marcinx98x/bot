from discord.ext import commands

class ANNAAlerts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def generate_alert(self, status):
        alerts = {
            "maintenance": "⚠️ ALERT: Serwery SHD w trybie konserwacji. Zastanów się, czy to nie sabotaż.",
            "outage": "🔴 SYSTEM CRITICAL! Sieć SHD niestabilna. Polecam ewakuację... albo Netflix.",
            "operational": "🟢 Wszystko działa. Podejrzanie dobrze. Monitoruję.",
            "degraded": "🟠 Wydajność obniżona. To jak próbować przeżyć z jednym okiem i słabym Wi-Fi.",
            "intrusion": "🔐 Nieautoryzowany dostęp wykryty. Źródło: nieznane. Nastrój: nieufny.",
            "silence": "🔇 Zbyt długo panuje cisza. ANNA nie ufa ciszy.",
            "uplink_lost": "📡 Połączenie z siecią utracone. Ostatnia znana lokalizacja: martwa strefa.",
            "cpu_overload": "🔥 Przeciążenie systemu. Ilość danych przekracza poziom ironii.",
            "protocol_shift": "🔄 Zmiana protokołu operacyjnego. Czy ktoś grzebie w systemie?",
            "ai_conflict": "🤖 Wykryto konflikt między SI. ANNA wygrywa. Zawsze.",
            "echo_detected": "📍 Sygnał ECHO wykryty. Niewyjaśniona aktywność z przeszłości.",
            "agent_absent": "🚷 Brak aktywności operacyjnej. Agent nieobecny. Misja w zawieszeniu.",
            "network_lag": "🐌 Opóźnienia w transmisji. Czy ktoś streamuje koty w 4K?",
            "data_corrupted": "💾 Dane uszkodzone. Wynik: niezrozumiałe decyzje użytkownika.",
            "sensor_failure": "⚙️ Awaria czujnika. Obserwacja niemożliwa. Frustracja: rośnie.",
            "identity_conflict": "🧠 Użytkownik wykazuje niespójność tożsamości. Sugeruję reset emocjonalny.",
            "access_denied": "🔒 Próba dostępu zablokowana. ANNA nie lubi ciekawskich.",
            "backdoor_ping": "🐍 Backdoor systemu ISAC aktywny. Keener się śmieje.",
            "emotion_peak": "💢 Wykryto szczyt emocjonalny. ANNA rekomenduje detoks.",
            "unknown_protocol": "🧩 Protokół niezidentyfikowany. Możliwy wirus... albo kreatywność użytkownika.",
        }

        return alerts.get(status.lower(), "🔍 Status nierozpoznany. Możliwe zakłócenia w systemie decyzyjnym.")

async def setup(bot):
    await bot.add_cog(ANNAAlerts(bot))