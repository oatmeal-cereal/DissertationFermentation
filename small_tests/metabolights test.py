import requests

base_url = 'https://www.ebi.ac.uk:443/metabolights/'

glucose_id = 'CHEBI:17234'
lactic_acid_id = 'CHEBI:42111'
xylitol_id = 'CHEBI:17151'

response = requests.post(base_url + 'ws/chebi-v2/search', params={'query': 'lactic acid'})

print(response)