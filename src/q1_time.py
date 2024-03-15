from typing import List, Tuple
from datetime import datetime
import pandas as pd

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Read the data file
    df = pd.read_parquet(file_path, columns=['date', 'user_username'])
    
    # Convert the 'date' column to date format
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    # Find the user with the most posts for each date
    most_posts_per_date = df.groupby('date')['user_username'].agg(lambda x: x.value_counts().idxmax())
    
    # Get the top 10 most common dates
    top_10_dates = df['date'].value_counts().nlargest(10).index
    
    # Create a list to store the results
    results = [(date, most_posts_per_date[date]) for date in top_10_dates]
    
    return results
