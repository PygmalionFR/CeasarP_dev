import discord
from discord import app_commands
from discord.ext import commands
import datetime

ts = int(datetime.datetime.utcnow().timestamp())

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Débannir un utilisateur !")
    @app_commands.describe(user="Le membre à débannir")
    async def unban_slash(self, interaction: discord.Interaction, user: str):
        server_id = str(interaction.guild.id)

        if server_id in server_data:
            log_channel_id = server_data[server_id].get('log_channel_id')
            log = interaction.guild.get_channel(log_channel_id)
        else:
            await interaction.response.send_message("Erreur : Données du serveur non trouvées.", ephemeral=True)
            return

        userName = user
        banned_users = await interaction.guild.bans()

        for banned_user in banned_users:
            if banned_user.user.name == userName:
                await interaction.guild.unban(banned_user.user)

                embed = discord.Embed(title="Unban", description="Un modérateur a débanni un membre", color=discord.Color.green())
                embed.add_field(name="`Membre Information` :", value=f"`Utilisateur` : {banned_user.user.mention}\n `Date` : <t:{ts}:R>\n `Modérateur responsable` : {interaction.user.mention}")
                embed.timestamp = datetime.datetime.now()

                await interaction.response.send_message(embed=embed)
                await log.send(embed=embed)
                return

        await interaction.response.send_message(f"L'utilisateur {user} n'est pas dans la liste des bannis.")

async def setup(bot):
    await bot.add_cog(Unban(bot))
