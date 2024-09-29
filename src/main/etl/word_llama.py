# Load the default WordLlama model
import os

import pandas as pd
from wordllama import WordLlama

from src.main.utils.commons import PathUtils

wl = WordLlama.load()

data_folder = [PathUtils.RESOURCES / "topics_with_time" / file for file in
               os.listdir(PathUtils.RESOURCES / "topics_with_time")]
docs = []
for file in data_folder:
    data = pd.read_json(file, orient='index')
    data['topic'] = data['topic_data'].apply(lambda x: x['topic'] if 'topic' in x else None)
    topics = data['topic'].dropna().unique()
    topics_str = [str(topic) for topic in topics]
    docs.extend(topics_str)
print(docs)
print(len(docs))
k = 130
labels, inertia = wl.cluster(docs, k=k, max_iterations=100, tolerance=1e-4)
print(labels)
print(inertia)


# Create a dictionary to store topics for each cluster
cluster_topics = {i: [] for i in range(k)}

# Assign each topic to its corresponding cluster
for topic, label in zip(docs, labels):
    cluster_topics[label].append(topic)

# Print topics for each cluster
for cluster, topics in cluster_topics.items():
    print(f"Cluster {cluster}:")
    for topic in topics:
        print(f"  - {topic}")
    print()  # Add a blank line between clusters for readability

print("Inertia:", inertia)

# Counter({48: 111, 19: 80, 74: 76, 60: 71, 20: 55, 66: 53, 0: 52, 8: 49, 50: 45, 23: 43, 16: 42, 21: 41, 39: 41, 26: 40, 65: 40, 73: 34, 25: 34, 9: 34, 43: 33, 27: 32, 78: 31, 14: 31, 53: 30, 2: 29, 13: 29, 7: 28, 5: 27, 11: 27, 17: 27, 57: 25, 35: 24, 71: 23, 15: 23, 30: 22, 56: 22, 10: 22, 44: 21, 63: 21, 24: 21, 79: 21, 34: 20, 3: 20, 59: 20, 52: 20, 1: 19, 12: 18, 69: 18, 76: 16, 62: 16, 29: 16, 31: 16, 55: 15, 54: 15, 42: 14, 32: 14, 77: 13, 58: 13, 41: 13, 47: 12, 37: 12, 22: 12, 49: 12, 38: 12, 28: 11, 18: 11, 75: 11, 40: 11, 33: 10, 68: 10, 36: 10, 61: 10, 51: 9, 67: 9, 64: 9, 46: 8, 6: 8, 45: 7, 70: 7, 4: 5, 72: 4})

