import discord
from discord import app_commands
from discord.ext import commands

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="botinfo", description="donne les info de CeasarP")
    async def botinfo_slash(self, interaction: discord.Interaction):
        bot_creator_id = 426377537606778881
        creator_mention = f"<@{bot_creator_id}>"
        message = f"Le Bot {self.bot.user} a été créé par {creator_mention}.\nSi vous trouvez un bug, merci de me contacter en message privé."
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
