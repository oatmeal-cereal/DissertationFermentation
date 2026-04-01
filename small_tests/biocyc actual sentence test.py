import requests
import json
import urllib.parse
from xml.etree import ElementTree as ET
import random
import time

sentence = 'it has been shown that S. cerevisiae could grow in milk and produce small amounts of ethanol, glycerol, and lactic acid'

microbes = ['Saccharomyces cerevisiae']

compounds = ['glycerol', 'butyric acid']

with open('..\\..\\dissertation DLC content\\go away\\passwords.json', 'r') as f:
    passwords = json.load(f)
    password = passwords.get('metacyc_pw')
    
with open('..\\list_files\\biocyc_db_mappings.json', 'r', encoding='utf-8') as f:
    db_mappings = json.load(f)

email = 'lp2095@bath.ac.uk'

session = requests.Session()

session.post('https://websvc.biocyc.org/credentials/login/', data={'email':email, 'password':password})

def process_comp(comp):
    replace_chars = [' ', '.', '?', '!', ',', '\\', '/']
    for char in replace_chars:
        comp = comp.replace(char, '')
    return comp

for microbe in microbes:
    for comp in compounds:
        dbs = db_mappings[microbe]
        if len(dbs) == 1:
            db_values = dbs.values()
            database = list(db_values)[0]
        else:
            db_values = dbs.values()
            database = random.choice(list(db_values))
        comp = process_comp(comp)
        comp_resp = session.get(f'https://websvc.biocyc.org/{database}/name-search?object={comp}&class=Compounds&fmt=json').json()

        if not comp_resp.get('RESULTS'):
            continue
        
        comp_resp = comp_resp.get('RESULTS')[0]
        
        time.sleep(1)
        
        comp_id = comp_resp.get('OBJECT-ID')

        utilisation = session.get(f'https://websvc.biocyc.org/getxml?{database}:{comp_id}&fmt=json')
        
        util_xml = ET.fromstring(utilisation.text).find('Compound')
        
        lefts = util_xml.find('appears-in-left-side-of')
        
        if not lefts == None:
            #add a relation that the microbe consumes the chemical as a substrate
            for reaction in lefts:
                reaction_id = reaction.get('frameid')
                print("reaction:", reaction_id)

                enzymes_resp = session.get(f"https://websvc.biocyc.org/apixml?fn=enzymes-of-reaction&id={database}:{reaction_id}")

                time.sleep(1)

                enzymes_xml = ET.fromstring(enzymes_resp.text)

                proteins = enzymes_xml.findall('Protein')

                for protein in proteins:

                    print(protein.find('common-name').text)
                    print(protein.get('frameid'))

                    """ enzreactions = protein.find('catalyzes')
                    for reaction in enzreactions:
                        enzyme_id = reaction.find('enzyme').find('Protein').get('frameid')

                        name_resp = session.get(f'https://websvc.biocyc.org/getxml?{database}:{enzyme_id}')

                        name_xml = ET.fromstring(name_resp.text)

                        print(name_xml.find('Protein').find('common-name').text)

                        time.sleep(1) """

                print()
        
        rights = util_xml.find('appears-in-right-side-of')
        
        if not rights == None:
            #add a relation that the microbe produces this metabolite
            pass
        
        """ for right in rights:
            print(right.get('frameid')) """
        
        time.sleep(1)