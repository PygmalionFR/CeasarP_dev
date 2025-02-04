import discord
from discord import app_commands
from discord.ext import commands
import asyncio

class Timer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="timer", description="Démarre un minuteur")
    @app_commands.describe(hours="Nombre d'heures", minutes="Nombre de minutes", seconds="Nombre de secondes")
    async def timer_slash(self, interaction: discord.Interaction, hours: int = 0, minutes: int = 0, seconds: int = 0):
        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds <= 0:
            await interaction.response.send_message("La durée du minuteur doit être supérieure à zéro.", ephemeral=True)
            return

        await interaction.response.send_message(f"Minuteur démarré pour {hours} heures, {minutes} minutes et {seconds} secondes.", ephemeral=True)
        await asyncio.sleep(total_seconds)
        await interaction.followup.send(f"Minuteur de {hours}h:{minutes}m:{seconds}s est terminé.")

async def setup(bot):
    await bot.add_cog(Timer(bot))
