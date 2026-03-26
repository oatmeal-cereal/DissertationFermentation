import requests
import json
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

with open('..\\..\\dissertation DLC content\\go away\\passwords.json', 'r') as f:
    passwords = json.load(f)
    password = passwords.get('metacyc_pw')

email = 'lp2095@bath.ac.uk'

session = requests.Session()
# Post login credentials to session:
#session.post('https://websvc.biocyc.org/credentials/login/', data={'email':email, 'password':password})
# Issue web service request:
response = session.get('https://websvc.biocyc.org/META/substring-search', params={'object': 'lactic acid'})

soup = BeautifulSoup(response.content, 'html.parser')

text = ''

for item in soup.find_all('table'):
    print(item)

#print(summary)