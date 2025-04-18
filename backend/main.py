from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import sys
from dotenv import load_dotenv
import uvicorn

# Add parent directory to path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import database and models
from models.database import engine, Base
from models.user import User, UserProfile, UserFoodLog, FoodRecommendation
from models.food import Food
from endpoints import auth_endpoint, imageprocess, user_endpoint, food_router, chatbot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Validate OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logger.error("OPENAI_API_KEY not found in environment variables")
else:
    logger.info("OpenAI API key is configured")

app = FastAPI(
    title="Food IQ API",
    description="API for Food IQ application providing personalized food recommendations",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000,http://localhost").split(",")
logger.info(f"Configuring CORS with allowed origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_endpoint.router)
app.include_router(user_endpoint.router)
app.include_router(imageprocess.router, prefix="/api/image", tags=["image"])
app.include_router(food_router.router, prefix="/api/food", tags=["food"])
app.include_router(chatbot.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Food IQ API",
        "docs": "/docs",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test-env")
async def test_env():
    """Test endpoint to verify environment variables"""
    return {
        "openai_api_key_exists": bool(os.getenv("OPENAI_API_KEY")),
        "openai_api_key_prefix": os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else None,
        "environment": os.getenv("ENVIRONMENT"),
        "all_env_vars": {k: v[:10] + "..." if k == "OPENAI_API_KEY" and v else v 
                        for k, v in os.environ.items() 
                        if not k.startswith("_")}
    }

# Direct LLM endpoint for testing (use with caution in production)
if os.getenv("ENABLE_DIRECT_LLM_ENDPOINT", "false").lower() == "true":
    from pydantic import BaseModel
    
    # Import LLM service
    from services.llm_service import get_llm_service
    
    class Prompt(BaseModel):
        prompt: str
        max_tokens: int = 256
    
    @app.post("/v1/completions")
    async def generate_text(prompt_data: Prompt):
        llm_service = get_llm_service()
        tokenizer = llm_service.tokenizer
        model = llm_service.model
        
        inputs = tokenizer(prompt_data.prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=prompt_data.max_tokens)
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"text": generated}

# Run the application directly if this file is executed
if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) 