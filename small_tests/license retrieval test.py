import requests

base_url = "https://api.crossref.org/licenses"

params = {
    'query': 'food fermentation'
}

response = requests.get(f"{base_url}", params=params)
if response.status_code == 200:
    print(response.json())