Setting up OpenSearch in local


docker run -d --name opensearch-knn -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "knn.memory.circuit_breaker.enabled=true" -e "DISABLE_SECURITY_PLUGIN=true" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<YourPassword>" --memory=6g --memory-swap=8g opensearchproject/opensearch:latest

curl -u admin:<YourPassword> -X GET "http://localhost:9200/_cat/plugins?v"

Setting up local Virtual environmebnt for Python from terminal
C:\Users\Documents\GitHub\Semantic-Search>python -m venv venv
C:\Users\Documents\GitHub\Semantic-Search>venv\Scripts\activate 

Run the dependencies
(venv) PS C:\Users\Documents\GitHub\Semantic-Search\src> pip install -r requirements.txt
