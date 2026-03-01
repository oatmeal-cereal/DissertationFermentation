import os
import json

os.chdir(os.getcwd())
for file in os.listdir("fermentation_papers"):
    filename = os.fsdecode(file)
    fullfilename = f"{os.getcwd()}\\fermentation_papers\\{filename}"
    if filename.endswith('json'):
        with open(fullfilename, 'r', encoding='utf-8') as f:
            content = json.load(f)
            text = content.get('originalText')
        with open(fullfilename, 'w', encoding='utf-8') as f:
            json.dump(text, f)
        print("done!")