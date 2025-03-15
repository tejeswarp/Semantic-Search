import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Example sentences
sentences = [
    "Machine learning is fascinating.",
    "I love working with Python.",
    "Artificial intelligence is the future."
]

# Generate embeddings
embeddings = model.encode(sentences)

# Print the embeddings (each sentence converts to a 384-dimensional vector)
for i, sentence in enumerate(sentences):
    print(f"Sentence: {sentence}")
    print(f"Embedding: {embeddings[i][:5]}...")  # Showing first 5 values for brevity
    print()
