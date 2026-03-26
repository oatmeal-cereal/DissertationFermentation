with open('list_files\\manual triples.txt', 'r', encoding='utf-8') as f:
    trip_lines = f.readlines()
    
entity_map = {}

numbers_map = {
    0: 'zero',
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine'
}

all_relations = []

#with cypher, the query language used by 
all_commands = []

current_labels = ['MICROBE_NAME', 'COMPOUND', 'SUBSTRATE']
current_relations = ['CONSUMES', 'PRODUCES', 'BECOMES']

def preprocess_label(label):
    if label[0].isnumeric():
        label = label.replace(label[0], numbers_map[int(label[0])])
    replace_chars = ["-", "(", ")", " ", ".", ",", "\'", "/", "\"", ";", "&", ":", ";", "|", "%", "’", "?", "!", "«", "+", "（", "）", "？", "，"]
    for char in replace_chars:
        label = label.replace(char, '')
    return label

def preprocess_name(name):
    new_name = name
    if name[0] == '(':
        new_name = name[1:]
    if name[-1] == ')':
        new_name = new_name[:-1]
    new_name = new_name.strip()
    return new_name

no_sentences = 0

for ind, trips in enumerate(trip_lines):
    if trips == '\n':
        continue
    no_sentences += 1
    trip = [t.strip() for t in trips.split('|')]
    for t in trip:
        ent1, rel, ent2 = t.split('~')
        ent1type, ent1name = ent1.split(':')
        ent2type, ent2name = ent2.split(':')
        ent1name = preprocess_name(ent1name)
        ent1type = preprocess_name(ent1type)
        ent2type = preprocess_name(ent2type)
        ent2name = preprocess_name(ent2name)
        ent1label = preprocess_label(ent1name)
        ent2label = preprocess_label(ent2name)
        if not ent1label in entity_map.values():
            entity_map[ent1name] = ent1label
            if ent1type in current_labels:
                newstring1 = "MERGE (" + ent1label + ":" + ent1type + r"{" + "name:'" + ent1name + r"'})"
                all_commands.append(newstring1)
        if not ent2label in entity_map.values():
            entity_map[ent2name] = ent2label
            if ent2type in current_labels:
                newstring2 = "MERGE (" + ent2label + ":" + ent2type + r"{" + "name:'" + ent2name + r"'})"
                all_commands.append(newstring2)
            
        if not rel in current_relations:
            continue
        else:
            rel_string = ent1label + rel + ent2label
            if not rel_string in all_relations:
                all_commands.append(f"MERGE ({ent1label})-[:{rel}]->({ent2label})")
                all_relations.append(rel_string)
                
print('no. sentences:', no_sentences)

""" for command in all_commands:
    with open('tiny_example.cypher', 'a', encoding='utf-8') as f:
        f.write(command)
        f.write('\n') """