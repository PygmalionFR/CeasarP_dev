import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import get_db_connection

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel_id(self, server_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Récupérer l'ID du canal de log pour le serveur
        select_query = f"""
        SELECT log_channel_id FROM server_{server_id}
        WHERE server_id = %s
        """
        cursor.execute(select_query, (server_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result[0] if result else None

    @app_commands.command(name="purge", description="Efface les messages du canal")
    @app_commands.describe(channel="Le salon où les messages seront supprimés")
    async def purge_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        server_id = interaction.guild.id
        log_channel_id = self.get_log_channel_id(server_id)
        log = interaction.guild.get_channel(log_channel_id) if log_channel_id else None

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
        await channel.purge(limit=100)

async def setup(bot):
    await bot.add_cog(Purge(bot))
