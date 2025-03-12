import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_db_connection():
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")

    if not all([user, password, host, db]):
        # Handle missing environment variables
        logging.warning("Missing database credentials.")
        return None

    try:
        engine = create_engine
        (f"mysql+mysqlconnector://{user}:{password}@{host}/{db}")
        # Test the connection
        with engine.connect():
            logging.info("Database connection successful!")
            return engine

    except Exception as e:
        logging.warning(f"Database connection failed: {e}")
        return None
