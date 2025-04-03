import logging
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

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

    url_object = URL.create(
        "mysql+mysqlconnector",
        username=user,
        password=password,
        host=host,
        database=db,
    )

    try:

        engine = create_engine(url_object)

        # Test the connection
        engine.connect()
        logging.info(f"Database connection to {db} successful!")

    except Exception as e:
        logging.warning(f"Database connection failed: {e}")
        return None


def get_table_names(connection):
    try:
        result = connection.execute(text("SHOW TABLES"))
        tables = result.fetchall()
        return [table[0] for table in tables]
    except Exception as e:
        logging.error(f"Failed to fetch table names: {e}")
        return None
