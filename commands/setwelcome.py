import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import get_db_connection

class SetWelcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def update_welcome_channel(self, server_id, channel_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Mettre à jour le canal de bienvenue dans la table du serveur
        update_query = f"""
        UPDATE server_{server_id}
        SET welcome_channel_id = %s
        WHERE server_id = %s
        """
        cursor.execute(update_query, (channel_id, server_id))
        connection.commit()

        cursor.close()
        connection.close()

    @app_commands.command(name="setwelcome", description="Définit l'ID du canal de bienvenue")
    @app_commands.describe(channel="Le canal de bienvenue")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        server_id = interaction.guild.id
        self.update_welcome_channel(server_id, channel.id)

        await interaction.response.send_message(f"L'ID du canal de bienvenue a été défini sur {channel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetWelcome(bot))
