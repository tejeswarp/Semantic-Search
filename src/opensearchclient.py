from opensearchpy import OpenSearch

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
