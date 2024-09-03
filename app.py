import streamlit as st
from web_crawler import fetch_search_results, scrape_example_website
from analyze_instagram import analyze_instagram_data
from analyze_sentiment import analyze_sentiments

st.set_page_config(layout="wide", page_title="Media Center")
scraped_content = scrape_example_website()


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
    "<h1 style='text-align: center; color: #fff;'>Social Media Analytical Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h2 style='text-align: center; color: #fff;'>Media Portal for Lisa Halaby</h2>",
    unsafe_allow_html=True
)
st.markdown("<hr style='border: 1px solid #fff;'>", unsafe_allow_html=True)

def display_news_articles():
    results = fetch_search_results('Lisa Halaby')
    articles_html = ''.join(
        [
            f"<div style='margin-bottom: 1px;'>"
            f"<a href='{item['link']}' style='color: white; text-decoration: none;'><h3 style='font-size: 24px;'>{item['title']}</h3></a>"
            f"<p style='color: white; font-size: 16px;'>{item['snippet']}</p>"
            "</div>"
            for item in results[:3]
        ]
    ) or "<p>No results found.</p>"
    return articles_html

# Function to display the modular design
def display_modular_design():
    # CSS for levitating effect with shadow
    st.markdown(
        """
        <style>
        .shadow-box {
            background-color: #2196F3;  
            padding: 10px;
            border-radius: 10px;
            color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2), 0 6px 20px rgba(0, 0, 0, 0.19); /* Shadow effect */
            margin: 20px 0; /* Add some space between columns */
            height: 100%;
            overflow: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
    st.markdown(hide_default_format, unsafe_allow_html=True)

  # Line separator
 
    #st.markdown()
    
    col1, col2 = st.columns([1, 1], gap="small")
    
    with col1:
        st.markdown(
            f"""
            <style>
            .news {{
                margin: 5px;
                background-color: #5F90B2;
                color: black;
                font-family: Arial, sans-serif;
                padding: 15px; 
            }}
            .news h2 {{
                margin: 5px;
                font-size: 18px;
                text-align: center;
            }}
            </style>
            <div class="news">
                <h2>News Articles</h2>
                {display_news_articles()}
            </div>
            """,
            unsafe_allow_html=True
        )

        
    with col2:
        st.markdown(
            """
            <style>
            .content {
                background-color: #5F90B2;
                color: black;
                font-family: Arial, sans-serif;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 20px;
                padding: 15px; 
            }
            .content h2 {
                font-size: 18px;  /* Matching the font size */
                text-align: center;
            }
            .content p {
                font-size: 12px;  /* Adjusting the font size for content */
                text-align: left;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="content">
                <h2>Web Scraping Results</h2>
                <p>{scraped_content}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


   
    st.markdown(
        """
        <div class="shadow-box" style='width: 512px; margin: 20px auto;'>
            <h2 style='color: white; text-align: center;'>Instagram Engagement Growth</h2>
        """,
        unsafe_allow_html=True
    )
    
    # Call the analyze_instagram_data function and display the graph
    engagement_fig = analyze_instagram_data()
    st.plotly_chart(engagement_fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    

    st.markdown(
    """
    <div class="shadow-box" style='width: 512px; margin: 20px auto;'>
        <h2 style='color: white; text-align: center;'>Sentiment Analysis</h2>
    """,
    unsafe_allow_html=True
    )

    sentiment_fig = analyze_sentiments()
    st.plotly_chart(sentiment_fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main app logic
st.markdown("<h1 style='text-align: center; color: #2196F3;'></h1>", unsafe_allow_html=True)

# Display the modular design
display_modular_design()