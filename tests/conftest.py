import pytest
from app.infrastructure.db.session.mysql import get_connection

@pytest.fixture(scope="function")
def db_conn():
    conn = get_connection()  # ou DB_NAME=ebib_test
    yield conn
    conn.close()
