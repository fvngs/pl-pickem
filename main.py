import api_handler

import json
import os
import dotenv

import discord
from discord.ext import commands, tasks
from discord import app_commands

dotenv.load_dotenv('secret.env')
TOKEN = os.getenv('TOKEN')

gameweek = api_handler.get_gw()

if not TOKEN:
    raise ValueError("Please make sure you have a valid secret.env file with a TOKEN declared!")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

with open('fixtures.json', 'r') as f:
    fixtures = json.load(f)
    
@client.event
async def on_ready():
    await tree.sync()
    print(f'Connection established with {client.user}')
    
@tasks.loop(hours=24)
async def gameweek_check():
    global gameweek
    gameweek = api_handler.get_gw()
    
@tree.command(name="fixture", description="Prints out the fixtures for the current gameweek")
async def fixture(interaction: discord.Interaction):
    embed = discord.Embed(title=f"Fixtures for Game Week {gameweek}", color=discord.Color.blue())

    if gameweek > 0 and gameweek <= len(fixtures):
        matchday_fixtures = fixtures[gameweek - 1]
        for match in matchday_fixtures['matches']:
            home_team = match['homeTeam']
            away_team = match['awayTeam']
            match_date = match['utcDate'].replace("T", " ").replace("Z", " ")
            embed.add_field(
                name=f"{home_team} vs {away_team}",
                value=f"Date: {match_date}",
                inline=False
            )
    else:
        embed.add_field(name="Error", value="No fixtures available for the current game week.", inline=False)

    # Send the embed
    await interaction.response.send_message(embed=embed)
    
client.run(TOKEN)