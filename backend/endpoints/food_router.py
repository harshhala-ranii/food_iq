from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
import numpy as np
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import logging
from typing import Optional
from jose import JWTError, jwt

# Import from our modules
from models.food import Food
from models.database import get_db
from models.food_queries import get_food_nutrition, display_food_details
from models.user import UserProfile
from utils.food_recommendations import FoodRecommendation

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
def get_food_summary(
    food_name: str, 
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    logger.debug(f"Received request for food: {food_name}")
    logger.debug(f"Food name type: {type(food_name)}")
    logger.debug(f"Food name value: '{food_name}'")
    
    # Get user health conditions if token is provided
    user_health_conditions = []
    if authorization and authorization.startswith('Bearer '):
        token = authorization.split(' ')[1]
        try:
            # Use the exact same secret key as in auth.py
            secret_key = "food_iq_secret_key"
            
            # Decode the JWT token
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            user_id = payload.get("sub")
            logger.info(f"Decoded user_id from token: {user_id}")
            
            if user_id:
                # Get user profile directly from database
                logger.info(f"Querying user profile for user_id: {user_id}")
                profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
                logger.info(f"User profile found: {profile is not None}")
                
                if profile and profile.health_issues:
                    # Split health issues if they're comma-separated
                    health_issues = [issue.strip() for issue in profile.health_issues.split(',')]
                    user_health_conditions.extend(health_issues)
                    logger.info(f"Found user health conditions: {user_health_conditions}")
        except JWTError as e:
            logger.error(f"JWT token validation failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing token: {str(e)}", exc_info=True)
    
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

    # Generate recommendations using FoodRecommendation class
    logger.info(f"Generating recommendations for {food_name} with health conditions: {user_health_conditions}")
    food_recommendation = FoodRecommendation(food_name, user_health_conditions)
    recommendations = food_recommendation.evaluate()
    logger.info(f"Generated recommendations: {recommendations}")

    # Return the response with summary, nutrition, and recommendations
    return {
        "summary": generate_food_summary(food_data),
        "nutrition": nutrition,
        "recommendations": recommendations
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