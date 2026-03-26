from pronto import Ontology
import spacy
import os

os.chdir('..\\')

path_to_scispacy_model = os.path.normpath('C:\\Users\\jace\\Documents\\assignments\\dissertation DLC content\\en_ner_bionlp13cg_md-0.5.4\\en_ner_bionlp13cg_md\\en_ner_bionlp13cg_md-0.5.4')

linker = Ontology('OntoBiotope_BioNLP-OST-2019.obo')

scispacy_model = spacy.load(path_to_scispacy_model)

sentence = 'Figure 1 Malolactic conversion: a direct decarboxylation of l(−)-malic acid to l(+)-lactic acid.'

sent_ents = scispacy_model(sentence)

print([ent.text for ent in sent_ents.ents])

sent_onto = [linker.get_term(ent.text) for ent in sent_ents.ents]

print(sent_onto)