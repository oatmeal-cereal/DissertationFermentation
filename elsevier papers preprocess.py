import os
import json
import re

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
        #split = re.split('All rights reserved|Published by', text)
        words = text.split(' ')
        no_website_filenames = [word for word in words if not re.findall('https?://|.sml|.png', word)]
        words = ' '.join(no_website_filenames)
        no_publisher = re.split('All rights reserved|Publishing Limited|Published by|Elsevier B.V.|Elsevier Ltd|Elsevier Inc.', words)
        #print(no_publisher[max(0, len(no_publisher)-1)])
        print(len(no_publisher[-1]))
        print()
        new_json_filename = f"{os.getcwd()}\\fermentation_papers_preprocessed\\{filename}"
        #if not os.path.isfile(new_json_filename):
        with open(new_json_filename, 'w', encoding='utf-8') as f:
            #json.dumps(no_publisher[-1])
            f.write(no_publisher[-1])