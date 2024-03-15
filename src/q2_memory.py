from typing import List, Tuple
import pandas as pd
import unicodedata

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Read Parquet file
    data = pd.read_parquet(file_path, columns=['content'])

    # Initialize a dictionary to store counts of emojis for each tweet
    emoji_counts = {}
    
    # Read every row in data
    for tweet in data['content']:
        # Validate if a letter in tweet is a emoji using unicodedata format
        emojis = [letter for letter in tweet if unicodedata.category(letter) in ['So', 'Sm']]
        # Add the data in dictionary
        for emoji in emojis:
            emoji_counts[emoji] = emoji_counts.get(emoji, 0) + 1

    # Sort data and select the top 10 emojis
    emoji_counts = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return emoji_counts