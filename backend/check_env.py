import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print all environment variables
print("Environment variables:")
for key, value in os.environ.items():
    if key == "OPENAI_API_KEY":
        print(f"{key}: {value[:10]}...")
    else:
        print(f"{key}: {value}")

# Check if OpenAI API key is set
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"\nOpenAI API key is set: {api_key[:10]}...")
else:
    print("\nOpenAI API key is NOT set!") 