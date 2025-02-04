import discord
from discord import app_commands
from discord.ext import commands
import random

class TirageAuSort(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tirage_au_sort", description="Sélectionne de manière aléatoire une option parmi celles données.")
    @app_commands.describe(choices="Les options séparées par des espaces (ex: choix1,choix2,choix3).")
    async def hasard(self, interaction: discord.Interaction, choices: str):
        options = choices.split(",")  # Divise la chaîne en une liste d'options
        if not options:
            await interaction.response.send_message("❌ Merci de fournir au moins une option pour le tirage au sort.", ephemeral=True)
            return

        gagnant = random.choice(options)
        await interaction.response.send_message(f"🎉 Le gagnant est : **{gagnant}** !")

async def setup(bot):
    await bot.add_cog(TirageAuSort(bot))
