import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.schema.schemas import Base, Food
from database import get_db
from backend.endpoints.get_food import app

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Create test data
    db = TestingSessionLocal()
    
    # Add test food items
    test_foods = [
        Food(
            food_product="Apple",
            average_volume=100.0,
            amount=100.0,
            energy=52.0,
            carbohydrate=14.0,
            protein=0.3,
            total_fat=0.2,
            sodium=1.0,
            iron=0.1
        ),
        Food(
            food_product="Banana",
            average_volume=120.0,
            amount=120.0,
            energy=89.0,
            carbohydrate=23.0,
            protein=1.1,
            total_fat=0.3,
            sodium=1.0,
            iron=0.3
        )
    ]
    
    for food in test_foods:
        db.add(food)
    
    db.commit()
    
    yield db
    
    # Clean up
    db.query(Food).delete()
    db.commit()
    db.close()

def test_get_food_summary_success(test_db):
    """Test successful retrieval of food summary."""
    response = client.get("/food/summary/Apple")
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert "Apple" in data["summary"]
    assert "52.0 kcal of energy" in data["summary"]

def test_get_food_summary_not_found(test_db):
    """Test food not found case."""
    response = client.get("/food/summary/NonExistentFood")
    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found"

def test_get_food_summary_multiple_results(test_db):
    """Test case when multiple food items match the query."""
    # Add another apple item to create ambiguity
    db = test_db
    db.add(Food(
        food_product="Green Apple",
        average_volume=110.0,
        amount=110.0,
        energy=55.0,
        carbohydrate=14.5,
        protein=0.4,
        total_fat=0.1,
        sodium=1.0,
        iron=0.1
    ))
    db.commit()
    
    # This should now find both "Apple" and "Green Apple"
    response = client.get("/food/summary/Apple")
    assert response.status_code == 400
    assert "Multiple food items found" in response.json()["detail"] 