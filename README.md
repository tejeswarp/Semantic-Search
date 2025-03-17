Setting up OpenSearch in local


docker run -d --name opensearch-knn -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "knn.memory.circuit_breaker.enabled=true" -e "DISABLE_SECURITY_PLUGIN=true" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=#YourPassword" --memory=6g --memory-swap=8g opensearchproject/opensearch:latest

curl -u admin:#YourPassword -X GET "http://localhost:9200/_cat/plugins?v"

Setting up local Virtual environmebnt for Python from terminal
C:\Users\Documents\GitHub\Semantic-Search>python -m venv venv
C:\Users\Documents\GitHub\Semantic-Search>venv\Scripts\activate 

Run the dependencies
(venv) PS C:\Users\Documents\GitHub\Semantic-Search\src> pip install -r requirements.txt


Steps to create Index in local OpenSearch Cluster

EndPoint: http://localhost:9200/consumer_knn_index

Method: PUT

Request Body:

{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "fname": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "lname": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "address": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "compositevector": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      },
      "compositevector_vector": {
        "type": "knn_vector",
        "dimension": 384,
        "method": {
          "engine": "nmslib",
          "space_type": "cosinesimil",
          "name": "hnsw",
          "parameters": {
            "ef_construction": 512,
            "m": 16
          }
        }
      }
    }
  }
}

follow below steps for running indexing pipeling in local, which reads mock data from csv and indexes data with embeddings in local Opensearch cluster

(venv) PS C:\Users\Documents\GitHub\Semantic-Search\src>python main.py


Start UVICORN server in local for REST API's

(venv) PS C:\Users\Documents\GitHub\Semantic-Search\src>uvicorn app:app --host 0.0.0.0 --port 8000 --reload

Access Swagger through below URL

http://127.0.0.1:8000/docs

CURL for testing Semantic search

curl -X 'POST' \
  'http://127.0.0.1:8000/search_customer?query=durga' \
  -H 'accept: application/json' \
  -d ''

CURL for testinng Semactic search with POST JSON Object

curl -X 'POST' \
  'http://127.0.0.1:8000/all-MiniLM-L6-v2/eval' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "fname": "sandep",
  "address": "stevnage"
}'
