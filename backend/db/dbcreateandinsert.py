import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from our modules
from models.database import engine, SessionLocal
from models.food import Food

# Function to load CSV data into the database
def load_csv_to_db(csv_file: str):
    df = pd.read_csv(csv_file)

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

    session = SessionLocal()
    
    try:
        for _, row in df.iterrows():
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
        
        session.commit()
        print(f"Inserted {len(df)} records from {csv_file} into the database.")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting data: {e}")

    finally:
        session.close()

# Example usage
if __name__ == "__main__":
    # Get the absolute path to the CSV file
    csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Sheet.csv")
    load_csv_to_db(csv_file)
