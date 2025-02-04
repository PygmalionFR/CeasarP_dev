import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class ResetXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/data.json'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    @app_commands.command(name="resetxp", description="Réinitialiser l'XP de tous les membres du serveur")
    async def resetxp(self, interaction: discord.Interaction):
        print(f"Command /resetxp called for server {interaction.guild.id}")  # Log pour le débogage
        data = self.load_data()
        server_id = str(interaction.guild.id)

        if server_id in data:
            print(f"Resetting XP for server {server_id}")  # Log pour le débogage
            for user_id, user_data in data[server_id].items():
                if isinstance(user_data, dict):
                    user_data['xp'] = 0
                    user_data['level'] = 0
                else:
                    print(f"Invalid data for user {user_id}: {user_data}")

            self.save_data(data)
            await interaction.response.send_message("L'XP de tous les membres du serveur a été réinitialisée.", ephemeral=True)
        else:
            print(f"No XP data found for server {server_id}")  # Log pour le débogage
            await interaction.response.send_message("Aucune donnée d'XP trouvée pour ce serveur.", ephemeral=True)

    @resetxp.error
    async def resetxp_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        print(f"Error in /resetxp command: {error}")  # Log pour le débogage
        await interaction.response.send_message("Une erreur s'est produite lors de la réinitialisation de l'XP.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ResetXP(bot))
