import streamlit as st
from web_crawler import news_search
from analyze_instagram import analyze_instagram_data
from instagram_sentiment import analyze_sentiments


st.set_page_config(layout="wide", page_title="Media Center")



st.markdown(
    """
    <style>
    /* Change the background color of the main content area */
    .stApp {
        background-color: #002349;
    }

    /* Optional: Change the color of the sidebar if you have one */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center; color: #fff;'>Media Center</h1>",
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #fff;'>", unsafe_allow_html=True)

# Function to display the modular design


  # Line separator
 
    #st.markdown()
    
col1, col2 = st.columns([1, 1], gap="small")
    
sentiment_fig = analyze_sentiments()

with col1:
    st.text("Sentiment Analysis")
    st.plotly_chart(sentiment_fig, use_container_width=True)

        
    # Insert the Plotly figure
    
        
with col2:
    st.text("Instagram Engagement")
    engagement_fig = analyze_instagram_data()
    st.plotly_chart(engagement_fig, use_container_width=True)
        
st.markdown(
"""
<div class="shadow-box" style='width: 512px; margin: 20px auto;'>
    <h2 style='color: white; text-align: center;'>Sentiment Analysis</h2>
""",
unsafe_allow_html=True
)

query = st.text_input('Enter your search query:')
num_results = st.slider('Number of results to display:', min_value=1, max_value=10, value=3)


if query:
    st.write(f'Searching for "{query}"...')
    news_links = news_search(query, num_results)
    
    if news_links:
        st.write('Found the following links:')
        for link in news_links:
            st.write(link)
    else:
        st.write('No results found.')


# Main app logic
st.markdown("<h1 style='text-align: center; color: #2196F3;'></h1>", unsafe_allow_html=True)
