import pandas as pd
import numpy as np
from opensearchpy import OpenSearch, NotFoundError
from opensearchpy.helpers import bulk
from tqdm import tqdm
import time
from vecconfig import INDEX_NAME
def main(df):
    #df = df.replace(np.nan, '', regex=True)
    initial_time = time.time()
    # Define OpenSearch connection parameters
    host = "localhost"
    port = 9200  # Default OpenSearch port
    client = OpenSearch(
        hosts=[{"host": host, "port": port}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        http_auth=("admin", "R06ust@09"),
    )

    # Check connection
    try:
        info = client.info()
        print("Connected to OpenSearch:", info)
    except Exception as e:
        print("Error connecting to OpenSearch:", e)
    bulk_data = []
    documents = []
    for i, row in tqdm(df.iterrows(), total=len(df)):
        compositevector_vector = [float(x) for x in row["compositevector_vector"]]
        bulk_data.append(
            {"_index": INDEX_NAME, "_id": row["applicationid"],
             "_source": {
                 "id": row["applicationid"],
                 "fname": row["fname"],
                 "lname": row["lname"],
                 "address": row["address"],
                 "compositevector": row["compositevector"],
                 "compositevector_vector": compositevector_vector
             }
            }
        )
    indexing = bulk(client, bulk_data, chunk_size=8000)
    finish_time = time.time()
    print("Success - %s" % (indexing[0]))
    print('Documents indexed in {:f} seconds\n'.format(finish_time-initial_time))
