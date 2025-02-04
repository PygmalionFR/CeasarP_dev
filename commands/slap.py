import discord
from PIL.ImageColor import colormap
from discord import app_commands
from discord.ext import commands

class Slap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gifle", description="Donne une gifle à quelqu'un")
    @app_commands.describe(user="Envoie une gifle à quelqu'un")
    async def gifle(self, interaction: discord.Interaction, user: discord.Member):
        gif_path = "./gif/slap.gif"
        embed = discord.Embed(title=f"{user.display_name} reçoit une gifle de {interaction.user.display_name}", color=0xFF4500)
        embed.set_image(url="attachment://slap.gif")

        await interaction.response.send_message(f"{user.mention}",embed=embed, file=discord.File(gif_path, ))

async def setup(bot):
    await bot.add_cog(Slap(bot))
