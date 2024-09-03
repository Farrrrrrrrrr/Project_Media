import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def analyze_instagram_data():
    # Path to the dataset
    file_path = 'files/lisa_halaby.csv'

    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Ensure the necessary columns are present
    if 'timestamp' not in df.columns or 'likesCount' not in df.columns or 'commentsCount' not in df.columns:
        raise ValueError("CSV file must contain 'timestamp', 'likesCount', and 'commentsCount' columns.")
    
    # Convert the 'timestamp' column to datetime
    df['date'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by date
    df = df.sort_values(by='date')
    
    # Limit the maximum value of likes and comments to 1000000 (this step can be adjusted based on your needs)
    df['likesCount'] = df['likesCount'].apply(lambda x: min(x, 1000000))
    df['commentsCount'] = df['commentsCount'].apply(lambda x: min(x, 1000000))
    
    # Calculate cumulative sum of likes and comments
    df['cumulative_likes'] = df['likesCount'].cumsum()
    df['cumulative_comments'] = df['commentsCount'].cumsum()
    df['total_insights'] = df['cumulative_likes'] + df['cumulative_comments']
    
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Plot cumulative likes, comments, and total insights over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['cumulative_likes'], mode='lines+markers', name='Cumulative Likes'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['cumulative_comments'], mode='lines+markers', name='Cumulative Comments'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['total_insights'], mode='lines+markers', name='Total Insights'))
    
    # Update layout with current date below the title
    fig.update_layout(
        title={
            'text': "Cumulative Instagram Engagement Growth Over Time",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        annotations=[
            {
                'x': 0.5,
                'y': -0.15,
                'xref': 'paper',
                'yref': 'paper',
                'text': f'Current Date: {current_date}',
                'showarrow': False,
                'font': {'size': 12, 'color': 'black'},
                'align': 'center'
            }
        ],
        xaxis_title="Date",
        yaxis_title="Cumulative Counts",
        legend_title="Engagement",
        template="plotly_dark"
    )
    
    # Save the plot to a file if needed or return the figure to display in Streamlit
    return fig
