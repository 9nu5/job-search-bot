import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def create_table():
    conne = None
    try:
        conne = psycopg2.connect(  # dialing, return:connection object
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        cur = conne.cursor()
        print("DB Accessed")

        create_query = """
        CREATE TABLE IF NOT EXISTS job_postings(
            id SERIAL PRIMARY KEY,
            company_name TEXT,
            title TEXT,
            salary_range TEXT,
            link TEXT UNIQUE,    -- unique for duplicates
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cur.execute(create_query)
        conne.commit()  # save
        print("Table created")

    except Exception as e:
        print(f"Error : {e}")
    finally:
        # disconnecting dialing
        if conne:
            cur.close()
            conne.close()
            print("Disconnected")


if __name__ == "__main__":
    create_table()
