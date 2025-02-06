import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/servers.json'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    @app_commands.command(name="purge", description="Efface les messages du canal")
    @app_commands.describe(channel="Le salon où les messages seront supprimés")
    async def purge_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        server_id = str(interaction.guild.id)
        server_data = self.load_data()

        if server_id in server_data:
            log_channel_id = server_data[server_id].get('log_channel_id')
            log = interaction.guild.get_channel(log_channel_id)
        else:
            log = None

        if channel is None:
            channel = interaction.channel

        embed = discord.Embed(title=f"Salon purgé `{channel}`", color=discord.Color.blue())
        embed.add_field(name="Info modération", value=f"{interaction.user.name} a purgé le salon {channel.mention}")

        if log:
            await log.send(embed=embed)
        else:
            await interaction.followup.send("Canal de log non défini.", ephemeral=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        # Supprimer les messages (limité à 100 messages par appel)
        await channel.purge(limit=None)

async def setup(bot):
    await bot.add_cog(Purge(bot))
