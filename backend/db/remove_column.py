#!/usr/bin/env python3
"""
Script to remove the average_volume column from the food table in the database.
"""

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

# Import from our modules
from database import engine, SessionLocal

def remove_average_volume_column():
    """
    Remove the average_volume column from the food table.
    """
    session = SessionLocal()
    
    try:
        print("Removing average_volume column from food table...")
        
        # SQL query to remove the column
        # Note: SQLAlchemy doesn't have a direct method to drop columns,
        # so we use raw SQL with the text() function
        query = text("""
        ALTER TABLE food DROP COLUMN average_volume;
        """)
        
        # Execute the query
        session.execute(query)
        session.commit()
        
        print("Successfully removed average_volume column from food table.")
        
        # Verify the column structure
        verify_query = text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'food' 
        ORDER BY ordinal_position;
        """)
        
        result = session.execute(verify_query)
        columns = [row[0] for row in result]
        
        print("Current columns in food table:")
        for column in columns:
            print(f"- {column}")
        
    except SQLAlchemyError as e:
        print(f"Error removing column: {e}")
        session.rollback()
    finally:
        session.close()

def update_schema_class():
    """
    Print instructions for updating the SQLAlchemy model class.
    """
    print("\nIMPORTANT: You need to update your SQLAlchemy model class in schemas.py")
    print("Remove the average_volume line from the Food class:")
    print("\nFrom:")
    print("class Food(Base):")
    print("    __tablename__ = \"food\"")
    print("    id = Column(Integer, primary_key=True, index=True)")
    print("    food_product = Column(String, index=True)")
    print("    average_volume = Column(Float)  # Remove this line")
    print("    amount = Column(Float)")
    print("    # ... other columns")
    print("\nTo:")
    print("class Food(Base):")
    print("    __tablename__ = \"food\"")
    print("    id = Column(Integer, primary_key=True, index=True)")
    print("    food_product = Column(String, index=True)")
    print("    amount = Column(Float)")
    print("    # ... other columns")

if __name__ == "__main__":
    # Remove the average_volume column
    remove_average_volume_column()
    
    # Print instructions for updating the model class
    update_schema_class() 