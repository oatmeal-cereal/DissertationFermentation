from pytaxize.gn import gni, gnr
from pytaxize import scicomm
from pytaxize import gbif
from pytaxize import vascan_search

#print(gnr.resolve(names='S. cerevisiae', source='NCBI'))
print(vascan_search(q=['S. cerevisiae']))
print(gbif.parse(name=['S. cerevisiae']))

#print(gnr.resolve(names='S. cerevisiae'))

