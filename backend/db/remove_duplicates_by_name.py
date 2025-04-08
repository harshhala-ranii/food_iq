#!/usr/bin/env python3
"""
Simple script to remove duplicate food records based on food_product name.
This script keeps only one record for each unique food name.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Import from our modules
from database import SessionLocal

def remove_duplicates_by_name():
    """
    Remove duplicate records from the Food table, keeping only one record
    for each unique food_product name.
    """
    session = SessionLocal()
    
    try:
        print("Starting duplicate removal by food name...")
        
        # SQL query to remove duplicates
        # This keeps the record with the lowest ID for each food_product
        query = text("""
        DELETE FROM food
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM food
            GROUP BY food_product
        );
        """)
        
        # Execute the query
        result = session.execute(query)
        session.commit()
        
        # Get the number of deleted rows
        deleted_count = result.rowcount
        print(f"Successfully removed {deleted_count} duplicate records.")
        
        # Count the number of remaining records
        count_query = text("SELECT COUNT(*) FROM food;")
        remaining_count = session.execute(count_query).scalar()
        print(f"Remaining unique food records: {remaining_count}")
        
    except SQLAlchemyError as e:
        print(f"Error removing duplicates: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    remove_duplicates_by_name() 