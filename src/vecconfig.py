from pathlib import Path
from dotenv import  load_dotenv
load_dotenv()
DATA = Path(__file__).parent.parent / "data"
CONSUMER_DATASET = DATA / "consumers_sample.csv"
INDEX_NAME = "customer_knn_index"