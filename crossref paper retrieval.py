import requests
import os
import time
import random
from pybtex.database import BibliographyData, Entry
import httpx
import codecs
import latexcodec
#import xml.etree.ElementTree as ET

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json
    
## Load configuration
con_file = open("config.json")
config = json.load(con_file)
con_file.close()

## Initialize client
els_client = ElsClient(config['apikey'])

base_url = "https://api.crossref.org/works"
base_url_filtered = "https://api.crossref.org/works/?filter=assertion:free"

unpaywall_url = "https://api.unpaywall.org/v2/"

els_api_key = '37855ec81adc5bddb76fcfa8ee4f1b29'

#cwd = os.getcwd()
os.chdir("..\\dissertation DLC content\\fermentation_papers")

content_types_and_ext = {
    'text/xml': 'xml',
    'text/plain': 'txt',
    'application/json': 'json',
    'application/pdf': 'pdf',
    'text/html': 'html'
}

headers = {'User-Agent': 'University of Bath student. I am gathering research papers on fermentation for a dissertation project in NLP. If you do not want your paper used for text or data mining purposes, please kindly email me at lp2095@bath.ac.uk with the paper title and DOI, and I will remove the paper from the corpus. I am using CrossRef to check for an approved tdm license for each paper before downloading the pdf, but unapproved papers might slip through the cracks.',
}

elsevier_headers = headers.copy()
elsevier_headers.update({'X-ELS-APIKey': els_api_key})

params = {
    'query': 'food fermentation',
    'select': 'title,DOI,assertion,link,update-to,license,author,container-title,volume,published',
    'sample': 100,
    'filter': 'has-full-text:true'
}

total_results = 0
all_papers = []

whitelisted_tdm_licenses = {"creativecommons.org/licenses/by": 'ccby',
                            "creativecommons.org/licenses/by-sa": 'ccbysa',
                            "creativecommons.org/licenses/by-nc": 'ccbync',
                            "creativecommons.org/licenses/by-nc-sa": 'ccbyncsa',
                            "http://www.springer.com/tdm": 'springer',
                            "creativecommons.org/publicdomain/zero": 'cczero',
                            "www.elsevier.com/tdm": 'elsevier',
                            "https://www.scientific.net/license/TDM_Licenser.pdf": 'transtechpub'}

#sometimes i get an error saying that i made too many requests to one website at one time, so i skip these to not get in trouble. otherwise they would be whitelisted
#licenses_skipping = ["springer", "elsevier", "mdpi"]
licenses_skipping = ["mdpi"]

#publisher-wide tdm approval, dont need to check for specific licenses from crossref or any other source, since all of them will be cc-by, cc0, etc.
whitelisted_tdm_publishers = ["Intech", "SAGE", "BMJ", "OECD", "PeerJ"]

#these publishers approve of tdm activity subject to the licenses of the individual papers, so tdm approval is not necessarily publisher-wide
#specifically i am concerned about cc-by-nc-nd which doesnt allow derivatives, it is currently unclear whether my project would constitute a derivative
publishers_subject_to_tdm_license = ["Frontiers Media SA", "Wiley", "Cambridge University Press", "BMC", "Humana Press", "Research Square Platform LLC", "Elsevier"]

#these publishers either dont approve tdm for my purpose, or im skipping them until more info is gathered, or are predatory publishers (eww pedos)
blacklisted_tdm_publishers = ["Brill", "Taylor and Francis", "Oxford University Press", "JSTOR", "CRC Press", 
                              "MDPI",
                              "OMICS Publishing Group",
                              "Springer"] #different api for this one

#check if the paper license has any of the above keywords which indicate text mining abilities or open access
def check_license_whitelist_for_tdm(license):
    for wl in whitelisted_tdm_licenses.keys():
        if wl in license:
            return True
    return False

def check_license_blacklist_for_tdm(license):
    for bl in licenses_skipping:
        if bl in license:
            return True
    return False

def check_publisher_tdm_whitelist(publisher):
    for pub in whitelisted_tdm_publishers:
        if pub in publisher:
            return True
    return False

def check_publisher_tdm_blacklist(publisher):
    for pub in blacklisted_tdm_publishers:
        if pub in publisher:
            return True
    return False

def check_tdm_license(licenses):
    tdm_found_and_whitelist = False
    tdm_license = ""
    for l in licenses:
        #first check if the license is blacklisted
        if check_license_blacklist_for_tdm(l.get('URL')):
            return False, None
        
        #if we can tell from the license alone that it is approved for tdm use, just return true with the link to the license
        if check_license_whitelist_for_tdm(l.get('URL')):
            return True, l.get('URL')

        #otherwise if we can't immediately tell, check the specific use of that license for tdm approval
        if l.get('content-version') == 'tdm':
            tdm_found_and_whitelist = True
            tdm_license = l.get('URL')
    return tdm_found_and_whitelist, tdm_license

fulltextheaders = headers.copy()
fulltextheaders.update({'Accept': ','.join(list(content_types_and_ext.keys()))})

def download_full_text(url, paperdoi, contenttype):
    filename = paperdoi.replace('/', '-')
    filetype = content_types_and_ext.get(contenttype, 'pdf')
    filepath = f"{filename}.{filetype}"
    success = False
    if not os.path.exists(filepath):
        if not 'elsevier' in url:
            fulltext = requests.get(url, headers=fulltextheaders)
            if fulltext.status_code == 200:
                print("creating file")
                f = open(filepath, 'x')
                with open(filepath, 'wb') as f:
                    f.write(fulltext.content)
                    f.close()
                f.close()
                success = True
        else: #vier
            #fulltext = client.get(f"https://api.elsevier.com/content/article/doi/{paperdoi}&view=FULL")
            doi_doc = FullDoc(doi=paperdoi)
            if doi_doc.read(els_client):
                doc_data = doi_doc.data
                doc_text = doc_data.get('originalText', '')
                if 'FULL-TEXT' in doc_text:
                    print('full text baybeeee')
                    doi_doc.write(os.getcwd(), filename)
                    success = True
    return success

response = requests.get(base_url, params=params, headers=headers)
if response.status_code == 200:
    data = response.json().get('message')
    total_results = data.get('total-results')
    print(total_results)
    papers = data.get('items')
    for paper in papers:
        time.sleep(1)
        print("Next paper")
        paperdoi = paper.get('DOI')
        paper_link = None

        #also want to skip papers like 'letter to the editor' or 'retraction note'
        
        wl_tdm_publisher = False
        tdm_license = None
        wl_tdm_license = False
        best_oa_url = None
        
        license = paper.get('license')

        unpaywall_response = requests.get(f"{unpaywall_url}/{paperdoi}?email=jacecereal@gmail.com")
        if unpaywall_response.status_code == 200:
            unpaywall_data = unpaywall_response.json()
            if not unpaywall_data:
                continue
            publisher = unpaywall_data.get('publisher')
            #if none of the publishers papers are available for tdm, or for my specific purpose, skip
            if check_publisher_tdm_blacklist(publisher):
                continue
            #if they are, set this as true
            if check_publisher_tdm_whitelist(publisher):
                wl_tdm_publisher = True
            else:
                if not license:
                    try:
                        license = unpaywall_data.get('best_oa_location', {'': ''}).get('license', None)
                    except:
                        pass
                        
                    try:
                        license = unpaywall_data.get('first_oa_location', {'': ''}).get('license', None)
                    except:
                        continue
                    if license not in whitelisted_tdm_licenses.values():
                        continue
                else:
                    wl_tdm_license, tdm_license = check_tdm_license(license)
                    if not wl_tdm_license:
                        continue
            if unpaywall_data.get('best_oa_location'):
                best_oa_url = unpaywall_data.get('best_oa_location').get('url')
            print(publisher)
        
        #if the publisher is not whitelisted nor there is a specific tdm license for the paper, skip it
        if not (wl_tdm_publisher or wl_tdm_license):
            continue
        
        if not (tdm_license or license):
            continue
        
        paper_url = None
        contenttype = None
        
        if paper.get('link'):
            paper_link = paper.get('link', [])
            for pl in paper_link:
                contenttype = pl.get('content-type')
                print(contenttype)
                paper_url = pl.get('URL')
                if pl.get('intended-application') == 'text-mining' or pl.get('content-type') == 'tdm':
                    paper_url = pl.get('URL') #if a link to the paper exists for which the intended application is text mining, use it, we want the optimal link
                    break
            paper_url = paper_link[0].get('URL') #otherwise, since at this point the paper was already approved for tm purposes just get the first link
                    
        if not (paper_url or best_oa_url):
            continue
        
        if not paper_url:
            paper_url = best_oa_url
                    
        paper_title = paper.get('title', '')
        print("Title:", paper_title)
        print(paper_url)
        
        download_success = download_full_text(paper_url, paperdoi, contenttype)
        
        if not download_success:
            continue
        
        bib_data = BibliographyData({
            '': Entry('article', [
                ('author', codecs.encode(f"{paper.get('author', [{}])[0].get('family')} {paper.get('author', [{}])[0].get('given')}", encoding='ulatex+utf8')),
                ('year', codecs.encode(f"{paper.get('published', {}).get('date-parts', [['']])[0][0]}", encoding='ulatex+utf8')),
                ('title', paper_title[0]),
                ('journal', paper.get('container-title', [''])[0]),
                ('volume', codecs.encode(f"{paper.get('volume')}", encoding='ulatex+utf8')),
                ('DOI', codecs.encode(f"{paperdoi}", encoding='ulatex+utf8')),
            ]),
        })

        bibli_success = False
        if download_success:
            #in the bibliography of papers included in the text mining activity, i want to group papers by license, because i am required to provide a link to the license
            for license_link, license_type in whitelisted_tdm_licenses.items():
                if license_link in tdm_license:
                    with codecs.open(f'{str(license_type)}.bib', 'a', encoding='utf-8', errors='ignore') as f:
                        bib_data.to_file(f)
                    bibli_success = True
                    break
            if not bibli_success:
                with codecs.open('tdm_papers.bib', 'a', encoding='utf-8', errors='ignore') as f:
                    bib_data.to_file(f)

        print('\n')
        
        randrange2 = random.uniform(5.026, 7.25)
        randtime = random.uniform(5.89, randrange2)
        time.sleep(randtime)