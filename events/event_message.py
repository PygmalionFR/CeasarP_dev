import discord
from discord.ext import commands

class MessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignorer les messages envoyés par le bot lui-même
        if message.author == self.bot.user:
            return

        # Liste des variantes de "quoi"
        quoi_variants = [
            "quoi ?",
            "quoi !",
            "quoi.",
            "quoi...",
            "quoi !?",
            "quoi ?!",
            "quoi !!",
            "quoi ???",
            "quoi !??",
            "quoi ?!?",
            "quoi",
            "Quoi",
            "kwa"
        ]

        # Vérifier si le message est dans la liste des variantes
        if message.content.lower() in quoi_variants:
            await message.channel.send("feur")

async def setup(bot):
    await bot.add_cog(MessageEvents(bot))

