import api

import discord
import discord.ext
import dotenv
import os

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)