import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import get_db_connection

class ResetXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def reset_xp_for_server(self, server_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Réinitialiser l'XP et le niveau de tous les utilisateurs du serveur
        update_query = f"""
        UPDATE xp_{server_id}
        SET xp = 0, level = 0, luck = 0, sagesse = 0
        """
        cursor.execute(update_query)
        connection.commit()

        cursor.close()
        connection.close()

    @app_commands.command(name="resetxp", description="Réinitialiser l'XP de tous les membres du serveur")
    async def resetxp(self, interaction: discord.Interaction):
        print(f"Command /resetxp called for server {interaction.guild.id}")  # Log pour le débogage
        server_id = interaction.guild.id

        self.reset_xp_for_server(server_id)

        await interaction.response.send_message("L'XP de tous les membres du serveur a été réinitialisée.", ephemeral=True)

    @resetxp.error
    async def resetxp_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"Error in /resetxp command: {error}")  # Log pour le débogage
        await interaction.response.send_message("Une erreur s'est produite lors de la réinitialisation de l'XP.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ResetXP(bot))
