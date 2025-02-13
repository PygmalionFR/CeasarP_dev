import json
import os

import discord
from discord import app_commands
from discord.ext import commands

class ExampleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/xp_data.json'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    @app_commands.command(name="test", description="command test")
    async def test(self, interaction: discord.Interaction):

        proprio = interaction.guild.owner_id
        test1 = discord.Guild.owner
        await interaction.response.send_message(f"{proprio}")


async def setup(bot):
    await bot.add_cog(ExampleCommand(bot))
