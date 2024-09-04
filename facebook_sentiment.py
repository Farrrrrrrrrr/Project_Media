import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import plotly.express as px
from googletrans import Translator, LANGUAGES
from requests.exceptions import ReadTimeout, RequestException
import time

# Download the VADER lexicon
nltk.download('vader_lexicon')

def analyze_facebook_sentiments():
    # Path to the dataset
    csv_file_path = 'files/facebook_sent_lisa_halaby.csv'

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

    # Check if the 'text' column exists in the DataFrame
    if 'text' in df.columns:
        # Analyze sentiment for each comment
        for comment in df['text'].dropna():
            try:
                # Translate comment to English
                translated_comment = translator.translate(comment, src='id', dest='en')
                
                # Check if translation is successful and the text is not None
                if translated_comment and translated_comment.text:
                    # Analyze sentiment of the translated comment
                    score = sia.polarity_scores(translated_comment.text)
                    if score['compound'] >= 0.05:
                        sentiment_results['positive'] += 1
                    elif score['compound'] <= -0.05:
                        sentiment_results['negative'] += 1
                    else:
                        sentiment_results['ambivalent'] += 1
                else:
                    print(f"Translation failed or returned empty text for comment: {comment}")

            except ReadTimeout:
                print("ReadTimeout occurred, skipping this comment.")
            except RequestException as e:
                print(f"RequestException occurred: {e}")
                # Optionally, retry or continue after delay
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected error processing comment: {e}")

        # Convert results to DataFrame
        sentiment_df = pd.DataFrame(list(sentiment_results.items()), columns=['Sentiment', 'Count'])

        # Create a pie chart using Plotly
        fig = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Analysis')

        # Save the plot to a file or return the figure to display in your application
        fig.write_html('sentiment_analysis.html')  # Save the plot
        return fig
    else:
        print("Column 'text' not found in the dataset.")
        return None