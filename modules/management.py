import os
import configparser
import discord
from discord.ext import tasks, commands
from discord import app_commands

SERVER = os.getenv("SERVER")
LOGS = os.getenv("LOGS")


config = configparser.ConfigParser(interpolation=None)
config.read("./config.yaml")

HONEYPOT = int(config.get("General", "honeypot"))

class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        guild: discord.guild.Guild = await self.bot.fetch_guild(SERVER)
        if message.author == self.bot.user:
            return
        
        if message.channel.id == HONEYPOT:
            user: discord.member.Member = await guild.fetch_member(message.author.id)
            # honey_channel = await self.bot.fetch_channel(HONEYPOT) 
            # await honey_channel.send("Bang")
            await user.ban(delete_message_days=1, reason="Scam Bot")

async def setup(bot: commands.Bot):
    await bot.add_cog(ManagementCog(bot))