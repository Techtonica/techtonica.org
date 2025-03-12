import logging
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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

        engine = create_engine(
            f"mysql+mysqlconnector://{user}:{password}@{host}/{db}"
        )  # noqa: E501

        # Test the connection
        with engine.connect() as connection:
            logging.info("Database connection successful!")

            # Fetch table names as a check
            tables = get_table_names(connection)
            if tables:
                logging.info(f"Tables in the database: {tables}")
            else:
                logging.warning("No tables found in the database.")

            return engine

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
