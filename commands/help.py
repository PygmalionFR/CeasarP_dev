import discord
from discord import app_commands
from discord.ext import commands
from utils.utils import get_db_connection

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_server_roles(self, server_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        # Récupérer les IDs des rôles pour le serveur
        select_query = f"""
        SELECT fondateur_id, admin_id, modo_id, membreplus_id, membre_id
        FROM server_{server_id}
        WHERE server_id = %s
        """
        cursor.execute(select_query, (server_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result if result else (None, None, None, None, None)

    @app_commands.command(name="help", description="Affiche l'aide pour toutes les commandes")
    async def help_slash(self, interaction: discord.Interaction):
        server_id = interaction.guild.id
        fonda, admin, modo, membreplus, membre = self.get_server_roles(server_id)

        admin_commands = [
            {"command": "/setxplog", "description": "Définit un canal pour les logs d'XP", "role": f"<@&{fonda}>"},
            {"command": "/setwelcome", "description": "Définit le canal des messages de bienvenue", "role": f"<@&{fonda}>"},
            {"command": "/setlog", "description": "Définit un canal pour les logs", "role": f"<@&{fonda}>"},
            {"command": "/setrole", "description": "Assigne un rôle à un grade", "role": f"<@&{fonda}>"},
            {"command": "/resetxp", "description": "Réinitialise l'XP des utilisateurs", "role": f"<@&{fonda}>"},
            {"command": "/purge", "description": "Supprime tous les messages d’un canal", "role": f"<@&{fonda}>"},
            {"command": "/ban", "description": "Bannit un utilisateur du serveur", "role": f"<@&{fonda}>, <@&{admin}>"},
            {"command": "/unban", "description": "Débannit un utilisateur", "role": f"<@&{fonda}>, <@&{admin}>"},
            {"command": "/bca", "description": "Envoie un message de broadcast (Admin)", "role": f"<@&{fonda}>, <@&{admin}>"},
            {"command": "/bc", "description": "Envoie un message de broadcast", "role": f"<@&{fonda}>, <@&{admin}>, <@&{modo}>"},
            {"command": "/clear", "description": "Supprime un nombre défini de messages", "role": f"<@&{fonda}>, <@&{admin}>, <@&{modo}>"}
        ]

        user_commands = [
            {"command": "/film", "description": "Permet de programmer une diffusion avec heure, lieu et image", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/slap", "description": "Donne une gifle à un utilisateur", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/invocation", "description": "Invoque un utilisateur", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/justeprix", "description": "Joue au jeu du Juste Prix", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/timer", "description": "Définit un minuteur", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/tirage_au_sort", "description": "Effectue un tirage au sort", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/info", "description": "Affiche les informations du serveur", "role": f"<@&{membreplus}>, <@&{membre}>"},
            {"command": "/botinfo", "description": "Affiche les informations sur le bot", "role": f"<@&{membreplus}>, <@&{membre}>"}
        ]

        # Embed pour les commandes admin
        embed_admin = discord.Embed(
            title="🔧 Commandes Admin",
            description="Liste des commandes réservées aux membres du staff :",
            color=discord.Color.red()
        )
        for command in admin_commands:
            embed_admin.add_field(
                name=command["command"],
                value=f"**Description :** {command['description']}\n**Rôle requis :** {command['role']}",
                inline=False
            )

        # Embed pour les autres commandes
        embed_user = discord.Embed(
            title="🔹 Commandes Utilisateurs",
            description="Liste des commandes accessibles aux membres :",
            color=discord.Color.blue()
        )
        for command in user_commands:
            embed_user.add_field(
                name=command["command"],
                value=f"**Description :** {command['description']}\n**Rôle requis :** {command['role']}",
                inline=False
            )

        # Envoi des embeds
        await interaction.response.send_message(embeds=[embed_admin, embed_user])

async def setup(bot):
    await bot.add_cog(Help(bot))
