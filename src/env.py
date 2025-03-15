import os
from dotenv import load_dotenv
load_dotenv(verbose=True)
elastic_server_host = os.environ.get('ELASTIC_SERVER_HOST')
opensearch_rest_username=os.environ.get('ELASTIC_USER_NAME')
opensearch_rest_password=os.environ.get('ELASTIC_USER_PASS')