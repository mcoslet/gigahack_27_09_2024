# Load the default WordLlama model
import os

from wordllama import WordLlama

from src.main.utils.commons import PathUtils

wl = WordLlama.load()

data_folder = [PathUtils.DATA / file for file in os.listdir(PathUtils.OUTPUT)][:100]

docs = [data.read_text() for data in data_folder]
labels, inertia = wl.cluster(docs, k=5, max_iterations=100, tolerance=1e-4)

print(labels)
print(inertia)
