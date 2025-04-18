import os
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables")
    exit(1)

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Send a test message
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the capital of India?"}
        ],
        temperature=0.7,
        max_tokens=100
    )

    print("OpenAI API response:")
    print(response.choices[0].message.content)

except Exception as e:
    print(f"OpenAI API request failed: {e}")
