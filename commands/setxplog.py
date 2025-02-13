import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class SetXPLog(commands.Cog):
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

    @app_commands.command(name="setxplog", description="Définir le canal des logs d'XP")
    @app_commands.describe(channel="Le canal où les logs d'XP seront envoyés")
    async def setxplog(self, interaction: discord.Interaction, channel: discord.TextChannel):
        data = self.load_data()
        server_id = str(interaction.guild.id)

        if server_id not in data:
            data[server_id] = {}

        data[server_id]['xp_log_channel'] = channel.id
        self.save_data(data)

        await interaction.response.send_message(f"Le canal des logs d'XP a été défini sur {channel.mention}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetXPLog(bot))