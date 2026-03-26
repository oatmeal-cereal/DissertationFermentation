#is a multistrain aerobic fermentation that progressively gets more confusing as it continues

from pypdf import PdfReader as pr
import spacy
from spacy import displacy
#from scispacy.abbreviation import AbbreviationDetector
import os

model = spacy.load('en_ner_bc5cdr_md')

i = 0
os.chdir('fermentation_papers')
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