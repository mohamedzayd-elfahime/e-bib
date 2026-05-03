import mysql.connector
from app.config import settings


def get_connection():
    """
    Create and return a new MySQL connection.
    One connection per request / query.
    """
    return mysql.connector.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME,
        autocommit=True,
    )
