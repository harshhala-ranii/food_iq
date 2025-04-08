#!/usr/bin/env python3
"""
Script to delete food records with specific IDs (from 111 to 132).
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Import from our modules
from database import SessionLocal

def delete_specific_ids():
    """
    Delete records from the Food table with IDs from 111 to 132.
    """
    session = SessionLocal()
    
    try:
        print("Starting deletion of records with IDs from 111 to 132...")
        
        # SQL query to delete records with IDs in the specified range
        query = text("""
        DELETE FROM food
        WHERE id BETWEEN 111 AND 132;
        """)
        
        # Execute the query
        result = session.execute(query)
        session.commit()
        
        # Get the number of deleted rows
        deleted_count = result.rowcount
        print(f"Successfully deleted {deleted_count} records with IDs between 111 and 132.")
        
        # Count the number of remaining records
        count_query = text("SELECT COUNT(*) FROM food;")
        remaining_count = session.execute(count_query).scalar()
        print(f"Remaining food records: {remaining_count}")
        
    except SQLAlchemyError as e:
        print(f"Error deleting records: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    delete_specific_ids() 