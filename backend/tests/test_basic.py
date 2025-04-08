import pytest
from backend.schema.schemas import Food
from database import engine, SessionLocal
from sqlalchemy.orm import Session

def test_database_connection():
    # Test that we can connect to the database
    session = SessionLocal()
    try:
        # Try to execute a simple query
        session.execute('SELECT 1')
        assert True
    finally:
        session.close() 