import discord
from discord import app_commands
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="purge", description="Efface tous les messages du channel")
    @app_commands.describe(channel="Le salon où les messages seront supprimés")
    async def purge_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        server_id = str(interaction.guild.id)

        if server_id in server_data:
            log_channel_id = server_data[server_id].get('log_channel_id')
            log = interaction.guild.get_channel(log_channel_id)
        else:
            await interaction.response.send_message("Erreur : Données du serveur non trouvées.", ephemeral=True)
            return

        if channel is None:
            channel = interaction.channel

        embed = discord.Embed(title=f"Salon purgé `{channel}`", color=discord.Color.blurple())
        embed.add_field(name="Info modération", value=f"{interaction.user.name} a purgé le salon {channel.mention}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await log.send(embed=embed)
        await channel.purge(limit=None)

async def setup(bot):
    await bot.add_cog(Purge(bot))
