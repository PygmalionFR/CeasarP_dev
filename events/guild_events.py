import discord
from discord.ext import commands
import json
import os

class GuildEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = self.load_server_data()

    def load_server_data(self):
        if os.path.exists('data/servers.json'):
            with open('data/servers.json', 'r') as f:
                return json.load(f)
        return {}

    def save_server_data(self):
        with open('data/servers.json', 'w') as f:
            json.dump(self.server_data, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        server_id = str(guild.id)
        owner_id = guild.owner_id

        # Vérifier si le serveur est déjà dans les données
        if server_id not in self.server_data:
            self.server_data[server_id] = {
                'owner_id': owner_id,
                'welcome_channel_id': None,
                'log_channel_id': None,
                'film_id': None,
                'first_msg': False,
                'fondateur_id': None,
                'admin_id': None,
                'modo_id': None,
                'membreplus_id': None,
                'membre_id': None
            }
            self.save_server_data()

            # Créer un canal visible uniquement par le propriétaire du serveur
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),  # Assure que le bot peut lire les messages
                guild.owner: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await guild.create_text_channel('bot-setup', overwrites=overwrites)

            # Embed de configuration
            embed_setup = discord.Embed(
                title="⚙️ Configuration du bot",
                description="Merci de m'avoir ajouté à votre serveur ! Voici comment configurer le bot en quelques étapes :",
                color=discord.Color.green()
            )

            embed_setup.add_field(
                name="1️⃣ Configurer les canaux de logs",
                value=(
                    "• **/setxplog** → Canal pour les logs d'XP.\n"
                    "• **/setlog** → Canal pour les logs du serveur.\n"
                    "• **/setwelcome** → Canal pour les messages de bienvenue."
                ),
                inline=False
            )

            embed_setup.add_field(
                name="2️⃣ Définir les 5 rôles **Fondateur**,**Admin** ,**Modérateur**, **MembrePlus** et **Membre**",
                value="Utilisez **/setrole** pour attribuer les rôles aux membres.\n ‼️⚠️‼️Veuillez Crée les 5 rôles avant de faire cette commande ‼️⚠️‼️\n le `@everyone` peux être utiliser pour le /setrole membre @everyone",
                inline=False
            )

            embed_setup.set_footer(text="Une fois ces étapes complétées, votre bot sera prêt à l'emploi ! 🚀")

            # Envoyer le message de configuration dans le canal
            await channel.send(embed=embed_setup)

            # Mettre à jour la valeur 'first_msg' à True
            self.server_data[server_id]['first_msg'] = True
            self.save_server_data()

        print(f'Serveur ajouté : {server_id} avec propriétaire {owner_id}')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        server_id = str(guild.id)

        if server_id in self.server_data:
            del self.server_data[server_id]
            self.save_server_data()
            print(f'Serveur supprimé : {server_id}')

async def setup(bot):
    await bot.add_cog(GuildEvents(bot))
