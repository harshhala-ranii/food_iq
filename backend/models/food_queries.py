from sqlalchemy.orm import Session
from models.food import Food
from models.database import get_db
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_food_nutrition(food_name: str, db: Session):
    """
    Get nutritional information for the predicted food from the database
    
    Args:
        food_name (str): The name of the food to search for
        db (Session): Database session
        
    Returns:
        Food: The food object with nutritional information or None if not found
    """
    logger.debug(f"Searching for food: {food_name}")
    logger.debug(f"Input food_name type: {type(food_name)}")
    logger.debug(f"Input food_name value: '{food_name}'")
    
    # Try to find an exact match
    food = db.query(Food).filter(Food.food_product == food_name).first()
    logger.debug(f"Exact match result: {food}")
    
    # If no exact match, try to find a partial match
    if not food:
        logger.debug(f"No exact match found, trying partial match for: {food_name}")
        food = db.query(Food).filter(Food.food_product.ilike(f"%{food_name}%")).first()
        logger.debug(f"Partial match result: {food}")
    
    if food:
        logger.debug(f"Found food: {food.food_product}")
    else:
        logger.debug("No food found")
    
    return food

def display_food_details(food):
    """
    Display specific nutritional columns of a food object
    
    Args:
        food: The food object to display
    """
    logger.debug("Displaying food details")
    
    if food is None:
        logger.warning("No food found to display")
        print("No food found with that name.")
        return
    
    # Define the columns to display
    columns_to_display = [
        "food_product", "energy", "carbohydrate", "protein", 
        "total_fat", "sodium", "iron"
    ]
    
    print("\nFood Details:")
    print("-" * 50)
    for column in columns_to_display:
        value = getattr(food, column)
        logger.debug(f"Column: {column}, Value: {value}")
        print(f"{column}: {value}")
    print("-" * 50)

if __name__ == "__main__":
    logger.info("Starting food_queries.py as main script")
    
    # Get the database session from the generator
    logger.debug("Getting database session")
    db = next(get_db())
    
    try:
        logger.info("Testing with food: jalebi")
        food = get_food_nutrition("aloo_matar", db)
        display_food_details(food)
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
    finally:
        # Close the database session
        logger.debug("Closing database session")
        db.close()
        logger.info("Script completed")