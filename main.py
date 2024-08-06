import api

import discord
import discord.ext
import dotenv
import os

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')

client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'connection with {client.user} established')

@tree.command(name="fixtures", description="prints fixtures for selected gw")
@discord.app_commands.describe(
    gw="gameweek # to print fixtures from; leave blank for current gw"
)
async def fixtures(interaction: discord.Interaction, gw:int):
    if gw:
        fixtures = api.gameweekFixtures(gw)
    else:
        fixtures = api.gameweekFixtures(1)
        
    embed = discord.Embed()
    for match in fixtures:
        embed.add_field(name=f"{match['homeTeam']} vs. {match['awayTeam']}", value={match['dateTime']})
    await interaction.response.send_message(embed=embed)
        
client.run(TOKEN)