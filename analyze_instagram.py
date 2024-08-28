import pandas as pd
import plotly.graph_objects as go

def analyze_instagram_data():
    # Path to the dataset
    csv_file_path = 'files/dataset_instagram-api-scraper_2024-08-27_11-40-35-904.csv'

    # Read the CSV file
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # Ensure the necessary columns are present
    if 'timestamp' not in df.columns or 'likesCount' not in df.columns or 'commentsCount' not in df.columns:
        raise ValueError("CSV file must contain 'timestamp', 'likesCount', and 'commentsCount' columns.")
    
    # Convert the 'timestamp' column to datetime
    df['date'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by date
    df = df.sort_values(by='date')
    
    # Limit the maximum value of likes and comments to 1000 (this step can be adjusted based on your needs)
    df['likesCount'] = df['likesCount'].apply(lambda x: min(x, 1000))
    df['commentsCount'] = df['commentsCount'].apply(lambda x: min(x, 1000))
    
    # ***Calculate cumulative sum of likes and comments***
    df['cumulative_likes'] = df['likesCount'].cumsum()
    df['cumulative_comments'] = df['commentsCount'].cumsum()
    
    # Plot cumulative likes and comments over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['cumulative_likes'], mode='lines+markers', name='Cumulative Likes'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['cumulative_comments'], mode='lines+markers', name='Cumulative Comments'))

    fig.update_layout(
        title="Cumulative Instagram Engagement Growth Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Counts",
        legend_title="Engagement",
        template="plotly_dark"
    )
    
    # Save the plot to a file if needed or return the figure to display in Streamlit
    return fig

# Example usage in Streamlit:
# fig = analyze_instagram_data()
# st.plotly_chart(fig, use_container_width=True)