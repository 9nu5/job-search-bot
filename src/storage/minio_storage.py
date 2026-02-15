import io
import json
import pandas as pd
from minio import Minio


class MinioStorage:
    def __init__(self, endpoint, access_key, secret_key):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

    def load_json_to_df(self, json_data):
        with open(json_data, 'r', encoding='utf-8') as f:
              json_data = json.load(f)
        return pd.DataFrame(json_data)
        
    def convert_df_to_parquet_buffer(self, df):
        buffer=io.BytesIO()
        df.to_parquet(buffer, engine='pyarrow')
        
        size = buffer.getbuffer().nbytes
        buffer.seek(0)
        
        return buffer, size
        
    def upload_buffer(self, buffer, size, object_name, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            print(f"{bucket_name} created.")
            
        self.client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=buffer,
        length=size,
        content_type='application/octet-stream'
    )
        print("upload successful")
		