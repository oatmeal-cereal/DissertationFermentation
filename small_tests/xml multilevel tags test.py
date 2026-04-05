from xml.etree import ElementTree as ET

file = ET.parse('yeast_glycerol_reactions_test.xml')

reactions = file.findall('Reaction')

for reaction in reactions:
    enzrxns = reaction.find('enzymatic-reaction')
    if enzrxns == None:
        #print("none:", enzrxns)
        continue

    enzyme_names = []

    for enzrxn in enzrxns.findall('Enzymatic-Reaction'):
        enzyme_names.append(enzrxn.find('common-name').text)

    #print(enzyme_names)

    print(reaction.keys())

    direction = reaction.findtext('reaction-direction')
    if direction:
        print("yes")
        print(direction)
    else:
        print("no")

    left_ids = [left.find('Compound').get('frameid') for left in reaction.findall('left')]
    right_ids = [right.find('Compound').get('frameid') for right in reaction.findall('right')]

    """ if 'GLYCEROL' in left_ids:
        print('glycerol becomes:', right_ids)
        #would add relations indicating that glycerol becomes all these, unless its glycerol itself then i dont do that

    if 'GLYCEROL' in right_ids:
        print('glycerol becomes:', left_ids) """
        #would indicate that a chemical becomes glycerol via the enzyme indicated by the enzymatic reaction

    #also would have to consider left-to-right, right-to-left and reversible reactions to determine which chemicals turn into what