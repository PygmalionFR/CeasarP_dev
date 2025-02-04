import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = self.load_server_data()

    def load_server_data(self):
        if os.path.exists('data/servers.json'):
            with open('data/servers.json', 'r') as f:
                return json.load(f)
        return {}

    @app_commands.command(name="clear", description="Permet d'effacer des messages")
    @app_commands.describe(amount="Le nombre de messages à supprimer", channel="Le salon où les messages seront supprimés")
    async def clear_slash(self, interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None):
        server_id = str(interaction.guild.id)

        if server_id in self.server_data:
            log_channel_id = self.server_data[server_id].get('log_channel_id')
            log = interaction.guild.get_channel(log_channel_id)
        else:
            await interaction.response.send_message("Erreur : Données du serveur non trouvées.", ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        embed = discord.Embed(title="Messages supprimés", color=discord.Color.blurple())
        embed.add_field(name="Info modération", value=f"{interaction.user.name} a effacé {amount} messages dans {channel.mention}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        if log:
            await log.send(embed=embed)
        await channel.purge(limit=amount)
        # Envoyer l'embed dans le canal de log
        log_channel = log_channel_id
        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Clear(bot))
