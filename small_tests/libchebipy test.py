from libchebipy import ChebiEntity
import requests

glucose_id = 'CHEBI:17234'

chebi_api_base_url = 'https://www.ebi.ac.uk/chebi/backend/api/public/es_search'

glucose_comp = ChebiEntity(glucose_id)

print(glucose_comp.get_names())