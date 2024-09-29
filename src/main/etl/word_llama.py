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
