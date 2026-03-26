import obonet
import pyobo
import requests


api_key = 'fee2907a-94b1-4f06-b0c3-4236098930f9'

data = requests.get(f'https://data.bioontology.org/search?q=Lactobacillus+acidophilus&ontology=NCBITAXON&apikey={api_key}')
#onto = pyobo.from_obo_path('..\\..\\dissertation DLC content\\ncbitaxon.obo', version=)
#onto = obonet.read_obo('..\\..\\dissertation DLC content\\ncbitaxon.obo')

print(data.content)