import discord
from discord.ext import commands
from utils.utils import get_db_connection  # Fonction de connexion à la BDD
from events.setup_channel import setup_welcome_channel  # Import de la fonction utilitaire

class BotJoinServer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Quand le bot rejoint un serveur"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Création de la table si elle n'existe pas
            create_table_query = """
            CREATE TABLE IF NOT EXISTS servers (
                server_id BIGINT PRIMARY KEY,
                owner_id BIGINT NOT NULL,
                welcome_channel_id BIGINT NULL,
                log_channel_id BIGINT NULL,
                film_id BIGINT NULL,
                first_msg BOOLEAN DEFAULT FALSE,
                fondateur_id BIGINT NULL,
                admin_id BIGINT NULL,
                modo_id BIGINT NULL,
                membreplus_id BIGINT NULL,
                membre_id BIGINT NULL
            );
            """
            cursor.execute(create_table_query)
            conn.commit()

            # Vérifier si le serveur est déjà enregistré
            cursor.execute("SELECT COUNT(*) FROM servers WHERE server_id = %s", (guild.id,))
            exists = cursor.fetchone()[0] > 0

            if not exists:
                # Insérer les infos du serveur
                insert_query = """
                INSERT INTO servers (server_id, owner_id) VALUES (%s, %s)
                """
                cursor.execute(insert_query, (guild.id, guild.owner.id))
                conn.commit()

            # Vérifier si le message de setup a déjà été envoyé
            cursor.execute("SELECT first_msg FROM servers WHERE server_id = %s", (guild.id,))
            first_msg = cursor.fetchone()[0]

            if not first_msg:
                await setup_welcome_channel(guild)  # Déplacement dans setup_channel.py

                # Mettre à jour 'first_msg' à True
                cursor.execute("UPDATE servers SET first_msg = TRUE WHERE server_id = %s", (guild.id,))
                conn.commit()

        except Exception as e:
            print(f"Erreur lors de l'ajout du serveur {guild.id} : {e}")

        finally:
            cursor.close()
            conn.close()

        print(f"Serveur ajouté : {guild.id} avec propriétaire {guild.owner.id}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """Quand le bot quitte un serveur"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM servers WHERE server_id = %s", (guild.id,))
            conn.commit()

            print(f"Serveur supprimé de la base de données : {guild.id}")

        except Exception as e:
            print(f"Erreur lors de la suppression du serveur {guild.id} : {e}")

        finally:
            cursor.close()
            conn.close()

async def setup(bot):
    await bot.add_cog(BotJoinServer(bot))
