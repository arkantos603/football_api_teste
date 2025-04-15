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

def get_leagues():
    url = f"{BASE_URL}/leagues"
    res = requests.get(url, headers=headers)
    return res.json()["response"]

def get_seasons_for_league(league_id):
    url = f"{BASE_URL}/leagues?id={league_id}"
    res = requests.get(url, headers=headers)
    data = res.json()["response"]
    if data:
        return data[0]["seasons"]
    return []

def get_fixtures(league_id, season):
    url = f"{BASE_URL}/fixtures?league={league_id}&season={season}"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("Erro ao buscar partidas:", res.text)
        return []
    return res.json()["response"]

def get_fixtures_today():
    today = date.today().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print("Erro:", response.text)
        return []
