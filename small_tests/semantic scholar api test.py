import requests
import json

# Define the API endpoint URL
url = "http://api.semanticscholar.org/graph/v1/paper/search"

# Define the query parameters
query_params = {
    "query": '"fermentation"',
    "fields": "title,url,publicationTypes,publicationDate,openAccessPdf",
    "year": "1990-"
}

# Directly define the API key (Reminder: Securely handle API keys in production environments)
api_key = "your api key goes here"  # Replace with the actual API key

# Define headers with API key
#headers = {"x-api-key": api_key}

# Send the API request
response = requests.get(url, params=query_params).json()
for paper in response["data"]:
    print(f"Title: {paper['title']}")
    print(f"Abstract: {paper.get('abstract', 'No abstract')[:50]}...")
    print("---")