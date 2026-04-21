from adeft.disambiguate import load_disambiguator
from adeft.download.download import get_s3_models

text = 'A fungus called Saccharomyces cerevisiae, also known as S. cerevisiae or bakers yeast, is used in making sourdough bread'

print(get_s3_models())

model = load_disambiguator('S')

dd = model.disambiguate(text)

print(dd)

#print(br.recognize(text=text))