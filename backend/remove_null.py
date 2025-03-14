from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal

def delete_null_food_products():
    """
    Delete all records where food_product is null.
    """
    session = SessionLocal()
    
    try:
        print("Deleting records with null food_product...")
        
        # SQL query to delete records with null food_product
        query = text("""
        DELETE FROM food
        WHERE food_product IS NULL OR food_product = '';
        """)
        
        # Execute the query
        result = session.execute(query)
        session.commit()
        
        # Get the number of deleted rows
        deleted_count = result.rowcount
        print(f"Successfully deleted {deleted_count} records with null food_product.")
        
        # Count the number of remaining records
        count_query = text("SELECT COUNT(*) FROM food;")
        remaining_count = session.execute(count_query).scalar()
        print(f"Remaining food records: {remaining_count}")
        
    except SQLAlchemyError as e:
        print(f"Error deleting null records: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # First delete records with null food_product
    delete_null_food_products()
    