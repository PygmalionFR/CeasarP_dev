import discord
from discord.ui import View
import random
import requests
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw

class MyView(View):
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
            result = f"Tu a choisi {user_choice}\nLe bot a choisi {bot_choice}.\nC'est un match nul!"
            color = discord.Color.yellow()
        elif (user_choice == "Pierre" and bot_choice == "Ciseaux") or \
             (user_choice == "Papier" and bot_choice == "Pierre") or \
             (user_choice == "Ciseaux" and bot_choice == "Papier"):
            result = f"Tu a choisi {user_choice}\nLe bot a choisi {bot_choice}.\nTu as gagné!"
            color = discord.Color.green()
        else:
            result = f"Tu a choisi {user_choice}\nLe bot a choisi {bot_choice}.\nTu as perdu!"
            color = discord.Color.red()

        return result, color

    def disable_buttons(self):
        """Désactive tous les boutons après un clic"""
        for child in self.children:
            child.disabled = True

def create_invocation_image(user):
    # Chemin vers votre image de fond
    background_path = "./img/invocation.png"

    # Charger l'image de fond
    background = Image.open(background_path).convert("RGBA")

    # Récupérer l'avatar de l'utilisateur sous forme d'image
    avatar_url = user.display_avatar.url
    response = requests.get(avatar_url)
    avatar = Image.open(BytesIO(response.content)).convert("RGBA")

    # Redimensionner l'avatar
    avatar_size = (120, 120)  # Taille de l'avatar
    avatar = avatar.resize(avatar_size)

    # Créer un masque circulaire
    mask = Image.new("L", avatar_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + avatar_size, fill=255)

    # Appliquer le masque à l'avatar pour rendre les coins transparents
    avatar = ImageOps.fit(avatar, avatar_size, method=0, bleed=0.2)
    avatar.putalpha(mask)

    # Calculer les coordonnées pour centrer l'avatar
    bg_width, bg_height = background.size
    avatar_x = (bg_width - avatar_size[0]) // 2
    avatar_y = (bg_height - avatar_size[1]) // 2

    # Coller l'avatar rond sur l'image de fond
    background.paste(avatar, (avatar_x, avatar_y), avatar)

    # Sauvegarder l'image finale en mémoire
    final_image = BytesIO()
    background.save(final_image, "PNG")
    final_image.seek(0)

    return final_image
