import json

with open('C:\\Users\\jace\\documents\\assignments\\DissertationFermentation\\list_files\\strain_names.json', 'r') as f:
    strains = json.load(f)

name = 'BL21'

if name in strains:
    print("yes")
else:
    print("no")