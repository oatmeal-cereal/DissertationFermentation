if saved_relations.get(f"{microbe}-CONSUMES-{chem}") or new_relations.get(('MICROBE', microbe, 'CONSUMES', 'CHEMICAL', chem)) or saved_relations.get(f"{microbe}-PRODUCES-{chem}") or new_relations.get(('MICROBE', microbe, 'PRODUCES', 'CHEMICAL', chem)):
    continue

dbs = biocyc_db_mappings.get(microbe)

if not dbs:
    continue

if len(dbs) == 1:
    db_values = dbs.values()
    database = list(db_values)[0]
else:
    db_values = dbs.values()
    database = random.choice(list(db_values))
chem = process_comp(chem)

#if nothing comes up in compounds search assume its an enzyme which was misidentified as a chemical
chem_resp = session.get(f'https://websvc.biocyc.org/{database}/name-search?object={chem}&class=Compounds&fmt=json')

try:
    chem_resp = chem_resp.json()
except:
    print("json error:")
    print(chem_resp.text)
    continue

if not chem_resp.get('RESULTS'):
    #nothing to see here!
    continue

time.sleep(1)

chem_resp = chem_resp.get('RESULTS')[0]

comp_id = chem_resp.get('OBJECT-ID')
#TODO: get TYPE of id, whether it is really a compound, or actually an enzyme, because those get identified by scispacy

utilisation = session.get(f'https://websvc.biocyc.org/getxml?{database}:{comp_id}&fmt=json')

try:
    util_xml = ET.fromstring(utilisation.text).find('Compound')
except: #accept defeat and move on
    continue

time.sleep(1)

lefts = util_xml.find('appears-in-left-side-of')

if not lefts == None:
    #add a relation that the microbe consumes the chemical as a substrate
    new_relations[('MICROBE', microbe, 'CONSUMES', 'CHEMICAL', chem)] = True

    for reaction in lefts:
        reaction_id = reaction.get('frameid')

        enzymes_resp = session.get(f"https://websvc.biocyc.org/apixml?fn=enzymes-of-reaction&id={database}:{reaction_id}")

        time.sleep(1)

        try:
            enzymes_xml = ET.fromstring(enzymes_resp.text)
        except:
            print("enzyme failure:")
            print(enzymes_resp.text)
            continue

        proteins = enzymes_xml.findall('Protein')

        for protein in proteins:
            enzreactions = protein.find('catalyzes')
            for reaction in enzreactions:
                enzyme_id = reaction.find('enzyme').find('Protein').get('frameid')

                enzyme_id_processed = preprocess_label(enzyme_id)

                if entity_label_map.get(enzyme_id_processed):
                    continue

                name_resp = session.get(f'https://websvc.biocyc.org/getxml?{database}:{enzyme_id}')

                name_xml = ET.fromstring(name_resp.text).find('Protein').find('common-name').text

                entity_label_map[enzyme_id_processed] = preprocess_name(name_xml)

                new_relations[('MICROBE', microbe, 'SYNTHASIZES', 'ENZYME', name_xml)] = True
                new_relations[('ENZYME', name_xml, 'CATALYZES', 'CHEMICAL', chem)] = True

                time.sleep(1)

        #print(enzymes_xml.findall('enzyme'))
        
else:
    new_relations[('MICROBE', microbe, 'CONSUMES', 'CHEMICAL', chem)] = False

rights = util_xml.find('appears-in-right-side-of')

if not rights == None:
    #add a relation that the microbe produces this metabolite
    new_relations[('MICROBE', microbe, 'PRODUCES', 'CHEMICAL', chem)] = True
else:
    new_relations[('MICROBE', microbe, 'PRODUCES', 'CHEMICAL', chem)] = False

""" for right in rights:
    print(right.get('frameid')) """