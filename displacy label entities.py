import json
import spacy

with open('list_files\\ner_triples.jsonl', 'r', encoding='utf-8') as f:
    lines = list(f)
    
for line in lines:
    sent, ents = json.loads(line)
    print(sent)