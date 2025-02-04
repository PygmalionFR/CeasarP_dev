import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.servers_file = 'data/servers.json'

    def load_servers_data(self):
        if os.path.exists(self.servers_file):
            with open(self.servers_file, 'r') as file:
                return json.load(file)
        return {}

    @app_commands.command(name="test",description="ceci et une commande de test")
    async def test(self,interaction: discord.Interaction):
        data = self.load_servers_data()
        server_id = str(interaction.guild.id)

        if server_id in data :
            welcome_id = data[server_id].get('welcome_channel_id')
            fonda = data[server_id].get('fondateur_id')
            await interaction.response.send_message(f"L'id de bienvenue est <#{welcome_id}> voici les <@&{fonda}>")


async def setup(bot):
    await bot.add_cog(Test(bot))