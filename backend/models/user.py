from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    food_logs = relationship("UserFoodLog", back_populates="user")
    food_recommendations = relationship("FoodRecommendation", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    age = Column(Integer)
    number = Column(String)  # Phone number
    weight = Column(Float)   # in kg
    height = Column(Float)   # in cm
    health_issues = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    blood_type = Column(String, nullable=True)
    smoking_status = Column(String, nullable=True)
    alcohol_consumption = Column(String, nullable=True)
    physical_activity_level = Column(String, nullable=True)
    dietary_preferences = Column(String, nullable=True)
    weight_goal = Column(String, nullable=True)  # gain, maintain, lose
    calorie_target = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")

class UserFoodLog(Base):
    __tablename__ = "user_food_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("food.id"))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    meal_type = Column(String)  # breakfast, lunch, dinner, snack
    amount = Column(Float)  # serving size
    
    # Relationships
    user = relationship("User", back_populates="food_logs")
    food = relationship("Food")

class FoodRecommendation(Base):
    __tablename__ = "food_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recommendation_text = Column(Text)
    food_ids = Column(String)  # Comma-separated list of food IDs
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    source = Column(String)  # e.g., "llm", "rule-based", "image-based"
    context = Column(Text, nullable=True)  # Context used for generating recommendation
    
    # Relationships
    user = relationship("User", back_populates="food_recommendations") 