import requests
from bs4 import BeautifulSoup
from config import GOOGLE_API_KEY, GOOGLE_CSE_ID

def fetch_search_results(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={GOOGLE_CSE_ID}"
    response = requests.get(search_url)
    results = response.json()
    return results.get('items', [])

def scrape_example_website():
    url = "https://example.com"  # Replace with the actual URL you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find and return the first paragraph text (or other content)
    paragraph = soup.find('p')  # This finds the first <p> tag
    return paragraph.text if paragraph else "No content found."