import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy import displacy

import json
from pypdf import PdfReader as pr
import os

model = spacy.load('en_core_web_sm')
ruler = model.add_pipe('entity_ruler')

with open('..\\species_names.json') as f:
    species_names = json.load(f)
    
ruler.add_patterns(species_names)
    
i = 0
os.chdir('..\\fermentation_papers')
for file in os.listdir(os.getcwd()):
    if i < 4:
        filename = os.fsdecode(file)
        reader = pr(filename)
        text = ""
        for page in reader.pages:
            text = text + page.extract_text()
        doc = model(text)
        entities = doc.ents
        displacy_image = displacy.render(doc)
        print(entities)
    i += 1