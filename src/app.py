import torch
from fastapi import FastAPI
from opensearchpy import OpenSearch
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import Optional
import env
from vecconfig import INDEX_NAME

app = FastAPI()


@app.get("/")
def index():
    return {"Make a post request to /search to search through customers"}


@app.get("/ready")
def get():
    msg = {"Message": "Read"}
    return msg


@app.post("/query_embeddings")
def search_hf(query: str):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # check if GPU is available and use it
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
        print(model.device)
    query_embeddings = model.encode(query, show_progress_bar=True)
    return {"response": query_embeddings.tolist(), }


@app.post("/search_customer")
def search_customer(query: str):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # check if GPU is available and use it
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
        print(model.device)
    query_embeddings = model.encode(query, show_progress_bar=True)
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
    # Define KNN query
    knn_query = {
        "size": 5,  # Number of nearest neighbors to retrieve
        "query": {
            "knn": {
                "compositevector_vector": {
                    "vector": query_embeddings.tolist(),
                    "k": 5,
                }
            }
        }
    }
    # Execute Search
    response = client.search(index=INDEX_NAME, body=knn_query)

    # Print search results
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Score: {hit['_score']}, Source: {hit['_source']}")
    # Filter results where score > 0.65
    filtered_results = [
        hit for hit in response["hits"]["hits"] if hit["_score"] > 0.65
    ]

    return {"results": filtered_results}

class SimpleEvalRequest(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    address: Optional[str] = None

def append_non_null_strings(*strings):
    return " ".join(s for s in strings if s)

@app.post("/all-MiniLM-L6-v2/eval")
def search_eval_customer(request: SimpleEvalRequest):
    print(request)
    result = append_non_null_strings(request.fname, request.lname, request.address)
    print(result)
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # check if GPU is available and use it
    if torch.cuda.is_available():
        model = model.to(torch.device("cuda"))
        print(model.device)
    query_embeddings = model.encode(result, show_progress_bar=True)
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
    # Define KNN query
    knn_query = {
        "size": 5,  # Number of nearest neighbors to retrieve
        "query": {
            "knn": {
                "compositevector_vector": {
                    "vector": query_embeddings.tolist(),
                    "k": 5,
                }
            }
        }
    }
    # Execute Search
    response = client.search(index=INDEX_NAME, body=knn_query)

    # Print search results
    for hit in response['hits']['hits']:
        print(f"ID: {hit['_id']}, Score: {hit['_score']}, Source: {hit['_source']}")
    # Filter results where score > 0.65
    filtered_results = [
        hit for hit in response["hits"]["hits"] if hit["_score"] > 0.65
    ]

    return {"results": filtered_results}