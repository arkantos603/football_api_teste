import requests
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

# Retorna todas as ligas disponíveis na API
def get_leagues():
    url = f"{BASE_URL}/leagues"
    res = requests.get(url, headers=headers)
    return res.json()["response"]

# Retorna as temporadas disponíveis para uma liga específica
def get_seasons_for_league(league_id):
    url = f"{BASE_URL}/leagues?id={league_id}"
    res = requests.get(url, headers=headers)
    data = res.json()["response"]
    if data:
        return data[0]["seasons"]
    return []

# Retorna as partidas (fixtures) de uma liga em uma temporada específica
def get_fixtures(league_id, season):
    url = f"{BASE_URL}/fixtures?league={league_id}&season={season}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("Erro ao buscar partidas:", res.text)
        return []
    return res.json()["response"]

# Retorna as partidas (fixtures) que acontecem na data atual
def get_fixtures_today():
    today = date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print("Erro:", response.text)
        return []

# Retorna os times de uma liga em uma temporada específica
def get_teams_for_league(league_id, season):
    url = f"{BASE_URL}/teams?league={league_id}&season={season}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()["response"]
    else:
        print("Erro ao buscar times:", res.text)
        return []

# Retorna as estatísticas de uma partida (fixture) específica
def get_statistics_for_fixture(fixture_id):
    url = f"{BASE_URL}/fixtures/statistics?fixture={fixture_id}"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json()["response"]
    else:
        print("Erro ao buscar estatísticas:", res.text)
        return []