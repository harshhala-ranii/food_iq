from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
import os
import shutil
import tempfile
from sqlalchemy.orm import Session
from database import get_db
from schemas import Food

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

def check_tensorflow_keras_versions():
    """
    Check TensorFlow and Keras version compatibility
    """
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    print(f"Keras version: {tf.keras.__version__}")  # tf.keras is included in TensorFlow
    return tf

def get_model():
    """
    Lazy load the TensorFlow model to avoid loading it at import time.
    This helps with faster startup and prevents loading the model if it's not used.
    """
    global _model
    if _model is None:
        try:
            tf = check_tensorflow_keras_versions()  # Check TensorFlow/Keras versions
            _model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'InputLayer': tf.keras.layers.InputLayer})
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            # Return a placeholder model or None
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

@router.post("/predict")
async def predict_food_from_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint to predict food from an uploaded image
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
        
        # Prepare response
        response = {
            "predicted_food": predicted_food,
            "confidence": confidence,
            "nutrition": None
        }
        
        if nutrition:
            response["nutrition"] = {
                "food_product": nutrition.food_product,
                "amount": nutrition.amount,
                "energy": nutrition.energy,
                "carbohydrate": nutrition.carbohydrate,
                "protein": nutrition.protein,
                "total_fat": nutrition.total_fat,
                "sodium": nutrition.sodium,
                "iron": nutrition.iron
            }
        
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

# Separate test to check if the model loads properly:
def test_model_loading():
    """
    A simple function to test if the model can load properly.
    You can use this to debug the model loading outside FastAPI.
    """
    try:
        model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'InputLayer': tf.keras.layers.InputLayer})
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
