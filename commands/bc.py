import discord
from discord import app_commands
from discord.ext import commands

class BC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bc", description="Commande pour faire une annonce")
    @app_commands.describe(bc="Annonce")
    async def bc_slash(self, interaction: discord.Interaction, bc: str):
        embed = discord.Embed(title="**Annonce**")
        embed.add_field(name=f"Annonce de `{interaction.user.display_name}`", value=bc)
        embed.set_thumbnail(
            url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Fstickers%2F1075394037793705984.png&w=128&q=75")
        await interaction.response.send_message("@everyone", embed=embed)

async def setup(bot):
    await bot.add_cog(BC(bot))
