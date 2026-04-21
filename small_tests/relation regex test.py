import re

relation = "MERGE (imidazoleglycerolphosphatesynthase)-[:CATALYZES]->(ammonium)"

ents = re.findall("\\([A-Za-z0-9]+\\)", relation)

rel = re.findall("\\[:[A-Za-z0-9]+\\]", relation)

for ent in ents:
    print(ent[1:-1])

print(rel[0][2:-1])