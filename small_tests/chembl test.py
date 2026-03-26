from chembl_webresource_client.new_client import new_client

test_compounds = ['lactic acid', 'propanoic acid', 'propionic acid', 'ethanol', 'bioethanol', 'riboflavin', 'vitamin B2', 'glucose', 'fructose', 'xylose']

molecule = new_client.molecule

organism = new_client

for compound in test_compounds:
    comp = molecule.search(compound)
    print(comp)
    wiki_name = [c['xref_id'] for c in comp['cross_references'] if c["xref_src"]=='Wikipedia']
    wiki_name = '' if not wiki_name else wiki_name[0]
    print(wiki_name)
    if comp:
        pref_name = comp[0]['pref_name']
        if pref_name:
            print(pref_name)
    """ for c in comp:
        pref_name = c['pref_name']
        if pref_name:
            print(pref_name) """