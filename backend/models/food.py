from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Food(Base):
    __tablename__ = "food"
    
    id = Column(Integer, primary_key=True, index=True)
    food_product = Column(String, index=True)  # Name of food
    amount = Column(Float)  # Standard amount (e.g., 100g)
    amount_unit = Column(String, default="g")  # Unit for amount (g, ml, etc.)
    
    # Nutrition per standard amount
    energy = Column(Float)  # Energy in kcal
    carbohydrate = Column(Float)  # Carbohydrate in g
    sugar = Column(Float, nullable=True)  # Sugar in g
    fiber = Column(Float, nullable=True)  # Dietary fiber in g
    protein = Column(Float)  # Protein in g
    total_fat = Column(Float)  # Total fat in g
    saturated_fat = Column(Float, nullable=True)  # Saturated fat in g
    unsaturated_fat = Column(Float, nullable=True)  # Unsaturated fat in g
    
    # Minerals and vitamins
    sodium = Column(Float, nullable=True)  # Sodium in mg
    potassium = Column(Float, nullable=True)  # Potassium in mg
    calcium = Column(Float, nullable=True)  # Calcium in mg
    iron = Column(Float, nullable=True)  # Iron in mg
    vitamin_a = Column(Float, nullable=True)  # Vitamin A in μg
    vitamin_c = Column(Float, nullable=True)  # Vitamin C in mg
    vitamin_d = Column(Float, nullable=True)  # Vitamin D in μg
    
    # Additional food properties
    food_group = Column(String, nullable=True)  # e.g., "Fruits", "Vegetables", "Proteins"
    glycemic_index = Column(Float, nullable=True)  # Glycemic index value
    processing_level = Column(String, nullable=True)  # e.g., "Raw", "Minimally Processed", "Highly Processed"
    allergens = Column(Text, nullable=True)  # Comma-separated list of allergens
    
    # Image information
    image_url = Column(String, nullable=True)  # URL to food image
    
    # Metadata
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def to_dict(self):
        """Convert food object to dictionary for API responses"""
        return {
            "id": self.id,
            "food_product": self.food_product,
            "amount": self.amount,
            "amount_unit": self.amount_unit,
            "energy": self.energy,
            "carbohydrate": self.carbohydrate,
            "protein": self.protein,
            "total_fat": self.total_fat,
            "sodium": self.sodium,
            "iron": self.iron,
            "food_group": self.food_group,
            # Add additional fields as needed
        }

# Removed the duplicate UserFoodLog and FoodRecommendation classes as they're already defined in models/user.py 