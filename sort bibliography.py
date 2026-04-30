import pandas as pd
import os
from pybtex.database import BibliographyData, Entry
import codecs
import latexcodec
import math

current_license = 'ccby'

csv_file = f'..\\dissertation DLC content\\{current_license}.csv'

df = pd.read_csv(csv_file)

print(df.columns)

preprocessed_filenames = []

def process_filename(file):
    replacing = [' ', '-', '/', '(', ')', '.']
    for rep in replacing:
        file = file.replace(rep, '')
    return file

for file in os.listdir('..\\dissertation DLC content\\fermentation_papers_preprocessed'):
    filename = os.fsdecode(file)
    file_split = filename.split('.')
    filename = ''.join(file_split[:-1]) #removing the file extension
    filename_processed = process_filename(filename)
    preprocessed_filenames.append(filename_processed)

for ind, row in df.iterrows():
    filename = row['DOI'].replace('/', '-')
    filename_processed = process_filename(filename)
    filepath1 = f'..\\dissertation DLC content\\fermentation_papers\\{filename}'
    filepath2 = f'..\\dissertation DLC content\\fermentation_papers_preprocessed\\{filename}'
    if os.path.exists(filepath1 + '.json') or os.path.exists(filepath1 + '.txt') or os.path.exists(filepath2 + '.json') or os.path.exists(filepath2 + '.txt') or filename_processed in preprocessed_filenames:
        volume = 0
        if row["Volume"] == 'None' or math.isnan(row['Volume']):
            volume = 0
        else:
            volume = int(row["Volume"])
        bib_data = BibliographyData({
            codecs.encode(row['DOI'], encoding='ulatex+utf8'): Entry('article', [
                ('author', codecs.encode(row["Authors"], encoding='ulatex+utf8')),
                ('year', codecs.encode(str(row["Publication year"]), encoding='ulatex+utf8')),
                ('title', codecs.encode(row["Title"], encoding='ulatex+utf8')),
                ('journal', codecs.encode(row["Journal"], encoding='ulatex+utf8')),
                ('volume', codecs.encode(str(volume), encoding='ulatex+utf8')),
                ('DOI', codecs.encode(row["DOI"], encoding='ulatex+utf8')),
            ]),
        })

        with open(f'..\\dissertation DLC content\\{current_license}-v2.bib', 'a', encoding='utf-8', errors='ignore') as f:
            bib_data.to_file(f)