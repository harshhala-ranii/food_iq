from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Ensure credentials are not None
if not DB_USERNAME or not DB_PASSWORD:
    raise ValueError("Database credentials are missing! Please set DB_USERNAME and DB_PASSWORD as environment variables.")

# For local development
LOCAL_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/food_db"
# For Docker environment
DOCKER_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@postgres:5432/food_db"

# Choose the appropriate URL based on environment
# If running in Docker, use the service name 'postgres' as the host
DATABASE_URL = DOCKER_DATABASE_URL if os.getenv("IN_DOCKER") else LOCAL_DATABASE_URL

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 