# parquet_minio_utils.py

import json
import pandas as pd
from minio import Minio


class MinioStorage:
    json_data="../data/scout_green_jobs.json"
    
    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

    def save_json_as_parquet(self, json_data, parquet_path):
        with open(json_data, 'r', encoding='utf-8') as f:
              json_data = json.load(f)
        df=pd.DataFrame(json_data)
        df.to_parquet(parquet_path)

    def upload_file(self, bucket_name, object_name, file_path):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"{bucket_name} created.")
            
        self.client.fput_object(bucket_name, object_name, file_path)
        print("upload successful")
		