import os
from datetime import datetime
from dotenv import load_dotenv
from src.storage.minio_storage import MinioStorage

os.makedirs("data", exist_ok=True)

def main():
    load_dotenv()
    
    endpoint= f"localhost:{os.getenv('MINIO_PORT')}"
    access_key = os.getenv('MINIO_ROOT_USER')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    bucket_name = os.getenv('MINIO_BUCKET_NAME')
    
    today=datetime.now().strftime("%Y_%m_%d")
    
    json_path= "data/scout_green_jobs.json"
    object_name =f"data/raw_data/{today}_jobs.parquet"
    
    minio=MinioStorage(endpoint,access_key,secret_key)
    
    df = minio.load_json_to_df(json_path)
    parquet_buffer, buffer_size = minio.convert_df_to_parquet_buffer(df)
    minio.upload_buffer(parquet_buffer, buffer_size, object_name, bucket_name)

    print("むこ!!!")

if __name__ == "__main__":
    main()