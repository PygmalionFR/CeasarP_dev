import discord
from discord import app_commands
from discord.ext import commands
import datetime
import json

# Fonction pour charger les données des serveurs depuis le fichier JSON
def load_server_data():
    try:
        with open('data/servers.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Retourne un dictionnaire vide si le fichier n'est pas trouvé
    except json.JSONDecodeError:
        return {}  # Retourne un dictionnaire vide si le fichier JSON est malformé

ts = int(datetime.datetime.utcnow().timestamp())

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ban", description="Bannir un utilisateur !")
    @app_commands.describe(user="Le membre à bannir", reason="Raison du ban")
    async def ban_slash(self, interaction: discord.Interaction, user: discord.Member, reason: str = None):
        # Charger les données du serveur à partir du fichier JSON
        server_data = load_server_data()
        server_id = str(interaction.guild.id)

        # Si aucune raison n'est donnée, définir une raison par défaut
        if reason is None:
            reason = "Aucune raison fournie"

        # Vérifier si le serveur a des données et un canal de log défini
        if server_id in server_data:
            log_channel_id = server_data[server_id].get('log_channel_id')
            if log_channel_id:
                log_channel = interaction.guild.get_channel(log_channel_id)
            else:
                await interaction.response.send_message("Erreur : Aucun canal de log défini dans la configuration.", ephemeral=True)
                return
        else:
            await interaction.response.send_message("Erreur : Données du serveur non trouvées.", ephemeral=True)
            return

        # Bannir l'utilisateur
        await interaction.guild.ban(user, reason=reason)

        # Créer l'embed pour annoncer le bannissement
        embed = discord.Embed(title="Bannissement", description="Un modérateur a banni un membre", color=0xff0000)
        embed.add_field(name="`Membre Information` :", value=f"`Utilisateur` : {user.mention}\n `Date` : <t:{ts}:R>\n `Modérateur responsable` : {interaction.user.mention}\n `Raison` :\n ```{reason}```")
        embed.timestamp = datetime.datetime.now()

        # Répondre à l'interaction avec l'embed
        await interaction.response.send_message(embed=embed)

        # Envoyer l'embed dans le canal de log
        await log_channel.send(embed=embed)

async def setup(bot):
    # Appel asynchrone à add_cog avec await
    await bot.add_cog(Ban(bot))
