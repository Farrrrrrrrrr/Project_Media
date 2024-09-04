import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from requests.exceptions import ReadTimeout, RequestException
import time

# Download the VADER lexicon
nltk.download('vader_lexicon')

def analyze_facebook_sentiments(csv_file_path, column_name):
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

    # Check if the column exists in the DataFrame
    if column_name in df.columns:
        # Analyze sentiment for each comment
        for comment in df[column_name].dropna():
            if comment:  # Ensure the comment is not None or empty
                try:
                    # Translate comment from English to Indonesian
                    translated = translator.translate(comment, src='en', dest='id')
                    translated_comment = translated.text if translated else ''
                    
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

        # Print the sentiment results
        print("Sentiment Analysis Results:")
        for sentiment, count in sentiment_results.items():
            print(f"{sentiment.capitalize()}: {count}")
    else:
        print(f"Column '{column_name}' not found in the dataset.")

# Example usage
csv_file_path = 'files/facebook_sent_lisa_halaby.csv'
column_name = 'text'  # Adjust based on your CSV column name
analyze_facebook_sentiments(csv_file_path, column_name)
