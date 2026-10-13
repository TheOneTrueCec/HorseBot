import os
import configparser
import discord
from discord.ext import tasks, commands
from discord import app_commands
import datetime
import peewee

SERVER = os.getenv("SERVER")
LOGS = os.getenv("LOGS")


config = configparser.ConfigParser(interpolation=None)
config.read("./config.yaml")

DATABASE = peewee.SqliteDatabase(config.get("General", "database"), pragmas={'journal_mode': 'wal'})
MODROLE = int(config.get("General", "moderator"))
HONEYPOT = int(config.get("General", "honeypot"))
YAMIKS = int(config.get("General", "yamiks"))

class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        DATABASE.create_tables([Banned])

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.wait_until_ready()
        self.updateStatus.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        guild: discord.guild.Guild = await self.bot.fetch_guild(SERVER)
        if message.author == self.bot.user:
            return
        elif message.author == YAMIKS:
            return

        try:
            MOD: discord.role.Role = guild.get_role(MODROLE)
            # if MOD in message.author.roles:
            #     return
        except:
            pass

        if message.channel.id == HONEYPOT:
            user: discord.member.Member = await guild.fetch_member(message.author.id)
            # honey_channel = await self.bot.fetch_channel(HONEYPOT) 
            # await honey_channel.send("Bang")
            try:
                await user.ban(delete_message_days=1, reason="Scam Bot")
                Banned.insert(discordid=int(user.id), banDate=datetime.datetime.now()).execute()
            except discord.errors.Forbidden:
                await user.timeout(datetime.timedelta(minutes=1), reason="Poor Soul Got Hacked")
                await message.delete()

    @tasks.loop(hours=1)
    async def updateStatus(self):
        bancount = len(Banned.select())
        game = discord.Game(f'with {bancount} banned players')
        await self.bot.change_presence(status=None, activity=game)


async def setup(bot: commands.Bot):
    await bot.add_cog(ManagementCog(bot))


class Banned(peewee.Model):
    discordid = peewee.IntegerField()
    banDate = peewee.DateField()

    class Meta:
        database = DATABASE