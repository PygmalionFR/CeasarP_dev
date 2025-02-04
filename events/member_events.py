import discord
from discord.ext import commands
import json
import os

class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_data = self.load_server_data()

    def load_server_data(self):
        if os.path.exists('data/servers.json'):
            with open('data/servers.json', 'r') as f:
                return json.load(f)
        return {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        server_id = str(member.guild.id)

        if server_id in self.server_data:
            welcome_channel_id = self.server_data[server_id].get('welcome_channel_id')
            general_channel = self.bot.get_channel(welcome_channel_id)

            if general_channel:
                embed = discord.Embed(
                    title=f"Bienvenue {member.display_name} sur {member.guild.name} ! ",
                    description=f"Je t'invite à te présenter ici <#1109914485055037520> \n et à lire le règlement dans <#1109265365906763837>"
                )
                embed.set_thumbnail(
                    url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Fstickers%2F863087410577014805.png&w=128&q=75"
                )
                await general_channel.send(embed=embed)
            else:
                print("Le canal de bienvenue n'a pas été défini correctement.")
        else:
            print("Erreur : Données du serveur non trouvées.")

async def setup(bot):
    await bot.add_cog(MemberEvents(bot))
