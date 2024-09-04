import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def analyze_facebook_data(selected_metric='likesCount'):
    # Path to the dataset
    file_path = 'files/facebook_lisa_halaby.csv'

    # Read the CSV file
    df = pd.read_csv(file_path, encoding='utf-8')

    # Filter the dataset to only include rows where user/name contains 'Hj. Erna Lisa Halaby'
    df_filtered = df[df['user/name'].str.contains('Hj. Erna Lisa Halaby', na=False)]

    # Ensure the necessary columns are present
    required_columns = ['date', 'likesCount', 'commentsCount', 'sharesCount', 'viewsCount']
    if not all(col in df_filtered.columns for col in required_columns):
        raise ValueError("CSV file must contain 'date', 'likesCount', 'commentsCount', 'sharesCount', and 'viewsCount' columns.")
    
    # Convert 'date' column to datetime
    df_filtered['date'] = pd.to_datetime(df_filtered['date'])
    
    # Sort the data by date
    df_filtered = df_filtered.sort_values(by='date')
    
    # Compute cumulative sums for each metric
    for metric in ['likesCount', 'commentsCount', 'sharesCount', 'viewsCount']:
        df_filtered[f'cumulative_{metric}'] = df_filtered[metric].cumsum()
    
    # Calculate cumulative total insights
    df_filtered['total_insights'] = (
        df_filtered['cumulative_likesCount'] +
        df_filtered['cumulative_commentsCount'] +
        df_filtered['cumulative_sharesCount'] +
        df_filtered['cumulative_viewsCount']
    )

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for each metric
    metrics = {
        'cumulative_likesCount': {'name': 'Total Likes', 'color': 'blue'},
        'cumulative_commentsCount': {'name': 'Total Comments', 'color': 'green'},
        'cumulative_sharesCount': {'name': 'Total Shares', 'color': 'purple'},
        'cumulative_viewsCount': {'name': 'Total Views', 'color': 'orange'},
        'total_insights': {'name': 'Total Insights', 'color': 'red'}
    }
    
    for metric, info in metrics.items():
        fig.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered[metric],
            mode='lines+markers',  # Ensure lines are connected
            name=info['name'],
            line=dict(color=info['color'])
        ))

    # Update layout with range slider and dropdown for y-axis selection
    fig.update_layout(
        title={
            'text': "Cumulative Facebook Engagement Growth Over Time",
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis_title='Date',
        yaxis_title='Cumulative Counts',
        xaxis=dict(
            tickformat='%b %d, %Y',
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(label='All', step='all')
                ])
            ),
            rangeslider=dict(visible=True)
        ),
        yaxis=dict(
            title='Cumulative Counts',
            rangemode='tozero'  # This ensures that the y-axis starts at zero
        ),
        template='plotly_dark'
    )

    # Set default view to the selected metric
    fig.update_traces(visible='legendonly')  # Hide all traces by default
    if f'cumulative_{selected_metric}' in metrics:
        fig.update_traces(selector=dict(name=metrics[f'cumulative_{selected_metric}']['name']), visible=True)

    # Save the plot to a file or return the figure to display in your application
    fig.write_html('facebook_engagement.html')
    return fig