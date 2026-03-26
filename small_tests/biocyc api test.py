import requests
from xml.etree import ElementTree
import json
from biocyc import biocyc

random_db = 'LACI891391'

biocyc.set_organism(random_db)

o = biocyc.find_compound_by_name('d-lactate')

print(o)

with open('..\\..\\dissertation DLC content\\go away\\passwords.json', 'r') as f:
    passwords = json.load(f)
    password = passwords.get('metacyc_pw')

email = 'lp2095@bath.ac.uk'

session = requests.Session()

session.post('https://websvc.biocyc.org/credentials/login/', data={'email':email, 'password':password})

""" response = requests.get("https://websvc.biocyc.org/xmlquery?dbs")

xml_resp = ElementTree.fromstring(response.text)

print(xml_resp.findall('species')) """

#response = requests.get("https://websvc.biocyc.org/xmlquery?[x:y<-dbs, x<-y^^compounds, x^name=\"lactic acid\"]")

response = session.get(f"https://websvc.biocyc.org/apixml?fn=get-class-all-instances&id={random_db}:Compounds&detail=none")

print(response.text)