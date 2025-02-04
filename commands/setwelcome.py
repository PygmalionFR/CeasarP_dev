import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class SetWelcome(commands.Cog):
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

    @app_commands.command(name="setwelcome", description="Définit l'ID du canal de bienvenue")
    @app_commands.describe(channel="Le canal de bienvenue")
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        server_id = str(interaction.guild.id)

        if server_id in self.server_data:
            self.server_data[server_id]['welcome_channel_id'] = channel.id
            self.save_server_data()
            await interaction.response.send_message(f"L'ID du canal de bienvenue a été défini sur <#{channel.id}>")
        else:
            await interaction.response.send_message("Erreur : Données du serveur non trouvées.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetWelcome(bot))
