import spacy
import json

#bionlp_model_name = '..\\dissertation DLC content\\en_ner_bionlp13cg_md-0.5.4\\en_ner_bionlp13cg_md\\en_ner_bionlp13cg_md-0.5.4'

model = spacy.load('en_core_sci_sm')

with open('list_files\\genus_names.json', 'r', encoding='utf-8') as f:
    genera = json.load(f)
    
with open('list_files\\species_names.json', 'r', encoding='utf-8') as f:
    species = json.load(f)

regular_vocab = list(model.vocab.strings)

""" no = 92_500
print(regular_vocab[no:no+100]) """

current_gib_num = 92_500

regular_vocab = set(regular_vocab[current_gib_num:]) - set(genera) - set(species) - set([gen.lower() for gen in genera])

with open('list_files\\custom_model_vocab.json', 'w', encoding='utf-8') as f:
    json.dump(list(regular_vocab), f)