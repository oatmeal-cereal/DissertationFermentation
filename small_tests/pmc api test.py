import requests
import time
import xmltodict
import json
from bs4 import BeautifulSoup as BS
import xml.etree.ElementTree as ET

base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

all_papers = []

cursormark = None

pagecount = 0

while pagecount < 1:
    params = {
        'query': "food fermentation AND (OPEN_ACCESS:y) AND (license:'CC0') AND (HAS_FULLTEXT:y) AND (pmcid:*)",
        'format': 'json',
        'pageSize': 1000,  # Max per request
        'resultType': 'core'
    }

    response = requests.get(f"{base_url}", params=params)
    if response.status_code == 200:
        data = response.json()
        cursormark = data.get('nextCursorMark')
        papers = data.get('resultList', {}).get('result', [])
        for paper in papers:
            all_papers.append(paper)
            
    time.sleep(1)
    pagecount += 1

print(f"Found {len(papers)} papers")

print(all_papers[0].keys())
print("\n")

for paper in all_papers:
    with open("papertitles.txt", 'a', encoding='utf-8') as f:
        f.write(paper.get('title'))
        f.write("\n")
        f.close()