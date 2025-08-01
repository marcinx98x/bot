from discord.ext import commands

CAPS_THRESHOLD = 0.8
MIN_LENGTH = 10
EXEMPT_ROLE_NAME = "Dowódca"

class CapsGuard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_caps_message(self, content):
        letters = [c for c in content if c.isalpha()]
        if len(letters) < MIN_LENGTH:
            return False
        upper = sum(1 for c in letters if c.isupper())
        return (upper / len(letters)) >= CAPS_THRESHOLD

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.content:
            return

        if self.is_caps_message(message.content):
            if any(role.name == EXEMPT_ROLE_NAME for role in message.author.roles):
                return
            await message.delete()
            await message.channel.send(f"🔇 {message.author.mention}, ANNA mówi: zniż ton... zanim zniży Ciebie 😌")

async def setup(bot):
    await bot.add_cog(CapsGuard(bot))