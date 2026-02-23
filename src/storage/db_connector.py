import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

class DBConnector:
    def __init__(self):
        load_dotenv()
        
        user = os.getenv('MYSQL_USER')
        password = os.getenv('MYSQL_PASSWORD')        
        database_name = os.getenv('MYSQL_DATABASE')
        port = os.getenv('MYSQL_PORT')
        host=os.getenv('MYSQL_HOST')

        # Format: mysql+pymysql://user:password@host:port/database_name
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}" 
        
        # 4. Create the SQLAlchemy engine (the central connection point)
        self.engine = create_engine(db_url)
        print("MySQL connector established successfully!")

    def get_engine(self):
        # Return the engine instance for database operations
        return self.engine