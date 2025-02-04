import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio

class JustePrix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="justeprix", description="Lance le jeu du juste prix")
    async def justeprix_slash(self, interaction: discord.Interaction):
        prix = random.randint(1, 100)
        vie = 6
        embed = discord.Embed(title="Juste Prix", color=discord.Color.green())
        embed.add_field(name="Trouve le juste prix", value=f"Le juste prix est entre 1 et 100, tu as {vie} chances.")
        await interaction.response.send_message(embed=embed)

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        while vie > 0:
            try:
                guess = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess_number = int(guess.content)

                if guess_number < prix:
                    vie -= 1
                    embed = discord.Embed(title="Juste Prix", color=discord.Color.orange())
                    embed.add_field(name="C'est plus!", value=f"Vie restante: {vie}")
                    await interaction.followup.send(embed=embed)
                elif guess_number > prix:
                    vie -= 1
                    embed = discord.Embed(title="Juste Prix", color=discord.Color.orange())
                    embed.add_field(name="C'est moins!", value=f"Vie restante: {vie}")
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(title="Félicitations!", color=discord.Color.green())
                    embed.add_field(name=f"Tu as trouvé le juste prix!", value=f"Le prix était {prix}. Vie restante: {vie}")
                    await interaction.followup.send(embed=embed)
                    break
            except asyncio.TimeoutError:
                await interaction.followup.send("Désolé, tu as mis trop de temps à répondre. Le jeu est terminé.")
                break
            except ValueError:
                await interaction.followup.send("Merci d'entrer un nombre valide.")

        if vie == 0:
            embed = discord.Embed(title="Perdu!", color=discord.Color.red())
            embed.add_field(name="Le jeu est terminé.", value=f"Le juste prix était {prix}.")
            await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JustePrix(bot))
