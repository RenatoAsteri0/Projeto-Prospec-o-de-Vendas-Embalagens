import requests
import time
import random
from os import getenv
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = getenv("API_KEY_GOOGLE_SCRAPY")
ACTOR_ID = "boztek-ltd~google-maps-scraper"

SEARCH_TERMS = [
    "industria alimenticia",
    "industria farmaceutica",
    "industria quimica",
    "fabricante de alimentos",
    "industria de cosmeticos",
]

CITIES = [
    "Campinas, São Paulo, Brazil"
    "Indaiatuba, São Paulo, Brazil",
    "Sorocaba, São Paulo, Brazil",
    "Hortolandia, São Paulo, Brazil",
    "Itu, São Paulo, Brazil",
    "Jundiai, São Paulo, Brazil",
]


def extract_places():
    # gerar buscas
    search_strings = []

    for city in CITIES:
        for term in SEARCH_TERMS:
            search_strings.append(f"{term} {city}")

    payload = {
        "searchStringsArray": search_strings,
        "maxCrawledPlacesPerSearch": 10,
        "language": "pt-BR"
    }

    # iniciar scraping
    run_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"
    response = requests.post(run_url, json=payload)
    run_data = response.json()
    run_id = run_data["data"]["id"]

    print("Run iniciado:", run_id)

    # verificar status
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"

    while True:
        status = requests.get(status_url).json()
        state = status["data"]["status"]

        print("Status:", state)

        if state == "SUCCEEDED":
            dataset_id = status["data"]["defaultDatasetId"]
            break
        elif state in ["FAILED", "ABORTED"]:
            raise Exception("Scraping falhou")

        time.sleep(10)

    # baixar dataset
    dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?clean=true"

    data = requests.get(dataset_url).json()
    print("Total encontrado:", len(data))

    # pegar apenas 50 aleatórios
    if len(data) > 50:
        data = random.sample(data, 50)

    print("Amostra final:", len(data))

    return data