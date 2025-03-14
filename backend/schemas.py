from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define Food table schema
class Food(Base):
    __tablename__ = "food"
    id = Column(Integer, primary_key=True, index=True)
    food_product = Column(String, index=True)  # Name of food
    amount = Column(Float)  # Amount (float)
    energy = Column(Float)  # Energy (float)
    carbohydrate = Column(Float)  # Carbohydrate (float)
    protein = Column(Float)  # Protein (float)
    total_fat = Column(Float)  # Total Fat (float)
    sodium = Column(Float)  # Sodium (float)
    iron = Column(Float)  # Iron (float) 