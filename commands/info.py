import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Info du serveur")
    async def info_slash(self, interaction: discord.Interaction):
        server = interaction.guild
        server_name = server.name
        member_count = server.member_count
        text_channels = len(server.text_channels)
        voice_channels = len(server.voice_channels)

        embed = discord.Embed(title=f"Informations sur le serveur {server_name}", color=0x3498db)
        embed.add_field(name=f"Le serveur *{server_name}* :", value=f"A `{member_count}` membres \nIl y a `{text_channels}` salons textuels et `{voice_channels}` salons vocaux")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
