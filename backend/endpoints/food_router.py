from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import numpy as np
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import logging

# Import from our modules
from models.food import Food
from models.database import get_db
from models.food_queries import get_food_nutrition, display_food_details

# Create router
router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Function to safely convert float values
def safe_float(value):
    """Convert NaN or Infinity to None (JSON-compliant)."""
    if value is None or isinstance(value, str):  
        return value  # Return as is if it's a string
    if np.isnan(value) or np.isinf(value):  
        return None
    return value

# Function to safely get attribute value
def get_safe_attr(obj, attr_name):
    """Fetch attribute value safely, return None if missing or invalid."""
    value = getattr(obj, attr_name, None)  # Get attribute safely
    return round(value, 2) if isinstance(value, (int, float)) else None  # Ensure it's JSON-safe

# Function to generate a user-friendly summary
def generate_food_summary(food):
    """Generate a summary of the food item's nutritional value."""
    summary = f"Your meal, {food['Food Product']}, consists of "
    
    nutrient_info = []
    if food["Energy (kcal)"]:
        nutrient_info.append(f"{food['Energy (kcal)']} kcal of energy")
    if food["Carbohydrate (g)"]:
        nutrient_info.append(f"{food['Carbohydrate (g)']}g of carbohydrates")
    if food["Protein (g)"]:
        nutrient_info.append(f"{food['Protein (g)']}g of protein")
    if food["Total Fat (g)"]:
        nutrient_info.append(f"{food['Total Fat (g)']}g of total fat")
    if food["Sodium (mg)"]:
        nutrient_info.append(f"{food['Sodium (mg)']}mg of sodium")
    if food["Iron (mg)"]:
        nutrient_info.append(f"{food['Iron (mg)']}mg of iron")

    if nutrient_info:
        summary += ", ".join(nutrient_info) + "."
    else:
        summary += "minimal nutritional data available."

    return summary

# API Endpoint to Fetch Food Summary by Name
@router.get("/summary/{food_name}")
def get_food_summary(food_name: str, db: Session = Depends(get_db)):
    logger.debug(f"Received request for food: {food_name}")
    logger.debug(f"Food name type: {type(food_name)}")
    logger.debug(f"Food name value: '{food_name}'")
    
    # Use get_food_nutrition from food_queries.py
    food_item = get_food_nutrition(food_name, db)
    
    if not food_item:
        logger.debug(f"No food found for: {food_name}")
        raise HTTPException(status_code=404, detail="Food item not found")

    logger.debug(f"Found food item: {food_item.food_product}")
    
    # Format data safely
    food_data = {
        "Food Product": food_name,
        "Energy (kcal)": get_safe_attr(food_item, "energy"),
        "Carbohydrate (g)": get_safe_attr(food_item, "carbohydrate"),
        "Protein (g)": get_safe_attr(food_item, "protein"),
        "Total Fat (g)": get_safe_attr(food_item, "total_fat"),
        "Sodium (mg)": get_safe_attr(food_item, "sodium"),
        "Iron (mg)": get_safe_attr(food_item, "iron")
    }

    # Create nutrition object for the response
    nutrition = {
        "food_product": food_item.food_product,
        "amount": get_safe_attr(food_item, "amount"),
        "energy": get_safe_attr(food_item, "energy"),
        "carbohydrate": get_safe_attr(food_item, "carbohydrate"),
        "protein": get_safe_attr(food_item, "protein"),
        "total_fat": get_safe_attr(food_item, "total_fat"),
        "sodium": get_safe_attr(food_item, "sodium"),
        "iron": get_safe_attr(food_item, "iron")
    }

    # Return the response with summary and nutrition
    return {
        "summary": generate_food_summary(food_data),
        "nutrition": nutrition
    }

# API Endpoint to Get All Food Items
@router.get("/all")
def get_all_foods(db: Session = Depends(get_db)):
    foods = db.query(Food).all()
    
    if not foods:
        raise HTTPException(status_code=404, detail="No food items found in the database")
    
    result = []
    for food in foods:
        result.append({
            "id": food.id,
            "food_product": food.food_product,
            "amount": get_safe_attr(food, "amount"),
            "energy": get_safe_attr(food, "energy"),
            "carbohydrate": get_safe_attr(food, "carbohydrate"),
            "protein": get_safe_attr(food, "protein"),
            "total_fat": get_safe_attr(food, "total_fat"),
            "sodium": get_safe_attr(food, "sodium"),
            "iron": get_safe_attr(food, "iron")
        })
    
    return {"foods": result} 