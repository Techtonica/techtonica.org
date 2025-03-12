import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_db_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")

    try:
        engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{db}"
        )  # noqa: E501
        print("Database connection successful!")
        return engine
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None
