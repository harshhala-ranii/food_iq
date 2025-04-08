#!/usr/bin/env python3
"""
Script to import data from Sheet.csv into the database.
"""

import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

# Import from our modules
from backend.schema.schemas import Base, Food
from database import engine, SessionLocal

def import_sheet_csv():
    """
    Import data from Sheet.csv into the database.
    """
    # Path to the CSV file
    csv_file = os.path.join(os.path.dirname(__file__), "Sheet.csv")
    
    if not os.path.exists(csv_file):
        print(f"Error: File not found at {csv_file}")
        return
    
    print(f"Importing data from {csv_file}...")
    
    # Read the CSV file
    try:
        df = pd.read_csv(csv_file)
        print(f"Successfully read CSV file with {len(df)} rows.")
        print(f"Columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return
    
    # Rename columns to match the database schema
    df.columns = ["food_product", "average_volume", "amount", "energy",
                  "carbohydrate", "protein", "total_fat", "sodium", "iron"]
    
    # Drop the average_volume column as it's no longer needed
    df = df.drop(columns=["average_volume"])
    
    # Replace NaN values with None (NULL in DB)
    df = df.where(pd.notnull(df), None)
    
    # Convert numeric columns to float
    numeric_columns = ["amount", "energy", "carbohydrate", 
                       "protein", "total_fat", "sodium", "iron"]
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to float
    
    # Create a database session
    session = SessionLocal()
    
    try:
        # Check if there are existing records
        existing_count = session.query(Food).count()
        print(f"Found {existing_count} existing records in the database.")
        
        # Insert new records
        inserted_count = 0
        for _, row in df.iterrows():
            # Skip empty rows
            if pd.isna(row["food_product"]) or row["food_product"] == "":
                continue
                
            # Check if the food product already exists
            existing_food = session.query(Food).filter(Food.food_product == row["food_product"]).first()
            
            if existing_food:
                print(f"Food product '{row['food_product']}' already exists, skipping.")
                continue
            
            food = Food(
                food_product=row["food_product"],
                amount=row["amount"],
                energy=row["energy"],
                carbohydrate=row["carbohydrate"],
                protein=row["protein"],
                total_fat=row["total_fat"],
                sodium=row["sodium"],
                iron=row["iron"]
            )
            session.add(food)
            inserted_count += 1
        
        session.commit()
        print(f"Successfully inserted {inserted_count} new records into the database.")
        
        # Verify the total count after insertion
        final_count = session.query(Food).count()
        print(f"Total records in the database: {final_count}")
        
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Import data from Sheet.csv
    import_sheet_csv() 