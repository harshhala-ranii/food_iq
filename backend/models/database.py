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

# Construct database URL
if os.getenv("ENVIRONMENT") == "docker":
    # For Docker deployment
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}"
else:
    # For local development
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Check if database URL is set manually
OVERRIDE_DB_URL = os.getenv("DATABASE_URL")
if OVERRIDE_DB_URL:
    SQLALCHEMY_DATABASE_URL = OVERRIDE_DB_URL

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