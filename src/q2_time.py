from typing import List, Tuple
import pandas as pd
import unicodedata

def is_emoji(text: str):
    return [letter for letter in text if unicodedata.category(letter) in ['So', 'Sm']]

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Read Parquet file
    data = pd.read_parquet(file_path, columns=['content'])

    # Initialize a dictionary to store counts of emojis for each tweet
    emoji_counts = {}
    
    # Read every row in data
    for tweet in data['content']:
        # Validate if a letter in tweet is a emoji using is_emoji function
        emojis = is_emoji(tweet)
        # Add the data in dictionary
        for emoji in emojis:
            emoji_counts[emoji] = emoji_counts.get(emoji, 0) + 1

    # Sort data and select the top 10 emojis
    emoji_counts = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return emoji_counts