import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import time
from vecconfig import DATA, CONSUMER_DATASET
import indexerhfcustomer
def main():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # Check if GPU is available and use it
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
        print(model.device)
    batch_size = 100
    batch = []
    vectors = []
    initial_time = time.time()
    df = pd.read_csv(CONSUMER_DATASET)
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = row['compositevector']
        print(text)
        batch.append(text)
        if len(batch) >= batch_size:
            response = model.encode(batch, batch_size=batch_size, show_progress_bar=True)
            vectors.append(response.tolist())
            batch = []
    if len(batch) > 0:
            response = model.encode(batch, batch_size=batch_size, show_progress_bar=True)
            vectors.append(response.tolist())
            batch = []
    df["compositevector_vector"] = [item for sublist in vectors for item in sublist]
    print(df)
    finish_time = time.time()
    print('Embeddings created in {:f} seconds\n'.format(finish_time-initial_time))
    indexerhfcustomer.main(df)

if __name__ == "__main__":
    main()


