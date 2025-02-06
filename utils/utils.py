import discord
from PIL import Image, ImageDraw, ImageFont
import io
import requests

def create_xp_card(user, level, xp, max_xp):
    """Crée une carte d'XP avec la photo de profil du membre, son nom, son niveau et une barre de progression."""

    # Charger l'image de base
    base_image_path = 'img/carte.png'
    base_image = Image.open(base_image_path)

    # Télécharger la photo de profil de l'utilisateur
    avatar_url = str(user.avatar.url) if user.avatar else str(user.default_avatar.url)
    avatar_response = requests.get(avatar_url)
    avatar_image = Image.open(io.BytesIO(avatar_response.content))

    # Redimensionner la photo de profil
    avatar_image = avatar_image.resize((350, 350))

    # Superposer la photo de profil sur l'image de base
    base_image.paste(avatar_image, (75, 75))  # Coordonnées à ajuster selon vos besoins

    # Initialiser le dessin sur l'image
    draw = ImageDraw.Draw(base_image)

    # Charger la police
    try:
        font = ImageFont.truetype("utils/Teko-bold.ttf", 80)  # Charge une police (Teko-bold)
    except IOError:
        font = ImageFont.load_default()  # Utilise une police par défaut si Teko-bold est indisponible

    # Ajouter le nom du membre avec une bordure de 4 pixels
    name_text = user.name
    text_bbox = draw.textbbox((0, 0), name_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]

    # Dessiner la bordure noire de 4 pixels
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((450 + dx, 75 + dy), name_text, fill=(0, 0, 0), font=font)

    # Dessiner le texte avec une couleur de remplissage
    draw.text((450, 75), name_text, fill=(255, 255, 255), font=font)

    # Ajouter le niveau du membre avec une bordure
    level_text = f"Niveau {level}"
    text_bbox = draw.textbbox((0, 0), level_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Dessiner la bordure
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((125 + dx, 500 + dy), level_text, fill=(0, 0, 0), font=font)

    # Dessiner le texte avec une couleur de remplissage
    draw.text((125, 500), level_text, fill=(255, 255, 255), font=font)

    # Calculer la largeur maximale de la barre de progression
    max_bar_width = 1592

    # Ajouter la barre de progression
    bar_width = int((xp / max_xp) * max_bar_width)  # Largeur de la barre d'XP remplie
    draw.rectangle([100, 650, 100 + bar_width, 750], fill=(0, 76, 191))

    # Ajouter un cadre à la barre de progression
    draw.rectangle([98, 648, 100 + max_bar_width + 5, 748], outline=(165, 165, 165), width=8)

    # Ajout des stat
    level_text = f"Statistique :\n\nLuck    : ??\nSagesse : ??"
    text_bbox = draw.textbbox((0, 0), level_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # Dessiner la bordure
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            draw.text((1250 + dx, 75 + dy), level_text, fill=(0, 0, 0), font=font)

    # Dessiner le texte avec une couleur de remplissage
    draw.text((1250, 75), level_text, fill=(255, 255, 255), font=font)


    # Sauvegarder l'image en mémoire pour Discord
    image_binary = io.BytesIO()
    base_image.save(image_binary, format="PNG")
    image_binary.seek(0)

    return discord.File(fp=image_binary, filename="xp_card.png")
