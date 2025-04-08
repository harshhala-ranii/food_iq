#!/usr/bin/env python3
"""
Script to initialize authentication-related tables and add test user data.
This should be run manually when setting up the database for the first time.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models and database
from models.database import engine, Base
from models.user import User, UserProfile
from auth.auth import get_password_hash

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def init_auth_tables():
    """Create authentication-related tables"""
    logger.info("Creating authentication tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Authentication tables created successfully")

def add_test_user():
    """Add initial test user with profile"""
    logger.info("Adding test user...")
    
    # Get a database session
    from models.database import SessionLocal
    db = SessionLocal()
    
    try:
        # Add test user with profile
        if db.query(User).filter(User.email == "test@example.com").first() is None:
            test_user = User(
                email="test@example.com",
                hashed_password=get_password_hash("password123"),
                is_active=True
            )
            db.add(test_user)
            db.flush()
            
            test_profile = UserProfile(
                user_id=test_user.id,
                name="Test User",
                age=30,
                number="1234567890",
                weight=70.5,
                height=175.0,
                health_issues="None",
                allergies="Peanuts",
                medications="None",
                blood_type="O+",
                smoking_status="Never",
                alcohol_consumption="Occasional",
                physical_activity_level="Moderate",
                dietary_preferences="Balanced",
                weight_goal="maintain",
                calorie_target=2000
            )
            db.add(test_profile)
            
            db.commit()
            logger.info("Added test user with profile")
        else:
            logger.info("Test user already exists")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding test user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_auth_tables()
    add_test_user() 