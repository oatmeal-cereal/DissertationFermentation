import os
import json
import re
from pypdf import PdfReader as pr
from pathlib import Path

os.chdir('..\\dissertation DLC content')

for ind, file in enumerate(os.listdir(os.getcwd() + "\\fermentation_papers")):
    print("Paper", ind)
    filename = os.fsdecode(file)
    if filename.endswith('.json'):
        json_filename = f"{os.getcwd()}\\fermentation_papers\\{filename}"
        try:
            with open(json_filename, 'r', encoding='utf-8') as f:
                text = json.load(f)
        except:
            with open(json_filename, 'rb') as f:
                text = f.read().decode('latin-1')
        new_filepath = f"{os.getcwd()}\\fermentation_papers_preprocessed\\{filename}"
    else:
        continue
    """     elif filename.endswith('.pdf'):
        print('pdf!')
        path = Path(os.getcwd() + "\\fermentation_papers\\" + filename)
        reader = pr(path)
        text = ""
        for page in reader.pages:
            text = text + page.extract_text()
        new_filename = ' '.join(filename.split('.')[:-1]) + '.json'
        new_filepath = f"{os.getcwd()}\\fermentation_papers_preprocessed\\{new_filename}"
    else:
        continue """

    #split = re.split('All rights reserved|Published by', text)
    words = text.split(' ')
    no_website_filenames = [word for word in words if not re.findall('https?://|.sml|.png', word)]
    words = ' '.join(no_website_filenames)
    no_publisher = re.split('All rights reserved|Publishing Limited|Published by|Elsevier B.V.|Elsevier Ltd|Elsevier Inc.', words)
    no_newline = [word for word in no_publisher if word != '\n']
    #print(no_publisher[max(0, len(no_publisher)-1)])
    print(no_newline[-1][:200])
    print()
    
    #if not os.path.isfile(new_json_filename):
    try:
        with open(new_filepath, 'w', encoding='utf-16') as f:
            #json.dumps(no_publisher[-1])
            f.write(no_newline[-1])
    except:
        print("encoding error bruh")