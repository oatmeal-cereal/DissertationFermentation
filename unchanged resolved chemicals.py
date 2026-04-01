import pubchempy as pcp
import time
import json

chemicals = ['glucose', 'fructose', 'lactose', 'malic acid', 'lactic acid', 'ethanol', 'sucrose', 'citrate', 'pyruvate', 'citric acid']

with open("list_files\\noresolve_chemicals_mapping.json", 'r', encoding='utf-8') as f:
    noresolve_chemicals_mapping = json.load(f)

""" for chem in chemicals:
    comps = pcp.get_compounds(chem, 'name')
    time.sleep(0.2)
    if comps:
        synonyms = [syn.lower() for syn in comps[0].synonyms]
        for syn in synonyms:
            noresolve_chemicals_mapping[syn] = chem
    noresolve_chemicals_mapping[chem] = chem """

noresolve_chemicals_mapping['l-lactic acid'] = 'lactic acid'
noresolve_chemicals_mapping['l-lactate'] = 'lactic acid'
noresolve_chemicals_mapping['(s)-lactate'] = 'lactic acid'
noresolve_chemicals_mapping['l-malic acid'] = 'malic acid'
noresolve_chemicals_mapping['l-malate'] = 'malic acid'

print(noresolve_chemicals_mapping)

with open("list_files\\noresolve_chemicals_mapping.json", 'w', encoding='utf-8') as f:
    json.dump(noresolve_chemicals_mapping, f)