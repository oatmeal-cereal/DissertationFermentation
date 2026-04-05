import requests
import json

email = 'lp2095@bath.ac.uk'

with open('..\\..\\dissertation DLC content\\go away\\passwords.json', 'r') as f:
    passwords = json.load(f)
    password = passwords.get('metacyc_pw')

session = requests.Session()

lactococcuslactis = 'GCF_003627395'

session.post('https://websvc.biocyc.org/credentials/login/', data={'email':email, 'password':password}, headers={'User-Agent': 'A University of Bath student. I am doing a dissertation project in Natural Language Processing, where I identify named entities such as microbes and chemicals in academic papers, and the relations between them. I am using the database for the relation extraction element, and whether a microbe consumes or produces a particular chemical.'})

#resp = session.get('https://websvc.biocyc.org/xmlquery?[x:x<-META^^compounds]')
resp = session.get(f'https://websvc.biocyc.org/xmlquery?query=[x:x<-{lactococcuslactis}^^compounds, "lactic acid" instringci x^names]&detail=low')
print(resp)
print(resp.text)