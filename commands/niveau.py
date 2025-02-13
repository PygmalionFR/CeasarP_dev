import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from utils.utils import create_xp_card

class LevelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/xp_data.json'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_xp_for_next_level(level):
        if level == 0:
            return 1
        elif level == 1:
            return 50
        else:
            return int(50 * (1.3 ** (level - 1)))

    @app_commands.command(name="niveau", description="Affiche votre niveau et votre progression")
    @app_commands.describe(user="L'utilisateur dont vous voulez voir le niveau")
    async def niveau(self, interaction: discord.Interaction, user: discord.User = None):
        user = user or interaction.user
        server_id = str(interaction.guild.id)
        user_id = str(user.id)

        data = self.load_data()
        if server_id not in data or user_id not in data[server_id]:
            await interaction.response.send_message("Aucune donnée d'XP trouvée pour cet utilisateur.", ephemeral=True)
            return

        user_data = data[server_id][user_id]
        level = user_data['level']
        xp = user_data['xp']
        max_xp = self.get_xp_for_next_level(level)

        xp_card_image = create_xp_card(user, level, xp, max_xp)
        try:
            await interaction.response.send_message(file=xp_card_image)
        except discord.HTTPException as e:
            await interaction.response.send_message(f"Erreur lors de l'envoi de l'image : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(LevelCommand(bot))