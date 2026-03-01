import spacy
import json

model = spacy.load('..\\dissertation DLC content\\en_ner_bionlp13cg_md-0.5.4\\en_ner_bionlp13cg_md\\en_ner_bionlp13cg_md-0.5.4')

print(type(model.vocab.strings))

model.vocab.to_disk('scispacy_vocab')