from vecconfig import CONSUMER_DATASET
from csv import DictReader
import pandas as pd
from tqdm import tqdm
with open(CONSUMER_DATASET, 'r') as new_obj:
    csv_dict_reader = DictReader(new_obj)
    for row in csv_dict_reader:
        print(row)
df = pd.read_csv(CONSUMER_DATASET)
for _, row in tqdm(df.iterrows(), total=len(df)):
    print(row)
