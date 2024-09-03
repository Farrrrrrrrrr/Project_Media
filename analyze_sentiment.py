import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px
from googletrans import Translator
from requests.exceptions import ReadTimeout
import time

# Download the VADER lexicon
nltk.download('vader_lexicon')

def analyze_sentiments():
    # Path to the dataset
    csv_file_path = 'files/lisa_halaby.csv'

    # Read the CSV file
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()

    # Initialize the translator
    translator = Translator()

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
                try:
                    # Translate comment to English
                    translated_comment = translator.translate(comment, src='id', dest='en').text
                    # Analyze sentiment of the translated comment
                    score = sia.polarity_scores(translated_comment)
                    if score['compound'] >= 0.05:
                        sentiment_results['positive'] += 1
                    elif score['compound'] <= -0.05:
                        sentiment_results['negative'] += 1
                    else:
                        sentiment_results['ambivalent'] += 1
                except ReadTimeout:
                    print("ReadTimeout occurred, skipping this comment.")
                except Exception as e:
                    print(f"Error processing comment: {e}")
                    # Optionally, log the error or handle it

    # Convert results to DataFrame
    sentiment_df = pd.DataFrame(list(sentiment_results.items()), columns=['Sentiment', 'Count'])

    # Create a pie chart using Plotly
    fig = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Analysis')

    return fig
