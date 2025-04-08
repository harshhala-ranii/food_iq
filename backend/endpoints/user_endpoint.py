from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from models.database import get_db
from models.user import User, UserProfile, UserFoodLog, FoodRecommendation
from models.food import Food
from auth.auth import get_current_active_user
from auth.models import UserResponse, ProfileResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# Get current user data
@router.get("/me", response_model=UserResponse)
def get_current_user_data(current_user: User = Depends(get_current_active_user)):
    """Get current user data"""
    return current_user

# Get user profile
@router.get("/me/profile", response_model=ProfileResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

# Get user food logs
@router.get("/me/food-logs")
def get_user_food_logs(
    skip: int = 0,
    limit: int = 100,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get food logs for the current user with optional date filtering"""
    query = db.query(UserFoodLog).filter(UserFoodLog.user_id == current_user.id)
    
    # Apply date filters if provided
    if date_from:
        query = query.filter(UserFoodLog.date >= date_from)
    if date_to:
        query = query.filter(UserFoodLog.date <= date_to)
    
    # Get results with pagination
    logs = query.order_by(UserFoodLog.date.desc()).offset(skip).limit(limit).all()
    
    # Format the response
    result = []
    for log in logs:
        food = db.query(Food).filter(Food.id == log.food_id).first()
        if food:
            result.append({
                "id": log.id,
                "date": log.date,
                "meal_type": log.meal_type,
                "amount": log.amount,
                "food": food.to_dict()
            })
    
    return {"food_logs": result, "total": len(result)}

# Add food to user's log
@router.post("/me/food-logs", status_code=status.HTTP_201_CREATED)
def add_food_to_log(
    food_log: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a food item to user's food log"""
    # Check if food exists
    food = db.query(Food).filter(Food.id == food_log.get("food_id")).first()
    if not food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found"
        )
    
    # Create new food log entry
    new_log = UserFoodLog(
        user_id=current_user.id,
        food_id=food.id,
        meal_type=food_log.get("meal_type", "Other"),
        amount=food_log.get("amount", 1.0),
        date=food_log.get("date")
    )
    
    try:
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
        
        return {
            "id": new_log.id,
            "user_id": new_log.user_id,
            "food_id": new_log.food_id,
            "meal_type": new_log.meal_type,
            "amount": new_log.amount,
            "date": new_log.date
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to add food to log"
        )

# Get user recommendations
@router.get("/me/recommendations")
def get_user_recommendations(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get food recommendations for the current user"""
    recommendations = db.query(FoodRecommendation)\
        .filter(FoodRecommendation.user_id == current_user.id)\
        .order_by(FoodRecommendation.created_at.desc())\
        .offset(skip).limit(limit).all()
    
    # Format the response
    result = []
    for rec in recommendations:
        # Get associated food items if they exist
        food_items = []
        if rec.food_ids:
            food_ids = [int(id) for id in rec.food_ids.split(",") if id.strip().isdigit()]
            food_items = db.query(Food).filter(Food.id.in_(food_ids)).all()
            food_items = [food.to_dict() for food in food_items]
        
        result.append({
            "id": rec.id,
            "recommendation_text": rec.recommendation_text,
            "created_at": rec.created_at,
            "source": rec.source,
            "context": rec.context,
            "food_items": food_items
        })
    
    return {"recommendations": result, "total": len(result)}

# Delete user account
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete current user account and all associated data (GDPR compliance)"""
    try:
        # Delete associated data first (due to foreign key constraints)
        db.query(UserProfile).filter(UserProfile.user_id == current_user.id).delete()
        db.query(UserFoodLog).filter(UserFoodLog.user_id == current_user.id).delete()
        db.query(FoodRecommendation).filter(FoodRecommendation.user_id == current_user.id).delete()
        
        # Delete the user
        db.query(User).filter(User.id == current_user.id).delete()
        
        db.commit()
        return None
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account: {str(e)}"
        ) 