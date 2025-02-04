import discord
from discord.ext import commands
import json
import os

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

    def get_xp_for_next_level(self, level):
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

        while user_data['xp'] >= self.get_xp_for_next_level(user_data['level']):
            user_data['xp'] -= self.get_xp_for_next_level(user_data['level'])
            user_data['level'] += 1
            self.save_data(data)
            return user_data['level']

        self.save_data(data)
        return None

    def create_xp_bar(self, xp, max_xp):
        # Calculer la progression de la barre d'XP
        progress = int((xp / max_xp) * 20)
        bar = '□' * progress + '■' * (20 - progress)
        return f'[{bar}]'

    async def send_level_up_embed(self, user, level, xp, max_xp, server_id):
        data = self.load_data()
        xp_log_channel_id = data.get(server_id, {}).get('xp_log_channel')

        if xp_log_channel_id:
            channel = self.bot.get_channel(xp_log_channel_id)
            if channel:
                embed = discord.Embed(title=f"Niveau {level} atteint !", color=discord.Color.green())
                embed.set_thumbnail(url=user.avatar.url)
                embed.add_field(name="Membre", value=user.mention, inline=False)
                embed.add_field(name="Niveau", value=level, inline=False)
                embed.add_field(name="Barre d'XP", value=self.create_xp_bar(xp, max_xp), inline=False)
                await channel.send(embed=embed)

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
            await self.send_level_up_embed(message.author, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

        # Ajouter XP pour une réponse
        if message.reference and message.reference.resolved:
            new_level = self.update_xp(server_id, user_id, 1)
            if new_level:
                data = self.load_data()
                user_data = data[server_id][user_id]
                await self.send_level_up_embed(message.author, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

        # Ajouter XP pour une interaction avec un emoji
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != message.author:
                    new_level = self.update_xp(server_id, str(user.id), 1)
                    if new_level:
                        data = self.load_data()
                        user_data = data[server_id][str(user.id)]
                        await self.send_level_up_embed(user, new_level, user_data['xp'], self.get_xp_for_next_level(new_level), server_id)

async def setup(bot):
    await bot.add_cog(XPMessageEvents(bot))