import requests
from bs4 import BeautifulSoup
from sites_to_search import news_sites
from datetime import datetime

def extract_date(soup):
    # Example logic to extract date. Adjust based on the actual HTML structure.
    date_tag = soup.find('time') or soup.find('span', class_='date')  # Example selectors
    if date_tag:
        try:
            # Example of parsing date. Adjust based on format and content.
            return datetime.strptime(date_tag.text.strip(), '%d %B %Y').strftime('%Y-%m-%d')
        except ValueError:
            return 'Unknown Date'
    return 'Unknown Date'

def news_search(query, num_results):
    news_links = []
    for site in news_sites:
        try:
            response = requests.get(site, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            for a_tag in soup.find_all('a', href=True):
                if query.lower() in a_tag.text.lower():
                    # Extract the page content to parse date
                    article_page = requests.get(a_tag['href'])
                    article_soup = BeautifulSoup(article_page.content, 'html.parser')
                    date = extract_date(article_soup)
                    news_links.append((a_tag.text, a_tag['href'], site, date))
                    if len(news_links) >= num_results:
                        # Sort by date, assuming 'Unknown Date' is the least recent
                        news_links.sort(key=lambda x: (x[3] == 'Unknown Date', x[3]), reverse=True)
                        return news_links
        except requests.exceptions.Timeout:
            print(f"Timeout accessing {site}. Skipping to the next site.")
            continue  # Skip to the next site if there's a timeout
        except requests.exceptions.RequestException as e:
            print(f"Error accessing {site}: {e}")
            continue  # Skip to the next site if there's another type of error
    
    # Sort results by date, assuming 'Unknown Date' is the least recent
    news_links.sort(key=lambda x: (x[3] == 'Unknown Date', x[3]), reverse=True)
    return news_links