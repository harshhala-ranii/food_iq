from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import routers
from endpoints.food_router import router as food_router
from endpoints.imageprocess import router as image_router

# Create FastAPI app
app = FastAPI(
    title="Food IQ API",
    description="API for retrieving nutritional information about food items and processing food images",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(food_router, prefix="/food", tags=["food"])
app.include_router(image_router, prefix="/image", tags=["image"])

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Food IQ API",
        "docs": "/docs",
        "endpoints": {
            "food": "/food/summary/{food_name}",
            "image": "/image/predict"
        }
    }

# Run the application directly if this file is executed
if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 