import streamlit as st

st.title("Social Media Analytical Dashboard")
st.header("Welcome to our Social Media Analytical Dashboard")

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

# Create a CSS file (replace 'styles.css' with your actual filename)
def fetch_search_results(query):
    api_key = 'AIzaSyCudPyUPvD7W3c34NFdWwlVcxRXCCkGUm8'  # Replace with your API key
    cse_id = '652a51e9118084553'    # Replace with your CSE ID
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cse_id}"
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

# Function to display news articles fetched from the search results
def display_news_articles():
    results = fetch_search_results('Lisa Halaby')
    articles_html = ''.join(
        [
            f"<div style='margin-bottom: 5px;'>"
            f"<a href='{item['link']}' style='color: white; text-decoration: none;'><h3 style='font-size: 12px;'>{item['title']}</h3></a>"
            f"<p style='color: white; font-size: 10px;'>{item['snippet']}</p>"
            "</div>"
            for item in results[:3]
        ]
    ) or "<p>No results found.</p>"
    return articles_html

# Function to display the modular design
def display_modular_design():
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown(
            f"""
            <div style='background-color: #2196F3; padding: 10px; border-radius: 10px; color: white; height: 100%; overflow: auto;'>
                <h2 style='font-size: 16px;'>News Articles</h2>
                {display_news_articles()}
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        scraped_content = scrape_example_website()
        st.markdown(
            f"""
            <div style='background-color: #2196F3; padding: 10px; border-radius: 10px; color: white;'>
                <h2 style='font-size: 14px; text-align: center;'>Web Scraping Results</h2>
                <p style='font-size: 12px;'>{scraped_content}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div style='background-color: #2196F3; width: 512px; height: 200px; margin: 20px auto; border-radius: 10px; padding: 20px; box-sizing: border-box;'>
            <h2 style='color: white; text-align: center;'>Middle</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style='background-color: #2196F3; width: 512px; height: 200px; margin: 20px auto; border-radius: 10px; padding: 20px; box-sizing: border-box;'>
            <h2 style='color: white; text-align: center;'>Bottom</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# Main app logic
st.markdown("<h1 style='text-align: center; color: #2196F3;'></h1>", unsafe_allow_html=True)

# Display the modular design
display_modular_design()