import discord
from discord import app_commands
from discord.ext import commands

class Film(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="diffusion", description="Informations sur la diffusion d'un film")
    @app_commands.describe(nom="Nom de la diffusion", time="Heure à laquelle la diffusion sera diffusé", urlimg="URL de l'image de la diffusion", channel="Salon vocal où ce sera diffusé")
    async def film_slash(self, interaction: discord.Interaction, nom: str, urlimg: str, time: str, channel: discord.VoiceChannel):
        embed = discord.Embed(title=f"Diffusion de {nom} dans le salon {channel.name}", color=0x3498db)
        embed.add_field(name="Nom de la diffusion", value=nom)
        embed.add_field(name="Heure de diffusion", value=time)
        embed.set_image(url=urlimg)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Film(bot))
