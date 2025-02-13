import discord
from discord.ext import commands


class SetupChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup_welcome_channel(guild):
    """Créer un canal et envoyer un message de configuration"""
    try:
        channel = await guild.create_text_channel('bot-setup')
        print(f"Canal créé avec succès sur le serveur {guild.id}")

        embed_setup = discord.Embed(
            title="⚙️ Configuration du bot",
            description="Merci de m'avoir ajouté à votre serveur ! Voici comment configurer le bot en quelques étapes :",
            color=discord.Color.green()
        )

        embed_setup.add_field(
            name="1️⃣ Configurer les canaux de logs",
            value=(
                "1.1 • **/setxplog** → Canal pour les logs d'XP.\n"
                "1.2 • **/setwelcome** → Canal pour les messages de bienvenue.\n"
                "1.3 • **/setlog** → Canal pour les logs du serveur."
            ),
            inline=False
        )

        embed_setup.add_field(
            name="2️⃣ Définir les 5 rôles : **Fondateur**, **Admin**, **Modérateur**, **MembrePlus**, **Membre**",
            value="Utilisez **/setrole** pour attribuer les rôles aux membres.\n‼️⚠️ Assurez-vous que ces rôles existent avant d’exécuter la commande ! ⚠️‼️",
            inline=False
        )

        embed_setup.set_footer(text="Une fois ces étapes complétées, votre bot sera prêt à l'emploi ! 🚀")

        await channel.send(embed=embed_setup)
        print(f"Message envoyé dans le canal {channel.id} sur le serveur {guild.id}")

    except discord.Forbidden:
        print(f"Permission insuffisante pour créer un canal sur {guild.id}")
    except discord.HTTPException as e:
        print(f"Erreur lors de la configuration du serveur {guild.id}: {e}")

async def setup(bot):
    await bot.add_cog(SetupChannel(bot))