import requests
from bs4 import BeautifulSoup
from sites_to_search import news_sites

def news_search(query, num_results):
    news_links = []
    for site in news_sites:
        try:
            response = requests.get(site, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                if query.lower() in a_tag.text.lower():
                    news_links.append((a_tag.text, a_tag['href'], site))
                    if len(news_links) >= num_results:
                        return news_links
        except requests.exceptions.Timeout:
            print(f"Timeout accessing {site}. Skipping to the next site.")
            continue  # Skip to the next site if there's a timeout
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {site}: {e}")
            continue  # Skip to the next site if there's another type of error
    return news_links