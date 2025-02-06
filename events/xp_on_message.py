import discord
from discord.ext import commands
import json
import os
from utils.utils import create_xp_card

class XPMessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_file = 'data/data.json'

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, data):
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def get_xp_for_next_level(level):
        if level == 0:
            return 1
        elif level == 1:
            return 50
        else:
            return int(50 * (1.3 ** (level - 1)))

    def update_xp(self, server_id, user_id, xp_gain):
        data = self.load_data()
        if server_id not in data:
            data[server_id] = {}
        if user_id not in data[server_id]:
            data[server_id][user_id] = {'xp': 0, 'level': 0}

        user_data = data[server_id][user_id]
        user_data['xp'] += xp_gain

        leveled_up = False
        while user_data['xp'] >= self.get_xp_for_next_level(user_data['level']):
            user_data['xp'] -= self.get_xp_for_next_level(user_data['level'])
            user_data['level'] += 1
            leveled_up = True

        self.save_data(data)  # On sauvegarde après toutes les mises à jour

        return user_data['level'] if leveled_up else None

    async def send_level_up_image(self, user, level, xp, max_xp, server_id):
        """Envoie l'image de la carte d'XP."""
        data = self.load_data()
        xp_log_channel_id = data.get(server_id, {}).get('xp_log_channel')

        print(f"XP Log Channel ID: {xp_log_channel_id}")  # Debug
        if xp_log_channel_id:
            channel = self.bot.get_channel(xp_log_channel_id)
            print(f"Channel trouvé : {channel}")  # Debug

            if channel:
                xp_card_image = create_xp_card(user, level, xp, max_xp)
                try:
                    await channel.send(file=xp_card_image)
                    print("Image envoyée avec succès.")
                except discord.HTTPException as e:
                    print(f"Erreur lors de l'envoi de l'image : {e}")
            else:
                print("Erreur : Le canal n'a pas été trouvé.")
        else:
            print("Erreur : Le canal de logs XP n'est pas défini.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        server_id = str(message.guild.id)
        user_id = str(message.author.id)

        # Ajouter XP pour un message envoyé
        new_level = self.update_xp(server_id, user_id, 2)
        if new_level:
            data = self.load_data()
            user_data = data[server_id][user_id]
            print(f"User data: {user_data}")  # Debug
            await self.send_level_up_image(message.author, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

        # Ajouter XP pour une réponse
        if message.reference and message.reference.resolved:
            new_level = self.update_xp(server_id, user_id, 1)
            if new_level:
                data = self.load_data()
                user_data = data[server_id][user_id]
                print(f"User data: {user_data}")  # Debug
                await self.send_level_up_image(message.author, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

        # Ajouter XP pour une interaction avec un emoji
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != message.author:
                    new_level = self.update_xp(server_id, str(user.id), 1)
                    if new_level:
                        data = self.load_data()
                        user_data = data[server_id][str(user.id)]
                        print(f"User data: {user_data}")  # Debug
                        await self.send_level_up_image(user, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

async def setup(bot):
    await bot.add_cog(XPMessageEvents(bot))
