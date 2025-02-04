import discord
from discord import app_commands
from discord.ext import commands
import random

class Shifumi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class MyView(discord.ui.View):
        def __init__(self):
            super().__init__()

        @discord.ui.button(label="Pierre", emoji="🪨", style=discord.ButtonStyle.primary)
        async def pierre_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result, color = await self.run_shifumi_script("Pierre")
            embed = discord.Embed(title="Résultat", description=result, color=color)
            self.disable_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

        @discord.ui.button(label="Papier", emoji="🍃", style=discord.ButtonStyle.primary)
        async def papier_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result, color = await self.run_shifumi_script("Papier")
            embed = discord.Embed(title="Résultat", description=result, color=color)
            self.disable_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

        @discord.ui.button(label="Ciseaux", emoji="✂️", style=discord.ButtonStyle.primary)
        async def ciseaux_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            result, color = await self.run_shifumi_script("Ciseaux")
            embed = discord.Embed(title="Résultat", description=result, color=color)
            self.disable_buttons()
            await interaction.response.edit_message(embed=embed, view=self)

        async def run_shifumi_script(self, user_choice: str):
            # Choix du bot
            choices = ["Pierre", "Papier", "Ciseaux"]
            bot_choice = random.choice(choices)

            # Déterminer le gagnant et la couleur de l'embed
            if user_choice == bot_choice:
                result = f"Tu as choisi {user_choice}\nLe bot a choisi {bot_choice}.\nC'est un match nul!"
                color = discord.Color.yellow()
            elif (user_choice == "Pierre" and bot_choice == "Ciseaux") or \
                 (user_choice == "Papier" and bot_choice == "Pierre") or \
                 (user_choice == "Ciseaux" and bot_choice == "Papier"):
                result = f"Tu as choisi {user_choice}\nLe bot a choisi {bot_choice}.\nTu as gagné!"
                color = discord.Color.green()
            else:
                result = f"Tu as choisi {user_choice}\nLe bot a choisi {bot_choice}.\nTu as perdu!"
                color = discord.Color.red()

            return result, color

        def disable_buttons(self):
            """Désactive tous les boutons après un clic"""
            for child in self.children:
                child.disabled = True

    @app_commands.command(name="shifumi", description="Lance un pierre feuille ciseaux")
    async def shifumi_slash(self, interaction: discord.Interaction):
        view = self.MyView()
        embed = discord.Embed(title="Shifumi", color=discord.Color.green())
        embed.add_field(name="Joue à pierre feuille ciseaux", value="Choisis une option ci-dessous :")
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Shifumi(bot))
