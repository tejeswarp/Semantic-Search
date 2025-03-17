import pandas as pd
import numpy as np
from opensearchpy import OpenSearch, NotFoundError
from opensearchpy.helpers import bulk
from tqdm import tqdm
import time
from vecconfig import INDEX_NAME
import env
def main(df):
    #df = df.replace(np.nan, '', regex=True)
    initial_time = time.time()
    # Define OpenSearch connection parameters
    client = OpenSearch(
        hosts=[{"host": env.elastic_server_host, "port": env.elastic_server_port}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False,
        http_auth=(env.opensearch_rest_username, env.opensearch_rest_password),
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
                 "countryofbirth": row["countryofbirth"],
                 "emailaddress": row["emailaddress"],
                 "gender": row["gender"],
                 "compositevector": row["compositevector"],
                 "compositevector_vector": compositevector_vector
             }
            }
        )
    indexing = bulk(client, bulk_data, chunk_size=8000)
    finish_time = time.time()
    print("Success - %s" % (indexing[0]))
    print('Documents indexed in {:f} seconds\n'.format(finish_time-initial_time))
