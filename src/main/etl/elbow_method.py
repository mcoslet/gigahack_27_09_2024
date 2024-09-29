import os

import pandas as pd
from wordllama import WordLlama

from src.main.utils.commons import PathUtils
import matplotlib.pyplot as plt

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

inertia_values = []
k_values = range(100, 151)  # Try k values from 1 to 100

for k in k_values:
    labels, inertia = wl.cluster(docs, k=k, max_iterations=100, tolerance=1e-4)
    inertia_values.append(inertia)

plt.figure(figsize=(8, 6))
plt.plot(k_values, inertia_values, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

# Counter({4: 720, 6: 269, 8: 205, 7: 176, 1: 125, 2: 124, 9: 121, 3: 121, 5: 88, 0: 67})
