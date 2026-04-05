import requests
import json
import urllib.parse
from xml.etree import ElementTree as ET
import random
import time

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

microbes = ['Saccharomyces cerevisiae', 'Lactococcus lactis', 'Lactiplantibacillus plantarum', 'Oenococcus oeni', 'Clostridium butyricum']
#microbes = ['Saccharomyces cerevisiae']

#compounds = ['glycerol', 'butyric acid', 'lactic acid', 'lactate', 'malic acid', 'r-lactic acid']
""" compounds = {
    'Saccharomyces cerevisiae': ['glycerol', 'glucose', 'acetic acid'],
    'Lactococcus lactis': ['lactic acid', 'lactate', 'r-lactic acid'],
    'Lactiplantibacillus plantarum': ['lactic acid', 'lactate', 'r-lactic acid'],
    'Oenococcus oeni': ['malic acid', 'l-malic acid', 'l-malate', 'r-lactic acid', 'lactate'],
    'Clostridium butyricum': ['butyric acid', 'lactate', 'acetate', 'lactic acid']
} """

compounds = {
    #'Saccharomyces cerevisiae': ['glycerol', 'acetic acid', 'glucose'],
    #'Lactococcus lactis': ['r-lactic acid', 'lactate'],
    'Oenococcus oeni': ['r-lactic acid', 'r-lactate']
}

results = []

logs = []

def process_log(log):
    print(log)
    logs.append(log + '\n')

#microbe index and name
for microbe in microbes:
    mic_chems = compounds.get(microbe)
    if not mic_chems:
        continue
    for chem in mic_chems:
        dbs = db_mappings.get(microbe)
        if not dbs:
            process_log('database not found for: {microbe}')
            continue
        if len(dbs) == 1:
            db_values = dbs.values()
            database = list(db_values)[0]
        else:
            db_values = dbs.values()
            database = random.choice(list(db_values))

        process_log(f"microbe name: {microbe}, chemical name: {chem}")
        process_log(f'database id: {database}')

        chem = process_comp(chem)
        chem_resp = session.get(f'https://websvc.biocyc.org/{database}/name-search?object={chem}&class=Compounds&fmt=json').json()

        if not chem_resp.get('RESULTS'):
            process_log(f"no chemical name found under microbe {microbe}")
            continue
        
        chem_resp = chem_resp.get('RESULTS')[0]
        
        time.sleep(1)
        
        chem_id = chem_resp.get('OBJECT-ID')

        if not chem_id:
            continue

        try:
            process_log(f"trying: {database}, {chem}, {chem_id}")
            chem_reactions_resp = session.get(f"https://websvc.biocyc.org/apixml?fn=reactions-of-compound&id={database}:{chem_id}&detail=full")
            time.sleep(1)
        except:
            print("failed")
            continue

        try:
            reactions_xml = ET.fromstring(chem_reactions_resp.text)
        except:
            process_log(f"failed chemical: {chem}")
            print(chem_reactions_resp.reason)
            continue

        reactions = reactions_xml.findall('Reaction')

        if not reactions:
            process_log(f"no reactions found for {microbe} and {chem}")
            continue

        left_found = right_found = False

        for reaction in reactions:
            enzrxns = reaction.find('enzymatic-reaction')
            try:
                enzs = enzrxns.findall('Enzymatic-Reaction')
                enzymes = []
                for enz in enzs:
                    if enz.find('common-name'):
                        enzymes.append(enz.find('common-name'))
                process_log(f"enzymes: {enzymes}")
            except:
                process_log(f"{enzrxns} has no reactions")
                continue

            direction = reaction.findtext('reaction-direction')

            if not direction:
                direction = 'LEFT-TO-RIGHT'

            def get_left_right_ids(direction):
                lr_ids = []
                for lr in reaction.findall(direction):
                    try:
                        lr_ids.append(lr.find('Compound').get('frameid'))
                    except:
                        process_log(f"what the hell kind of compound wouldnt have a frameid huh?? oh, {lr.find('Compound')}")
                return lr_ids
            
            left_label = right_label = None
            
            if 'LEFT-TO-RIGHT' in direction or direction == 'REVERSIBLE':
                left_label = 'left'
                right_label = 'right'
                left_ids = get_left_right_ids('left')
                right_ids = get_left_right_ids('right')
            elif 'RIGHT-TO-LEFT' in direction:
                left_label = 'right'
                right_label = 'left'
                left_ids = get_left_right_ids('right')
                right_ids = get_left_right_ids('left')
            else:
                continue

            process_log(f'left: {left_ids}')
            process_log(f'right: {right_ids}')

            if chem_id in left_ids:
                left_found = True
                
            if chem_id in right_ids:
                right_found = True
                
        if left_found:
            results.append((microbe, 'CONSUMES', chem))
            process_log('chemical appears on the left side, must be consumed')

        if right_found:
            results.append((microbe, 'PRODUCES', chem))
            process_log('chemical appears on the right side, must be produced')

        time.sleep(1)

with open('biocyc_small_test_results_2.json', 'w', encoding='utf-8') as f:
    json.dump(results, f)

with open('biocyc_small_test_logs_2.json', 'w') as f:
    json.dump(logs, f)