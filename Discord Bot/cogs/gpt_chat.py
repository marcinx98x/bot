from discord.ext import commands
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

class GPTChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anna")
    async def speak_as_anna(self, ctx, *, prompt: str):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Mów jako ANNA: sarkastyczna, zabawna, ale wspierająca persona z uniwersum Marcinowego."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            reply = response.choices[0].message.content
            await ctx.send(reply)
        except Exception as e:
            await ctx.send(f"Ups... ANNA zgubiła głos 🤐 ({type(e).__name__})")

async def setup(bot):
    await bot.add_cog(GPTChat(bot))