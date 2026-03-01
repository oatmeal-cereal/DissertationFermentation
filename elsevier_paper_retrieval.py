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
client = ElsClient(config['apikey'])
client.inst_token = config['insttoken']

## ScienceDirect (full-text) document example using DOI
doi_doc = FullDoc(doi = '10.1016/S1525-1578(10)60571-5')
if doi_doc.read(client):
    print ("doi_doc.title: ", doi_doc.title)
    doi_doc.write()
else:
    print ("Read document failed.")


## Initialize doc search object using ScienceDirect and execute search, 
#   retrieving all results
doc_srch = ElsSearch("food fermentation",'sciencedirect')
doc_srch.execute(client, get_all = False)
print ("doc_srch has", len(doc_srch.results), "results.")