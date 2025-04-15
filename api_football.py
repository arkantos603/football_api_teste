import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

headers = {
    "x-apisports-key": API_KEY
}

def get_leagues():
    url = f"{BASE_URL}/leagues"
    response = requests.get(url, headers=headers)
    return response.json()["response"]

def get_fixtures(league_id, season):
    url = f"{BASE_URL}/fixtures?league={league_id}&season={season}"
    response = requests.get(url, headers=headers)
    return response.json()["response"]
