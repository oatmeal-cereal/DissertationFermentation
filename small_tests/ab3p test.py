import pyab3p

text = 'Saccharomyces fragilis (S. fragilis), produces galactosidase'
text2 = 'In this study, Lactobacillus fermentum (LF) inoculum was used as stater culture for small scale cocoa fermentation'
text3 = 'The bacteria produced LA'
text4 = 'The microbe Saccharomyces cerevisiae, also known as S. cerevisiae which is a yeast fungi'

abbrev = pyab3p.Ab3p()

print(abbrev.get_abbrs(text4))