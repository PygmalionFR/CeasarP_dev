import discord
from discord import app_commands
from discord.ext import commands
import requests
from io import BytesIO
from PIL import Image, ImageOps, ImageDraw

class Invocation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="invocation", description="Invoque une entité pour un utilisateur")
    @app_commands.describe(user="Le membre pour lequel invoquer l'entité")
    async def invocation(self, interaction: discord.Interaction, user: discord.Member):
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

        # Créer un fichier Discord et envoyer l'image
        file = discord.File(final_image, filename="invocation.png")
        embed = discord.Embed(
            title="Invocation Réussie!",  # Utilise la mention pour identifier l'utilisateur
            description=f"{user.display_name}"
        )
        embed.set_image(url="attachment://invocation.png")
        await interaction.response.send_message(f"{user.mention}",embed=embed, file=file)

async def setup(bot):
    await bot.add_cog(Invocation(bot))
