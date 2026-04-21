import requests

test_microbes = ['S. cerevisiae', 'Lactobacillus acidophilus', 'Lactobacillus brevis', 'Levilactobacillus brevis', 'Lacticaseibacillus casei', 'Lactobacillus casei', 'Lentilactobacillus hilgardii', 'Lactobacillus hilgardii']
#test_microbes = ['Levilactobacillus brevis', 'Lacticaseibacillus casei', 'Lactobacillus casei', 'Streptomyces fragilis', 'Lactobacillus hilgardii']

for mic in test_microbes:
    print(mic)
    data = requests.get(f"https://api.gbif.org/v1/species/search?q={mic.replace(' ', '+')}")
    name = data.json()['results']

    if name:
        print(name[0]['species'])
        print(name[0])
        
""" gnr = requests.get('https://verifier.globalnames.org/api/v1/verifications/Lactobacillus%20acidophilus')
gnr_data = gnr.json()

print(gnr_data) """