import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class SetRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = self.load_server_data()

    def load_server_data(self):
        if os.path.exists('data/servers.json'):
            with open('data/servers.json', 'r') as f:
                return json.load(f)
        return {}

    def save_server_data(self):
        with open('data/servers.json', 'w') as f:
            json.dump(self.server_data, f, indent=4)

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
        server_id = str(interaction.guild.id)

        if server_id not in self.server_data:
            self.server_data[server_id] = {}

        # Mettre à jour l'ID du rôle spécifié dans les données du serveur
        self.server_data[server_id][f"{role_type.value}_id"] = role.id
        self.save_server_data()

        await interaction.response.send_message(f"L'ID du rôle {role_type.value} a été défini sur <@&{role.id}>")

async def setup(bot):
    await bot.add_cog(SetRole(bot))
