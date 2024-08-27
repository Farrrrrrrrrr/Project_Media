import pandas as pd
import matplotlib.pyplot as plt

def analyze_instagram_data():
    # Use the specified file path
    csv_file_path = 'files/dataset_instagram-api-scraper_2024-08-27_11-40-35-904.csv'
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Ensure the necessary columns are present
    if 'timestamp' not in df.columns or 'likesCount' not in df.columns or 'commentsCount' not in df.columns:
        raise ValueError("CSV file must contain 'timestamp', 'likesCount', and 'commentsCount' columns.")
    
    # Convert the 'timestamp' column to datetime
    df['date'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by date
    df = df.sort_values(by='date')
    
    # Calculate the cumulative sum for likes and comments
    df['cumulative_likes'] = df['likesCount'].cumsum()
    df['cumulative_comments'] = df['commentsCount'].cumsum()
    
    # Plot the cumulative likes and comments
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['cumulative_likes'], marker='o', color='blue', linestyle='-', label='Cumulative Likes')
    plt.plot(df['date'], df['cumulative_comments'], marker='o', color='green', linestyle='-', label='Cumulative Comments')
    plt.title('Cumulative Instagram Engagement Growth Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Counts')
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.tight_layout()
    
    # Save the plot to a file
    graph_path = 'engagement_growth.png'
    plt.savefig(graph_path, bbox_inches='tight')
    
    return graph_path

# Example usage:
# graph_file = analyze_instagram_data()
# print(f"Graph saved to {graph_file}")
