import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px
from deep_translator import GoogleTranslator
from requests.exceptions import ReadTimeout, RequestException
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
    translator = GoogleTranslator(source='id', target='en')

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
                if comment:  # Ensure the comment is not None or empty
                    try:
                        # Translate comment to English using deep-translator
                        translated_comment = translator.translate(comment)
                        
                        if translated_comment:  # Ensure the translation is not empty
                            # Analyze sentiment of the translated comment
                            score = sia.polarity_scores(translated_comment)
                            if score['compound'] >= 0.05:
                                sentiment_results['positive'] += 1
                            elif score['compound'] <= -0.05:
                                sentiment_results['negative'] += 1
                            else:
                                sentiment_results['ambivalent'] += 1
                        else:
                            print(f"Translation returned an empty result for comment: {comment}")
                    except ReadTimeout:
                        print("ReadTimeout occurred, skipping this comment.")
                    except RequestException as e:
                        print(f"RequestException occurred: {e}")
                        # Optionally, retry or continue after delay
                        time.sleep(5)
                    except Exception as e:
                        print(f"Unexpected error processing comment: {e}")

    # Convert results to DataFrame
    sentiment_df = pd.DataFrame(list(sentiment_results.items()), columns=['Sentiment', 'Count'])

    # Create a pie chart using Plotly
    fig = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Analysis')

    return fig
