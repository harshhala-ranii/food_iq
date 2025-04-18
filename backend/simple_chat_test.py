import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def test_chat():
    """Test OpenAI chat API directly"""
    logger.info("Testing OpenAI chat API...")
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return False

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Create a test message
        messages = [
            {"role": "system", "content": "You are a knowledgeable Indian nutritionist and healthcare assistant, specializing in traditional Indian dietary practices and modern nutritional science."},
            {"role": "user", "content": "Can you give me some advice about healthy Indian breakfast options?"}
        ]
        
        # Make API call
        logger.info("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # Print response
        logger.info("OpenAI API test successful!")
        logger.info("\nResponse:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)
        
        return True
        
    except Exception as e:
        logger.error(f"OpenAI API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_chat()
    logger.info(f"\nTest {'succeeded' if success else 'failed'}") 