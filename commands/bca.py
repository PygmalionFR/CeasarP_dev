import discord
from discord import app_commands
from discord.ext import commands

class BCA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bca", description="Commande pour faire une annonce Admin")
    @app_commands.describe(annonceadmin="Annonce")
    async def bca_slash(self, interaction: discord.Interaction, annonceadmin: str):
        embed = discord.Embed(title="**Annonce Admin**")
        embed.add_field(name=f"Annonce de `{interaction.user.display_name}`", value=annonceadmin)
        embed.set_thumbnail(
            url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F940660766187593728.gif%3Fv%3D1&w=64&q=75")
        await interaction.response.send_message("@everyone", embed=embed)

async def setup(bot):
    await bot.add_cog(BCA(bot))
