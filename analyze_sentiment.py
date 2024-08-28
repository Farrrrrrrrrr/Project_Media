import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px

# Download the VADER lexicon
nltk.download('vader_lexicon')

def analyze_sentiments():
    # Path to the dataset
    csv_file_path = 'files/dataset_instagram-api-scraper_2024-08-27_11-40-35-904.csv'

    # Read the CSV file
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()

    # List to store sentiment results
    sentiment_results = {
        'positive': 0,
        'negative': 0,
        'ambivalent': 0
    }

    # Analyze sentiment for each comment
    for i in range(10):
        comment_column = f'latestComments/{i}/text'
        if comment_column in df.columns:
            for comment in df[comment_column].dropna():
                score = sia.polarity_scores(comment)
                if score['compound'] >= 0.05:
                    sentiment_results['positive'] += 1
                elif score['compound'] <= -0.05:
                    sentiment_results['negative'] += 1
                else:
                    sentiment_results['ambivalent'] += 1

    # Convert results to DataFrame
    sentiment_df = pd.DataFrame(list(sentiment_results.items()), columns=['Sentiment', 'Count'])

    # Create a pie chart using Plotly
    fig = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Analysis')

    return fig
