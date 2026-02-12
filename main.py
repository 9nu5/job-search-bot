import os
from datetime import datetime
from dotenv import load_dotenv
from src.storage.minio_storage import MinioStorage

def main():
    load_dotenv()
    
    endpoint= f"localhost:{os.getenv('MINIO_PORT')}"
    access_key = os.getenv('MINIO_ROOT_USER')
    secret_key = os.getenv('MINIO_ROOT_PASSWORD')
    bucket_name = os.getenv('MINIO_BUCKET_NAME')
    
    today=datetime.now().strftime("%Y_%m_%d")
    
    json_path= "data/scout_green_jobs.json"
    parquet_path=f"data/{today}_green_jobs.parquet"
    file_path=parquet_path
    object_name =f"data/raw_data/{today}_jobs.parquet"
    
    minio=MinioStorage(endpoint,access_key,secret_key)
    
    minio.save_json_as_parquet(json_path,parquet_path)
    minio.upload_file(bucket_name,object_name,file_path)

    print("むこ!!!")

if __name__ == "__main__":
    main()