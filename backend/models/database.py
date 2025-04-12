import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database credentials from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "food_db")

# Check if database URL is set manually
OVERRIDE_DB_URL = os.getenv("DATABASE_URL")
if OVERRIDE_DB_URL:
    # Use the manually set database URL
    SQLALCHEMY_DATABASE_URL = OVERRIDE_DB_URL
    print(f"Using manually set database URL: {SQLALCHEMY_DATABASE_URL}")
else:
    # Construct database URL based on environment
    if os.getenv("ENVIRONMENT") == "docker":
        # For Docker deployment - use 'postgres' as the host name
        SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@postgres:{DB_PORT}/{DB_NAME}"
        print(f"Using Docker database URL: {SQLALCHEMY_DATABASE_URL}")
    else:
        # For local development
        SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Using local database URL: {SQLALCHEMY_DATABASE_URL}")

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 