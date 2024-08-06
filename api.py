import requests
import dotenv
import os
import time

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')


def gameweekFixtures(gameweek: int) -> list:
    headers = {"X-Auth-Token": API_KEY}
    fixtures = requests.get(f'http://api.football-data.org/v4/competitions/PL/matches?matchday={gameweek}', headers=headers).json()
    matches = list()
    for match in fixtures['matches']:
        details = {}
        details['homeTeam'] = match['homeTeam']['shortName']
        details['awayTeam'] = match['awayTeam']['shortName']
        details['dateTime'] = match['utcDate']
        matches.append(details)
    return matches

def gameweekResults(gameweek: int) -> list:
    headers = {"X-Auth-Token": API_KEY}
    fixtures = requests.get(f'http://api.football-data.org/v4/competitions/PL/matches?matchday={gameweek}', headers=headers).json()
    results = []
    for result in fixtures['matches']:
        results.append(result['score']['winner'])
    return results

