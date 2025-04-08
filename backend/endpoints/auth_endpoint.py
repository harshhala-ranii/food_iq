from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from typing import List

from models.database import get_db
from models.user import User, UserProfile
from auth.auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token, 
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from auth.models import (
    Token, 
    UserCreate, 
    UserResponse, 
    ProfileCreate, 
    ProfileUpdate, 
    ProfileResponse,
    UserProfileCreate
)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

@router.post("/register-with-profile", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_with_profile(user_data: UserProfileCreate, db: Session = Depends(get_db)):
    """Register a new user with profile information"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(email=user_data.email, hashed_password=hashed_password)
    
    try:
        db.add(user)
        db.flush()  # To get user id without committing transaction
        
        # Create profile
        profile_data = user_data.profile
        profile = UserProfile(
            user_id=user.id,
            name=profile_data.name,
            age=profile_data.age,
            number=profile_data.number,
            weight=profile_data.weight,
            height=profile_data.height,
            health_issues=profile_data.health_issues,
            allergies=profile_data.allergies,
            medications=profile_data.medications,
            blood_type=profile_data.blood_type,
            smoking_status=profile_data.smoking_status,
            alcohol_consumption=profile_data.alcohol_consumption,
            physical_activity_level=profile_data.physical_activity_level
        )
        
        db.add(profile)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login endpoint to get access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email
    }

@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/users/me/profile", response_model=ProfileResponse)
def read_user_profile(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.post("/users/me/profile", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(profile_data: ProfileCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Create user profile for current user"""
    # Check if profile already exists
    existing_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists"
        )
    
    # Create profile
    profile = UserProfile(
        user_id=current_user.id,
        name=profile_data.name,
        age=profile_data.age,
        number=profile_data.number,
        weight=profile_data.weight,
        height=profile_data.height,
        health_issues=profile_data.health_issues,
        allergies=profile_data.allergies,
        medications=profile_data.medications,
        blood_type=profile_data.blood_type,
        smoking_status=profile_data.smoking_status,
        alcohol_consumption=profile_data.alcohol_consumption,
        physical_activity_level=profile_data.physical_activity_level
    )
    
    try:
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create profile"
        )

@router.put("/users/me/profile", response_model=ProfileResponse)
def update_user_profile(profile_data: ProfileUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update current user's profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile fields if provided
    if profile_data.name is not None:
        profile.name = profile_data.name
    if profile_data.age is not None:
        profile.age = profile_data.age
    if profile_data.number is not None:
        profile.number = profile_data.number
    if profile_data.weight is not None:
        profile.weight = profile_data.weight
    if profile_data.height is not None:
        profile.height = profile_data.height
    if profile_data.health_issues is not None:
        profile.health_issues = profile_data.health_issues
    if profile_data.allergies is not None:
        profile.allergies = profile_data.allergies
    if profile_data.medications is not None:
        profile.medications = profile_data.medications
    if profile_data.blood_type is not None:
        profile.blood_type = profile_data.blood_type
    if profile_data.smoking_status is not None:
        profile.smoking_status = profile_data.smoking_status
    if profile_data.alcohol_consumption is not None:
        profile.alcohol_consumption = profile_data.alcohol_consumption
    if profile_data.physical_activity_level is not None:
        profile.physical_activity_level = profile_data.physical_activity_level
    
    try:
        db.commit()
        db.refresh(profile)
        return profile
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update profile"
        ) 