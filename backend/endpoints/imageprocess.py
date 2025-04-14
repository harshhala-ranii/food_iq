from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
import os
import shutil
import tempfile
from sqlalchemy.orm import Session
import logging
from models.food_queries import get_food_nutrition
from PIL import Image
# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import models and services
from models.database import get_db, SQLALCHEMY_DATABASE_URL
from models.food import Food  # Import Food model directly
from models.food_queries import display_food_details

# Try different import paths for image preprocessing
try:
    # TensorFlow 2.x preferred path
    from tensorflow.keras.preprocessing import image
    logger.info("Successfully imported image from tensorflow.keras.preprocessing")
except ImportError:
    try:
        # Alternative import path for some TensorFlow versions
        from keras.preprocessing import image
        logger.info("Successfully imported image from keras.preprocessing")
    except ImportError:
        try:
            # For newer TensorFlow versions (2.6+)
            from keras.utils import load_img, img_to_array
            logger.info("Successfully imported load_img and img_to_array from keras.utils")
            
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
            logger.info("Using PIL directly for image processing")
            
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

router = APIRouter()

# Define Image Size
IMG_SIZE = 224
logger.debug(f"Image size set to: {IMG_SIZE}")

# Define Class Names (Ensure it matches training classes)
CLASS_NAMES = [
       "aloo_matar", "appam", "bhindi_masala", "biryani", "butter_chicken",
    "chapati", "chicken_tikka", "chole_bhature", "daal_baati_churma",
    "daal_puri", "dal_makhani", "dhokla", "gulab_jamun", "idli", "jalebi",
    "kaathi_rolls", "kadai_paneer", "masala_dosa", "mysore_pak", "pakode",
    "palak_paneer", "paneer_butter_masala", "paani_puri", "pav_bhaji", "samosa"
]
logger.debug(f"Number of food classes: {len(CLASS_NAMES)}")

# Path to the model file
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "Indian_Food_CNN_Model.h5")
logger.debug(f"Model path: {MODEL_PATH}")

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
    logger.info(f"TensorFlow version: {tf.__version__}")
    logger.info(f"Keras version: {tf.keras.__version__}")  # tf.keras is included in TensorFlow
    return tf

def create_model():
    """
    Create a new model with the same architecture as the original
    """
    logger.info("Creating a new model with MobileNetV2 base")
    
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
    logger.info("Model created successfully")
    return model

def get_model():
    """
    Lazy load the TensorFlow model to avoid loading it at import time.
    This helps with faster startup and prevents loading the model if it's not used.
    """
    global _model
    if _model is None:
        try:
            logger.info("Loading model...")
            check_tensorflow_keras_versions()  # Check TensorFlow/Keras versions
            
            # Check if model file exists
            if not os.path.exists(MODEL_PATH):
                logger.error(f"Error: Model file not found at {MODEL_PATH}")
                return None
            
            # Define custom objects to handle batch_shape and DTypePolicy
            custom_objects = {
                'InputLayer': CustomInputLayer
            }
            
            # Add DTypePolicy to custom_objects
            try:
                from tensorflow.keras.mixed_precision import Policy as DTypePolicy
                custom_objects['DTypePolicy'] = DTypePolicy
                logger.info("Added DTypePolicy to custom_objects")
            except ImportError:
                try:
                    # For older TensorFlow versions
                    from tensorflow.keras.mixed_precision.experimental import Policy as DTypePolicy
                    custom_objects['DTypePolicy'] = DTypePolicy
                    logger.info("Added experimental DTypePolicy to custom_objects")
                except ImportError:
                    logger.warning("Could not import DTypePolicy, will try to continue without it")
            
            # Try different approaches to load the model
            try:
                # Approach 1: Load with custom objects
                logger.info("Attempting to load model with custom objects")
                _model = tf.keras.models.load_model(
                    MODEL_PATH, 
                    custom_objects=custom_objects,
                    compile=False
                )
                logger.info("Model loaded successfully with custom objects!")
            except Exception as e1:
                logger.error(f"Error loading model with custom objects: {e1}")
                
                try:
                    # Approach 2: Try with a different DTypePolicy approach
                    # Create a dummy policy class
                    logger.info("Attempting to load model with dummy DTypePolicy")
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
                    logger.info("Model loaded successfully with dummy DTypePolicy!")
                except Exception as e2:
                    logger.error(f"Error loading model with dummy DTypePolicy: {e2}")
                    
                    # Approach 3: Use the simplified model for demonstration
                    logger.warning("Using a simplified model for demonstration purposes...")
                    _model = create_model()
                    logger.info("Simplified model created successfully!")
            
        except Exception as e:
            logger.error(f"Error in get_model: {e}", exc_info=True)
            return None
    return _model

def predict_food(img_path):
    """
    Predict food from image path
    """
    logger.info(f"Predicting food from image: {img_path}")
    
    model = get_model()
    if model is None:
        logger.error("Model not available")
        raise HTTPException(status_code=500, detail="Model not available")
    
    try:
        logger.debug("Loading and preprocessing image")
        img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))  # Resize image
        img_array = image.img_to_array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Expand batch dimension

        # Make Prediction
        logger.debug("Making prediction")
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]  # Get highest probability class
        confidence = float(np.max(prediction))  # Get confidence score (convert to float for JSON serialization)
        
        logger.info(f"Predicted food: {CLASS_NAMES[predicted_class]} with confidence: {confidence}")
        return CLASS_NAMES[predicted_class], confidence
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

# Direct database query function to use as a fallback
def direct_get_food_nutrition(food_name: str, db: Session):
    """
    Direct database query function to use as a fallback
    """
    logger.debug(f"Direct database query for food: {food_name}")
    
    # Try to find an exact match
    food = db.query(Food).filter(Food.food_product == food_name).first()
    logger.debug(f"Direct query exact match result: {food}")
    
    # If no exact match, try to find a partial match
    if not food:
        logger.debug(f"No exact match found, trying partial match for: {food_name}")
        food = db.query(Food).filter(Food.food_product.ilike(f"%{food_name}%")).first()
        logger.debug(f"Direct query partial match result: {food}")
    
    return food

# Function to check database connection
def check_db_connection(db: Session):
    """
    Check if the database connection is working and print the current database URL
    """
    logger.info(f"Current database URL: {SQLALCHEMY_DATABASE_URL}")
    
    try:
        # Try to execute a simple query
        result = db.execute("SELECT 1").scalar()
        logger.info(f"Database connection successful. Test query result: {result}")
        
        # Check if the food table exists and has data
        food_count = db.query(Food).count()
        logger.info(f"Food table exists and has {food_count} records")
        
        # List all food items in the database
        foods = db.query(Food.food_product).all()
        food_names = [food[0] for food in foods]
        logger.info(f"Food items in database: {food_names}")
        
        return True
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}", exc_info=True)
        return False

@router.post("/predict")
async def predict_food_from_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint to predict food from an uploaded image and get nutritional information
    """
    logger.info(f"Received image file: {file.filename}, content type: {file.content_type}")
    
    # Check database connection
    check_db_connection(db)
    
    # Check if the file is a JPG/JPEG
    if not file.content_type in ["image/jpeg", "image/jpg"]:
        logger.warning(f"Unsupported file type: {file.content_type}")
        raise HTTPException(status_code=400, detail="Only JPG/JPEG images are supported")
    
    # Read the file contents once
    contents = await file.read()
    
    # Create a temporary file to store the uploaded image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        # Write the contents to the temporary file
        logger.debug(f"Creating temporary file: {temp_file.name}")
        temp_file.write(contents)
        temp_file_path = temp_file.name
    
    try:
        # Predict food from image
        logger.info("Predicting food from image")
        predicted_food, confidence = predict_food(temp_file_path)
        
        # Get nutritional information from database using the food_queries module
        logger.info(f"Getting nutritional information for: {predicted_food}")
        
        # Try the imported function first
        nutrition = get_food_nutrition(predicted_food, db)
        
        # If that fails, try the direct query function
        if nutrition is None:
            logger.warning(f"Imported get_food_nutrition failed, trying direct query for: {predicted_food}")
            nutrition = direct_get_food_nutrition(predicted_food, db)
        
        # Calculate volume and adjust nutrition
        logger.info("Calculating volume and adjusting nutrition")
        try:
            # Create a new BytesIO object from the saved contents
            logger.debug("Creating BytesIO object from image contents")
            image_stream = BytesIO(contents)
            
            logger.debug("Opening image with PIL and converting to RGB")
            image = Image.open(image_stream).convert("RGB")
            logger.debug(f"Image size: {image.size}, mode: {image.mode}")
            
            # Depth Estimation and Mask Generation
            logger.debug("Starting depth estimation")
            depth_map = estimate_depth(image)
            logger.debug(f"Depth map shape: {depth_map.shape}, min: {depth_map.min()}, max: {depth_map.max()}")
            
            logger.debug("Creating binary mask")
            mask = create_mask(image)
            logger.debug(f"Mask shape: {mask.shape}, unique values: {np.unique(mask)}")
            
            logger.debug("Estimating volume from depth map")
            # Use predicted food type for better volume estimation
            food_type = predicted_food.split('_')[0]  # Extract base food type
            
            # Set reference volume based on food type
            reference_volumes = {
                "default": 240.0,
                "rice": 200.0,
                "bread": 150.0,
                "soup": 300.0,
                "curry": 250.0,
                "salad": 180.0,
                "fruit": 200.0,
                "vegetables": 180.0,
                "meat": 250.0,
                "fish": 200.0,
                "dessert": 200.0,
                "beverage": 300.0
            }
            reference_volume = reference_volumes.get(food_type, reference_volumes["default"])
            
            volume_ml = estimate_volume_from_depth(depth_map, mask, reference_volume)
            logger.debug(f"Estimated volume in ml: {volume_ml}")
            
            volume_grams = volume_ml  # assuming 1g/ml for food density
            logger.debug(f"Converted volume to grams: {volume_grams}")
            
            # Generate masked image
            logger.debug("Generating masked image")
            masked_image = generate_masked_image(image, mask)
            logger.debug(f"Masked image size: {masked_image.size}, mode: {masked_image.mode}")
            
            # Convert masked image to base64
            logger.debug("Converting masked image to base64")
            masked_buffer = BytesIO()
            masked_image.save(masked_buffer, format="PNG")
            masked_image_base64 = base64.b64encode(masked_buffer.getvalue()).decode("utf-8")
            logger.debug("Successfully converted masked image to base64")
            
            # Adjust nutrition based on volume
            if nutrition:
                logger.debug("Adjusting nutrition values based on volume")
                # Convert volume from ml to grams (assuming 1g/ml density)
                volume_grams = volume_ml
                # Calculate scale factor based on the difference from 150g (standard serving)
                scale_factor = volume_grams / 150.0
                logger.debug(f"Scale factor for nutrition adjustment: {scale_factor}")
                
                adjusted_nutrition = {
                    "food_product": getattr(nutrition, 'food_product', 'Unknown'),
                    "amount": f"{volume_grams:.1f}g",
                    "energy": round(getattr(nutrition, 'energy', 0) * scale_factor, 1),
                    "carbohydrate": round(getattr(nutrition, 'carbohydrate', 0) * scale_factor, 1),
                    "protein": round(getattr(nutrition, 'protein', 0) * scale_factor, 1),
                    "total_fat": round(getattr(nutrition, 'total_fat', 0) * scale_factor, 1),
                    "sodium": round(getattr(nutrition, 'sodium', 0) * scale_factor, 1),
                    "iron": round(getattr(nutrition, 'iron', 0) * scale_factor, 1)
                }
                logger.debug(f"Adjusted nutrition values: {adjusted_nutrition}")
            else:
                logger.warning("No nutrition data available for adjustment")
                adjusted_nutrition = None
                
        except Exception as e:
            logger.error(f"Error in volume calculation: {str(e)}", exc_info=True)
            logger.error("Stack trace:", exc_info=True)
            adjusted_nutrition = None
            masked_image_base64 = None
        
        # Prepare response
        response = {
            "predicted_food": predicted_food,
            "confidence": confidence,
            "nutrition": adjusted_nutrition,
            "volume_estimation": volume_grams if 'volume_grams' in locals() else None,
            "masked_image": f"data:image/png;base64,{masked_image_base64}" if masked_image_base64 else None
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error in predict_food_from_image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
        except Exception as e:
            logger.error(f"Error deleting temporary file: {str(e)}")

@router.get("/food-classes")
async def get_food_classes():
    """
    Endpoint to get all available food classes that the model can predict
    """
    logger.info("Returning food classes")
    return {"food_classes": CLASS_NAMES}

@router.get("/check-db")
async def check_database(db: Session = Depends(get_db)):
    """
    Endpoint to check the database connection and list food items
    """
    logger.info("Checking database connection")
    
    # Check database connection
    connection_ok = check_db_connection(db)
    
    if connection_ok:
        # Check if the database has been properly initialized with food data
        food_count = db.query(Food).count()
        if food_count == 0:
            logger.warning("Database is connected but has no food data. It may not be properly initialized.")
            return {
                "status": "warning", 
                "message": "Database connection successful but no food data found",
                "food_count": 0,
                "database_url": SQLALCHEMY_DATABASE_URL
            }
        
        # Get a sample of food items
        sample_foods = db.query(Food).limit(5).all()
        sample_food_names = [food.food_product for food in sample_foods]
        
        return {
            "status": "success", 
            "message": "Database connection successful",
            "food_count": food_count,
            "sample_foods": sample_food_names,
            "database_url": SQLALCHEMY_DATABASE_URL
        }
    else:
        return {
            "status": "error", 
            "message": "Database connection failed",
            "database_url": SQLALCHEMY_DATABASE_URL
        }

@router.get("/init-db")
async def initialize_database(db: Session = Depends(get_db)):
    """
    Endpoint to initialize the database with food data if it's empty
    """
    logger.info("Checking if database needs initialization")
    
    # Check if the database has food data
    food_count = db.query(Food).count()
    if food_count > 0:
        logger.info(f"Database already has {food_count} food items")
        return {
            "status": "success", 
            "message": "Database already initialized", 
            "food_count": food_count,
            "database_url": SQLALCHEMY_DATABASE_URL
        }
    
    # If the database is empty, try to initialize it
    logger.info("Database is empty, attempting to initialize it")
    
    try:
        # Import the function to load CSV data into the database
        from backend.db.dbcreateandinsert import load_csv_to_db
        
        # Get the path to the CSV file
        csv_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Sheet.csv")
        
        if not os.path.exists(csv_file):
            logger.error(f"CSV file not found at {csv_file}")
            return {
                "status": "error", 
                "message": f"CSV file not found at {csv_file}",
                "database_url": SQLALCHEMY_DATABASE_URL
            }
        
        # Load the CSV data into the database
        load_csv_to_db(csv_file)
        
        # Check if the database was successfully initialized
        food_count = db.query(Food).count()
        if food_count > 0:
            logger.info(f"Database initialized with {food_count} food items")
            return {
                "status": "success", 
                "message": f"Database initialized with {food_count} food items", 
                "food_count": food_count,
                "database_url": SQLALCHEMY_DATABASE_URL
            }
        else:
            logger.error("Failed to initialize database")
            return {
                "status": "error", 
                "message": "Failed to initialize database",
                "database_url": SQLALCHEMY_DATABASE_URL
            }
    
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        return {
            "status": "error", 
            "message": f"Error initializing database: {str(e)}",
            "database_url": SQLALCHEMY_DATABASE_URL
        }

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.depth_estimation import estimate_depth, create_mask, estimate_volume_from_depth, generate_masked_image
import base64
from io import BytesIO
