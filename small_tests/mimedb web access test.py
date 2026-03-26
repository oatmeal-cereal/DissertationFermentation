import requests

path = 'https://mimedb.org/unearth/q?searcher=metabolites&query='

response = requests.get(f'{path}lactic+acid')

print(response)