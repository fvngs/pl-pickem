import requests
import os
import json
import dotenv

dotenv.load_dotenv('secret.env')
key = os.getenv('API_KEY')

def get_fixtures() -> bool:
    if not os.path.isfile('fixtures.json'):
        response = requests.get(
            "https://api.football-data.org/v4/competitions/PL/matches", 
            headers={'X-Auth-Token': key}
        ).json()

        fixtures = []
        current_matchday = 0
        matchday_fixtures = []

        for match in response['matches']:
            match_info = {
                'homeTeam': match['homeTeam']['name'],
                'awayTeam': match['awayTeam']['name'],
                'utcDate': match['utcDate'],
                'status': match['status']
            }

            if int(match['matchday']) > current_matchday:
                if matchday_fixtures:
                    fixtures.append({
                        'matchday': current_matchday,
                        'matches': matchday_fixtures
                    })
                current_matchday = int(match['matchday'])
                matchday_fixtures = []

            matchday_fixtures.append(match_info)

        if matchday_fixtures:
            fixtures.append({
                'matchday': current_matchday,
                'matches': matchday_fixtures
            })

        with open('fixtures.json', 'w') as f:
            json.dump(fixtures, f, indent=4)

        print("Fixtures have been saved to fixtures.json")
        return True
    else:
        print("fixtures.json already exists")
        return False

def get_gw() -> int:
    response = requests.get(
            "https://api.football-data.org/v4/competitions/PL/", 
            headers={'X-Auth-Token': key}
        ).json()
    return response['currentSeason']['currentMatchday']