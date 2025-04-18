from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OpenAI API key not found in environment variables")
    client = None
else:
    logger.info("OpenAI API key found, initializing client")
    client = OpenAI(api_key=api_key)
    logger.info("OpenAI client initialized")

class ChatRequest(BaseModel):
    message: str

@router.post("/chat/message")
async def chat_with_healthbot(data: ChatRequest):
    """Simple chat endpoint that directly uses OpenAI API"""
    try:
        if not client:
            raise HTTPException(status_code=500, detail="OpenAI client not initialized. Please check your API key configuration.")
            
        logger.info(f"Received chat request: {data.message}")
        
        # Create messages for the API call
        messages = [
            {"role": "system", "content": "You are a knowledgeable Indian nutritionist and healthcare assistant, specializing in traditional Indian dietary practices and modern nutritional science."},
            {"role": "user", "content": data.message}
        ]
        
        logger.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        logger.info("Received response from OpenAI API")
        return {"response": response.choices[0].message.content}
            
    except Exception as e:
        logger.error(f"Error in chat_with_healthbot: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}") 