import os
import sys
import configparser
import discord
from discord import app_commands
from discord.ext import tasks, commands
import discord.ext.commands
from dotenv import load_dotenv

import asyncio

# utc = datetime.timezone.utc

#Constants
FILEPATH = os.path.dirname(__file__)
os.system('color')

# region Instantiation
if __name__ == "__main__":

    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    SERVER = os.getenv("SERVER")
    LOGS = os.getenv("LOGS")

    config = configparser.ConfigParser(interpolation=None)
    config.read("./config.yaml")

    intents = discord.Intents.default()
    # intents.message_content = True
    # intents.members = True
    client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.tree.sync()

    print("---Ready---")

# endregion

async def load_extensions():
    """Load all modules/extensions/cogs from specificed directories"""
    dir_list = ['modules']
    exclusion_list = ['help']
    for dir_ in dir_list:
        print(f'=== Attempting to load all extensions in {dir_} directory ...')
        for filename in os.listdir(f'./{dir_}'):
            module = filename[:-3]
            if filename.endswith('.py') and module not in exclusion_list:
                try:
                    await client.load_extension(f'{dir_}.{module}')
                    print(f'\tSuccessfully loaded extension: {module}')
                except Exception as err:
                    exc = f'{type(err).__name__}: {err}'
                    print(f'\tFailed to load extension:  {module}\n\t\t{exc}')
    for excl_module in exclusion_list:
        print(f'=== Excluding the extension: {excl_module}')


def log_in():
    """Login function"""
    print('=== Initializing startup sequence ...')
    asyncio.run(load_extensions())
    print('=== Attempting to log in to bot ...')
    try:
        client.run(TOKEN) #Keep at the end of the file
    except discord.errors.HTTPException or discord.errors.LoginFailure as error:
        print('\nDiscord: Unsuccessful login:', error)
    else:
        sys.exit("Login Unsuccessful")

log_in()