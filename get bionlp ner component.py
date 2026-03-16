import spacy

model_name = '..\\dissertation DLC content\\en_ner_bionlp13cg_md-0.5.4\\en_ner_bionlp13cg_md\\en_ner_bionlp13cg_md-0.5.4'

model = spacy.load(model_name)

ner_component = model.get_pipe('ner')