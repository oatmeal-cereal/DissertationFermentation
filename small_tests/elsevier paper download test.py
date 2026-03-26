import httpx

headers = {
    'X-ELS-APIKey': '37855ec81adc5bddb76fcfa8ee4f1b29',
    'Accept': 'application/pdf'
}

client = httpx.Client(headers=headers)
fulltext = client.get('https://api.elsevier.com/content/article/PII:B9780123744074005070')

print(fulltext.status_code)

f = open('elsevier_test_file.pdf', 'x')
with open('elsevier_test_file.pdf', 'wb') as f:
    f.write(fulltext.content)
    f.close()
f.close()