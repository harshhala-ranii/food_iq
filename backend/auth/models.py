from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# Token response models
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

# User authentication models
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

# Profile models
class ProfileBase(BaseModel):
    name: str
    age: int
    number: str
    weight: float
    height: float
    health_issues: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    blood_type: Optional[str] = None
    smoking_status: Optional[str] = None  # e.g., "Never", "Former", "Current"
    alcohol_consumption: Optional[str] = None  # e.g., "None", "Occasional", "Regular"
    physical_activity_level: Optional[str] = None  # e.g., "Sedentary", "Active", "Very Active"
    dietary_preferences: Optional[str] = None
    weight_goal: Optional[str] = None
    calorie_target: Optional[int] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    number: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    health_issues: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    blood_type: Optional[str] = None
    smoking_status: Optional[str] = None
    alcohol_consumption: Optional[str] = None
    physical_activity_level: Optional[str] = None
    dietary_preferences: Optional[str] = None
    weight_goal: Optional[str] = None
    calorie_target: Optional[int] = None

class ProfileResponse(ProfileBase):
    id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Combined user and profile registration model
class UserProfileCreate(BaseModel):
    email: EmailStr
    password: str
    profile: ProfileCreate
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

# Food models for API responses
class FoodBase(BaseModel):
    food_product: str
    amount: float
    amount_unit: str = "g"
    energy: float
    carbohydrate: float
    protein: float
    total_fat: float

class FoodCreate(FoodBase):
    sugar: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    potassium: Optional[float] = None
    calcium: Optional[float] = None
    iron: Optional[float] = None
    food_group: Optional[str] = None

class FoodResponse(FoodBase):
    id: int
    sugar: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    iron: Optional[float] = None
    food_group: Optional[str] = None

    class Config:
        orm_mode = True 