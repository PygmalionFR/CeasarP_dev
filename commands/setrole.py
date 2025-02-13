import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import get_db_connection

class SetRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def update_role_id(self, server_id, role_type, role_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Mettre à jour l'ID du rôle dans la table du serveur
        update_query = f"""
        UPDATE server_{server_id}
        SET {role_type}_id = %s
        WHERE server_id = %s
        """
        cursor.execute(update_query, (role_id, server_id))
        connection.commit()

        cursor.close()
        connection.close()

    @app_commands.command(name="setrole", description="Définit l'ID du rôle pour différents rôles")
    @app_commands.describe(role_type="Type de rôle", role="Rôle")
    @app_commands.choices(role_type=[
        app_commands.Choice(name="fondateur", value="fondateur"),
        app_commands.Choice(name="admin", value="admin"),
        app_commands.Choice(name="modo", value="modo"),
        app_commands.Choice(name="membreplus", value="membreplus"),
        app_commands.Choice(name="membre", value="membre")
    ])
    async def set_role(self, interaction: discord.Interaction, role_type: app_commands.Choice[str], role: discord.Role):
        server_id = interaction.guild.id
        self.update_role_id(server_id, role_type.value, role.id)

        await interaction.response.send_message(f"L'ID du rôle {role_type.value} a été défini sur <@&{role.id}>", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetRole(bot))
