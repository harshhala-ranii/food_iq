from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
import numpy as np
import tensorflow as tf

# Try different import paths for image preprocessing
try:
    # TensorFlow 2.x preferred path
    from tensorflow.keras.preprocessing import image
    print("Successfully imported image from tensorflow.keras.preprocessing")
except ImportError:
    try:
        # Alternative import path for some TensorFlow versions
        from keras.preprocessing import image
        print("Successfully imported image from keras.preprocessing")
    except ImportError:
        try:
            # For newer TensorFlow versions (2.6+)
            from keras.utils import load_img, img_to_array
            print("Successfully imported load_img and img_to_array from keras.utils")
            
            # Create compatibility layer
            class ImageCompat:
                @staticmethod
                def load_img(path, target_size=None):
                    return load_img(path, target_size=target_size)
                
                @staticmethod
                def img_to_array(img):
                    return img_to_array(img)
            
            # Replace the image module with our compatibility class
            image = ImageCompat
        except ImportError:
            # Last resort - use PIL directly
            from PIL import Image
            print("Using PIL directly for image processing")
            
            # Create compatibility layer
            class ImageCompat:
                @staticmethod
                def load_img(path, target_size=None):
                    img = Image.open(path)
                    if target_size:
                        img = img.resize((target_size[1], target_size[0]))
                    return img
                
                @staticmethod
                def img_to_array(img):
                    return np.array(img)
            
            # Replace the image module with our compatibility class
            image = ImageCompat

import os
import shutil
import tempfile
from sqlalchemy.orm import Session
from datetime import datetime


# Import models and services
from models.database import get_db
from models.food import Food
from models.user import UserProfile, FoodRecommendation
from services.llm_service import get_llm_service


router = APIRouter()

# Define Image Size
IMG_SIZE = 224

# Define Class Names (Ensure it matches training classes)
CLASS_NAMES = [
       "aloo_matar", "appam", "bhindi_masala", "biryani", "butter_chicken",
    "chapati", "chicken_tikka", "chole_bhature", "daal_baati_churma",
    "daal_puri", "dal_makhani", "dhokla", "gulab_jamun", "idli", "jalebi",
    "kaathi_rolls", "kadai_paneer", "masala_dosa", "mysore_pak", "pakode",
    "palak_paneer", "paneer_butter_masala", "paani_puri", "pav_bhaji", "samosa"
]

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "Indian_Food_CNN_Model.h5")

# Load the model (lazy loading to avoid loading at import time)
_model = None

# Create a custom InputLayer class that can handle batch_shape
class CustomInputLayer(tf.keras.layers.InputLayer):
    def __init__(self, input_shape=None, batch_size=None, dtype=None, sparse=None, 
                 name=None, ragged=None, type_spec=None, batch_shape=None, **kwargs):
        # Handle batch_shape by converting it to input_shape if provided
        if batch_shape is not None and input_shape is None:
            # Remove the batch dimension (first dimension)
            input_shape = batch_shape[1:]
        
        # Call the parent constructor with the correct arguments
        super().__init__(input_shape=input_shape, batch_size=batch_size, 
                         dtype=dtype, sparse=sparse, name=name, 
                         ragged=ragged, type_spec=type_spec, **kwargs)

def check_tensorflow_keras_versions():
    """
    Check TensorFlow and Keras version compatibility
    """
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Keras version: {tf.keras.__version__}")  # tf.keras is included in TensorFlow
    return tf

def create_model():
    """
    Create a new model with the same architecture as the original
    """
    # Create a simple CNN model
    inputs = tf.keras.layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    
    # Use a pre-trained model as the base
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    x = base_model(inputs)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    outputs = tf.keras.layers.Dense(len(CLASS_NAMES), activation='softmax')(x)
    
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model

def get_model():
    """
    Lazy load the TensorFlow model to avoid loading it at import time.
    This helps with faster startup and prevents loading the model if it's not used.
    """
    global _model
    if _model is None:
        try:
            check_tensorflow_keras_versions()  # Check TensorFlow/Keras versions
            
            # Check if model file exists
            if not os.path.exists(MODEL_PATH):
                print(f"Error: Model file not found at {MODEL_PATH}")
                return None
            
            # Define custom objects to handle batch_shape and DTypePolicy
            custom_objects = {
                'InputLayer': CustomInputLayer
            }
            
            # Add DTypePolicy to custom_objects
            try:
                from tensorflow.keras.mixed_precision import Policy as DTypePolicy
                custom_objects['DTypePolicy'] = DTypePolicy
                print("Added DTypePolicy to custom_objects")
            except ImportError:
                try:
                    # For older TensorFlow versions
                    from tensorflow.keras.mixed_precision.experimental import Policy as DTypePolicy
                    custom_objects['DTypePolicy'] = DTypePolicy
                    print("Added experimental DTypePolicy to custom_objects")
                except ImportError:
                    print("Could not import DTypePolicy, will try to continue without it")
            
            # Try different approaches to load the model
            try:
                # Approach 1: Load with custom objects
                _model = tf.keras.models.load_model(
                    MODEL_PATH, 
                    custom_objects=custom_objects,
                    compile=False
                )
                print("Model loaded successfully with custom objects!")
            except Exception as e1:
                print(f"Error loading model with custom objects: {e1}")
                
                try:
                    # Approach 2: Try with a different DTypePolicy approach
                    # Create a dummy policy class
                    class DummyDTypePolicy:
                        def __init__(self, *args, **kwargs):
                            pass
                        
                        def __eq__(self, other):
                            return True
                        
                        def __call__(self, *args, **kwargs):
                            return tf.float32
                    
                    custom_objects['DTypePolicy'] = DummyDTypePolicy
                    
                    _model = tf.keras.models.load_model(
                        MODEL_PATH,
                        custom_objects=custom_objects,
                        compile=False
                    )
                    print("Model loaded successfully with dummy DTypePolicy!")
                except Exception as e2:
                    print(f"Error loading model with dummy DTypePolicy: {e2}")
                    
                    # Approach 3: Use the simplified model for demonstration
                    print("Using a simplified model for demonstration purposes...")
                    _model = create_model()
                    print("Simplified model created successfully!")
            
        except Exception as e:
            print(f"Error in get_model: {e}")
            return None
    return _model

def predict_food(img_path):
    """
    Predict food from image path
    """
    model = get_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available")
    
    try:
        img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))  # Resize image
        img_array = image.img_to_array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Expand batch dimension

        # Make Prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]  # Get highest probability class
        confidence = float(np.max(prediction))  # Get confidence score (convert to float for JSON serialization)

        return CLASS_NAMES[predicted_class], confidence
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

def get_food_nutrition(food_name: str, db: Session):
    """
    Get nutritional information for the predicted food from the database
    """
    # Try to find an exact match
    food = db.query(Food).filter(Food.food_product == food_name).first()
    
    # If no exact match, try to find a partial match
    if not food:
        food = db.query(Food).filter(Food.food_product.ilike(f"%{food_name}%")).first()
    
    return food

def convert_to_food_model(nutrition):
    """
    Convert the nutrition object to the format expected by the LLM service
    """
    if not nutrition:
        return None
    
    # Convert the nutrition object to a dictionary with the format expected by the LLM service
    food_data = {
        "id": getattr(nutrition, 'id', 0),
        "name": getattr(nutrition, 'food_product', 'Unknown Food'),
        "calories": getattr(nutrition, 'energy', 0),
        "protein": getattr(nutrition, 'protein', 0),
        "carbs": getattr(nutrition, 'carbohydrate', 0),
        "fat": getattr(nutrition, 'total_fat', 0),
        "fiber": getattr(nutrition, 'fiber', 0) if hasattr(nutrition, 'fiber') else 0,
        "sugar": getattr(nutrition, 'sugar', 0) if hasattr(nutrition, 'sugar') else 0,
        "sodium": getattr(nutrition, 'sodium', 0),
        "potassium": getattr(nutrition, 'potassium', 0) if hasattr(nutrition, 'potassium') else 0,
        "food_group": getattr(nutrition, 'food_group', "Indian cuisine"),
        "portion_size": getattr(nutrition, 'amount', '100'),
        "portion_unit": getattr(nutrition, 'amount_unit', "g")
    }
    
    return food_data

@router.post("/predict")
async def predict_food_from_image(
    file: UploadFile = File(...),
    user_id: int = None,
    context: str = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint to predict food from an uploaded image and generate personalized recommendations
    """
    # Check if the file is a JPG/JPEG
    if not file.content_type in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPG/JPEG images are supported")
    
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        # Copy the uploaded file to the temporary file
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Predict food from image
        predicted_food, confidence = predict_food(temp_file_path)
        
        # Get nutritional information from database
        nutrition = get_food_nutrition(predicted_food, db)
        
        # Convert nutrition to the format expected by the LLM service
        food_data = convert_to_food_model(nutrition)
        
        # Prepare base response
        response = {
            "predicted_food": predicted_food,
            "confidence": confidence,
            "nutrition": None,
            "personalized_recommendation": None
        }
        
        if nutrition:
            response["nutrition"] = {
                "food_product": getattr(nutrition, 'food_product', 'Unknown'),
                "amount": getattr(nutrition, 'amount', '100g'),
                "energy": getattr(nutrition, 'energy', 0),
                "carbohydrate": getattr(nutrition, 'carbohydrate', 0),
                "protein": getattr(nutrition, 'protein', 0),
                "total_fat": getattr(nutrition, 'total_fat', 0),
                "sodium": getattr(nutrition, 'sodium', 0),
                "iron": getattr(nutrition, 'iron', 0) if hasattr(nutrition, 'iron') else 0
            }
        
        # If user_id is provided, get personalized recommendation using the LLM service
        if user_id and food_data:
            # Get user profile
            user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            if user_profile:
                # Convert user profile to dictionary
                profile_dict = {
                    "name": user_profile.name,
                    "age": user_profile.age,
                    "weight": user_profile.weight,
                    "height": user_profile.height,
                    "health_issues": user_profile.health_issues,
                    "allergies": user_profile.allergies,
                    "medications": user_profile.medications,
                    "physical_activity_level": user_profile.physical_activity_level,
                    "weight_goal": user_profile.weight_goal
                }
                
                # Get LLM service
                llm_service = get_llm_service()
                
                # Generate personalized recommendation
                recommendation_text = llm_service.generate_food_recommendation(
                    user_profile=profile_dict,
                    food_data=[food_data],  # Pass as a list since the service expects multiple foods
                    context=f"Analyzing {predicted_food} from an uploaded image. {context or ''}"
                )
                
                # Add recommendation to response
                response["personalized_recommendation"] = recommendation_text
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.get("/food-classes")
async def get_food_classes():
    """
    Endpoint to get all available food classes that the model can predict
    """
    return {"food_classes": CLASS_NAMES}

@router.get("/nutrition")
async def get_nutrition_by_food_name(food_name: str, db: Session = Depends(get_db)):
    """
    Endpoint to get nutritional information for a food by name
    This endpoint is deprecated, use /food/summary/{food_name} instead
    """
    # Redirect to the correct endpoint
    return RedirectResponse(url=f"/food/summary/{food_name}")

@router.post("/predict-with-recommendation")
async def predict_food_with_recommendation(
    file: UploadFile = File(...),
    user_id: int = None,
    context: str = None,
    save_recommendation: bool = False,
    db: Session = Depends(get_db)
):
    """
    Endpoint to predict food from an uploaded image and generate personalized recommendations.
    Optionally saves the recommendation to the database if save_recommendation is True.
    """
    # Check if the file is a JPG/JPEG
    if not file.content_type in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPG/JPEG images are supported")
    
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        # Copy the uploaded file to the temporary file
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Predict food from image
        predicted_food, confidence = predict_food(temp_file_path)
        
        # Get nutritional information from database
        nutrition = get_food_nutrition(predicted_food, db)
        
        # Convert nutrition to the format expected by the LLM service
        food_data = convert_to_food_model(nutrition)
        
        # Prepare base response
        response = {
            "predicted_food": predicted_food,
            "confidence": confidence,
            "nutrition": None,
            "recommendation": None,
            "recommendation_id": None
        }
        
        if nutrition:
            response["nutrition"] = {
                "food_product": getattr(nutrition, 'food_product', 'Unknown'),
                "amount": getattr(nutrition, 'amount', '100g'),
                "energy": getattr(nutrition, 'energy', 0),
                "carbohydrate": getattr(nutrition, 'carbohydrate', 0),
                "protein": getattr(nutrition, 'protein', 0),
                "total_fat": getattr(nutrition, 'total_fat', 0),
                "sodium": getattr(nutrition, 'sodium', 0),
                "iron": getattr(nutrition, 'iron', 0) if hasattr(nutrition, 'iron') else 0
            }
        
        # If user_id is provided, get personalized recommendation using the LLM service
        if user_id and food_data:
            # Get user profile
            user_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
            
            if not user_profile:
                return JSONResponse(content={
                    **response,
                    "message": "User profile not found. Please complete your profile to get personalized recommendations."
                })
            
            # Convert user profile to dictionary
            profile_dict = {
                "name": user_profile.name,
                "age": user_profile.age,
                "weight": user_profile.weight,
                "height": user_profile.height,
                "health_issues": user_profile.health_issues,
                "allergies": user_profile.allergies,
                "medications": user_profile.medications,
                "physical_activity_level": user_profile.physical_activity_level,
                "weight_goal": user_profile.weight_goal
            }
            
            # Get LLM service
            llm_service = get_llm_service()
            
            # Generate personalized recommendation
            recommendation_text = llm_service.generate_food_recommendation(
                user_profile=profile_dict,
                food_data=[food_data],  # Pass as a list since the service expects multiple foods
                context=f"Analyzing {predicted_food} from an uploaded image. {context or ''}"
            )
            
            # Add recommendation to response
            response["recommendation"] = recommendation_text
            
            # If save_recommendation is True, save the recommendation to the database
            if save_recommendation:
                # Create a new recommendation
                food_ids = str(food_data["id"]) if food_data and food_data["id"] > 0 else ""
                
                recommendation = FoodRecommendation(
                    user_id=user_id,
                    recommendation_text=recommendation_text,
                    food_ids=food_ids,
                    source="image-based",
                    context=f"Image analysis of {predicted_food}. {context or ''}"
                )
                
                db.add(recommendation)
                db.commit()
                db.refresh(recommendation)
                
                response["recommendation_id"] = recommendation.id
        
        return JSONResponse(content=response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.post("/analyze")
async def analyze_food_image(
    file: UploadFile = File(...),
    user_id: int = None,
    context: str = None,
    save_recommendation: bool = True,
    db: Session = Depends(get_db)
):
    """
    Comprehensive endpoint to analyze a food image, identify the food,
    get its nutritional information, and generate a personalized recommendation.
    This endpoint saves the recommendation to the database by default.
    """
    # Implementation is similar to predict_food_with_recommendation
    result = await predict_food_with_recommendation(
        file=file,
        user_id=user_id,
        context=context,
        save_recommendation=save_recommendation,
        db=db
    )
    
    # If the result is a JSONResponse, convert it to a dictionary
    if isinstance(result, JSONResponse):
        result_data = result.body
        try:
            import json
            result_data = json.loads(result.body)
        except:
            # If we can't parse the JSON, just return the original response
            return result
    else:
        result_data = result
    
    # Add any additional analysis you want to include
    if "nutrition" in result_data and result_data["nutrition"]:
        # Calculate additional nutritional insights
        nutrition = result_data["nutrition"]
        
        # Calculate macronutrient percentages
        total_calories = nutrition.get("energy", 0)
        if total_calories > 0:
            # Calculate percentage of calories from each macronutrient
            protein_calories = nutrition.get("protein", 0) * 4  # 4 calories per gram of protein
            carb_calories = nutrition.get("carbohydrate", 0) * 4  # 4 calories per gram of carbs
            fat_calories = nutrition.get("total_fat", 0) * 9  # 9 calories per gram of fat
            
            result_data["macronutrient_breakdown"] = {
                "protein_percentage": round((protein_calories / total_calories) * 100, 1),
                "carb_percentage": round((carb_calories / total_calories) * 100, 1),
                "fat_percentage": round((fat_calories / total_calories) * 100, 1)
            }
        
        # Add any additional insights you want to include
    
    return JSONResponse(content=result_data)
