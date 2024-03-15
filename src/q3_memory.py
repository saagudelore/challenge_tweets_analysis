from collections import defaultdict
import pandas as pd
from typing import List, Tuple

def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Initialize a dictionary to store counts of mentioned users for each tweet
    mentioned_user_counts = {}

    # Read every row in data
    for row in pd.read_parquet(file_path, columns=['mentionedUsers_username'])['mentionedUsers_username']:
        # Validate if mentioned users is not null
        if row is not None:
            mentioned_user_counts[row] = mentioned_user_counts.get(row, 0) + 1

    # Sort data and select the top 10 mentioned users
    mentioned_user_counts = sorted(mentioned_user_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return mentioned_user_counts
