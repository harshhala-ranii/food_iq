from fastapi import HTTPException
import os
import logging
from openai import OpenAI
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodRecommendationLLM:
    def __init__(self):
        """Initialize the OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized")

    def _create_recommendation_prompt(
        self,
        food_name: str,
        food_nutrition: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None
    ) -> str:
        """
        Create a prompt for the LLM to generate food recommendations.
        
        Args:
            food_name: Name of the food item
            food_nutrition: Nutritional information of the food
            user_profile: User's health profile and preferences
            context: Additional context for the recommendation
            
        Returns:
            Formatted prompt string
        """
        # Format food nutritional information
        nutrition_info = f"""
Food: {food_name}
Nutritional Information (per {food_nutrition.get('amount', '100g')}):
- Energy: {food_nutrition.get('energy', 'N/A')} kcal
- Carbohydrates: {food_nutrition.get('carbohydrate', 'N/A')}g
- Protein: {food_nutrition.get('protein', 'N/A')}g
- Total Fat: {food_nutrition.get('total_fat', 'N/A')}g
- Sodium: {food_nutrition.get('sodium', 'N/A')}mg
- Iron: {food_nutrition.get('iron', 'N/A')}mg
"""

        # Format user profile information if available
        user_info = ""
        if user_profile:
            user_info = f"""
User Profile:
- Age: {user_profile.get('age', 'N/A')}
- Weight: {user_profile.get('weight', 'N/A')}kg
- Height: {user_profile.get('height', 'N/A')}cm
- Health Issues: {user_profile.get('health_issues', 'None')}
- Allergies: {user_profile.get('allergies', 'None')}
- Physical Activity: {user_profile.get('physical_activity_level', 'N/A')}
- Weight Goal: {user_profile.get('weight_goal', 'maintain')}
- Dietary Preferences: {user_profile.get('dietary_preferences', 'None')}
"""

        # Create the prompt
        prompt = f"""You are a knowledgeable Indian nutritionist and healthcare assistant. Based on the following information, provide a detailed food recommendation:

{nutrition_info}
{user_info}
{f'Additional Context: {context}' if context else ''}

Please provide a recommendation that includes:
1. Whether this food is suitable for the user's health conditions and goals
2. Any potential health concerns or warnings
3. Suggested portion sizes
4. Alternative food options if this food is not suitable
5. Tips for making this food healthier if applicable

Format your response as a JSON object with the following structure:
{{
    "is_safe": boolean,
    "warnings": [string],
    "suggestions": [string],
    "approval_message": string
}}
"""

        return prompt

    def get_recommendation(
        self,
        food_name: str,
        food_nutrition: Dict[str, Any],
        user_profile: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a food recommendation using the OpenAI API.
        
        Args:
            food_name: Name of the food item
            food_nutrition: Nutritional information of the food
            user_profile: User's health profile and preferences
            context: Additional context for the recommendation
            
        Returns:
            Dictionary containing the recommendation
        """
        try:
            # Create the prompt
            prompt = self._create_recommendation_prompt(
                food_name=food_name,
                food_nutrition=food_nutrition,
                user_profile=user_profile,
                context=context
            )
            
            logger.info(f"Generating recommendation for {food_name}")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable Indian nutritionist and healthcare assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract and parse the response
            recommendation_text = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                import json
                recommendation = json.loads(recommendation_text)
                logger.info("Successfully parsed recommendation JSON")
                return recommendation
            except json.JSONDecodeError:
                logger.warning("Failed to parse recommendation as JSON, returning raw text")
                return {
                    "is_safe": True,
                    "warnings": [],
                    "suggestions": [],
                    "approval_message": recommendation_text
                }
                
        except Exception as e:
            logger.error(f"Error generating recommendation: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate recommendation: {str(e)}"
            ) 