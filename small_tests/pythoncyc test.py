import pythoncyc
from pythoncyc.PToolsFrame import PFrame
from pythoncyc.PTools import sendQueryToPTools

pgdb = pythoncyc.select_organism('meta')

""" glucose = pgdb['GLUCOSE']

print(glucose)

print(pgdb.get_name_string(glucose, include_species_strain_name=True)) """

random_pathway = 'PWY-6005'
random_enzymatic_reaction = 'ENZRXN0-8627'

list_of_reactions = ['ENZRXN0-8627', 'ENZRXN-20698', 'ENZRXN-13625']

random_compounds = ['MALTOSE', 'CPD0-2040']

frameid = pgdb

""" response = sendQueryToPTools("(loop for x in (all-substrates) collect (get-name-string x))")

print(response) """

""" pathways = pgdb.all_pathways('small-molecule')

print([path for path in pathways])

for path in pathways:
    #print(pgdb.get_slot_value(path, 'common-name'))
    components = pgdb.pathway_components(path)
    if components:
        first_part = components[0][0]
        #print([pgdb.get_slot_value(comp, 'common-name') for comp in first_part])
        print([comp for comp in first_part]) """