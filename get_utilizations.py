import json

with open('list_files\\annotations_all_sentences.json', 'r', encoding='utf-8') as f:
    annotations = json.load(f)['annotations']
    
utilizations = set()

def strip_word(word):
    word = word.strip()
    stripping_crit = '.,-'
    if word[-1] in stripping_crit:
        word = word[:-1]
    return word
    
for sent, entities in annotations:
    ents = entities['entities']
    for start, end, label in ents:
        if label == 'KIND_OF_UTILIZATION_TESTED':
            utilizations.add(strip_word(sent[start:end].lower()))
            
utilizations.update(['forms', 'processes', 'consumes', 'breaks down', 'hydrolyse', 'exhibit', 'carbon source', 'nitrogen source', 'co-metabolize', 'metabolize', '-producing'])
utilizations = utilizations - set(['alcoholic fermentation', 'co-metabolized', '', 'changing', 'change', 'changed'])

print(utilizations)
print(len(utilizations))

with open('list_files\\utilizations_list.json', 'w', encoding='utf-8') as f:
    json.dump(list(utilizations), f)