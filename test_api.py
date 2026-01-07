import requests
from decouple import config

api_key=config("api_key")
# api_key=""

# AVIAPAGES_BASE_URL = "https://api.aviapages.com/v1/"

AVIAPAGES_API_KEY = api_key



# AVIAPAGES_BASE_URL = "https://api.aviapages.com/v3/" #charter_quotes
AVIAPAGES_BASE_URL="https://dir.aviapages.com/api/"     #availabilities
# AVIAPAGES_BASE_URL="https://aviapages.com/"
AVIAPAGES_API_KEY =api_key

def call_aviapages_api(endpoint):
    url = f"{AVIAPAGES_BASE_URL}{endpoint}"
    
    headers = {
        "Authorization": f"Token {AVIAPAGES_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    } 

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()



response = call_aviapages_api("charter_aircraft/")
print(response)
