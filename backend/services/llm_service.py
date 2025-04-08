import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, model_id: str = "HuggingFaceH4/zephyr-7b-beta"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading model {model_id} on {self.device}")
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            torch_dtype=torch.float16, 
            device_map="auto"
        )
        logger.info(f"Model loaded successfully")
    
    def generate_food_recommendation(
        self,
        user_profile: Dict[str, Any],
        food_data: Dict[str, Any],
        context: Optional[str] = None,
        max_tokens: int = 512
    ) -> str:
        """
        Generate food recommendations based on user profile and food data.
        
        Args:
            user_profile: User profile information
            food_data: Food nutritional data
            context: Additional context for the recommendation
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated recommendation text
        """
        prompt = self._create_guidance_prompt(user_profile, food_data, context)
        
        logger.info(f"Generating recommendation with {len(prompt)} chars prompt")
        
        # Generate text
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=max_tokens,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        # Decode and return the generated text
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the response part (removing the prompt)
        response = generated_text[len(prompt):].strip()
        
        return response
    
    def _create_guidance_prompt(
        self, 
        user_profile: Dict[str, Any],
        food_data: Dict[str, Any],
        context: Optional[str] = None
    ) -> str:
        """
        Create a guidance prompt for the LLM to generate food recommendations.
        
        Args:
            user_profile: User profile information
            food_data: Food nutritional data
            context: Additional context for the recommendation
            
        Returns:
            Formatted prompt string
        """
        # Extract user information
        name = user_profile.get("name", "User")
        age = user_profile.get("age", "Unknown")
        weight = user_profile.get("weight", "Unknown")
        height = user_profile.get("height", "Unknown")
        health_issues = user_profile.get("health_issues", "None")
        allergies = user_profile.get("allergies", "None")
        physical_activity = user_profile.get("physical_activity_level", "Unknown")
        weight_goal = user_profile.get("weight_goal", "maintain")
        
        # Calculate BMI if height and weight are available
        bmi = "Unknown"
        if isinstance(height, (int, float)) and isinstance(weight, (int, float)) and height > 0:
            bmi = round(weight / ((height / 100) ** 2), 1)
        
        # Format food data
        food_details = ""
        for food in food_data:
            food_name = food.get("name", "Unknown food")
            calories = food.get("calories", "Unknown")
            protein = food.get("protein", "Unknown")
            carbs = food.get("carbs", "Unknown")
            fat = food.get("fat", "Unknown")
            
            food_details += f"- {food_name}: {calories} calories, {protein}g protein, {carbs}g carbs, {fat}g fat\\n"
        
        # Build the main prompt with all information
        prompt = f"""You are a nutrition expert and personalized food recommender. Your task is to provide specific, tailored food recommendations based on user health data and food nutritional information.

USER PROFILE:
Name: {name}
Age: {age}
Weight: {weight} kg
Height: {height} cm
BMI: {bmi}
Health Issues: {health_issues}
Allergies: {allergies}
Physical Activity Level: {physical_activity}
Weight Goal: {weight_goal}

AVAILABLE FOOD INFORMATION:
{food_details}

CONTEXT:
{context or "Provide general nutrition advice based on the user's profile and the available food options."}

TASK:
1. Analyze the nutritional content of the foods in relation to the user's profile.
2. Consider any health issues, allergies, or dietary restrictions.
3. Make personalized recommendations about which foods would be beneficial for this user.
4. Explain WHY these foods are recommended based on their nutritional value and the user's health needs.
5. If appropriate, suggest meal combinations or preparation methods.
6. Provide specific portion size recommendations based on the user's needs.

Your recommendation should be detailed, scientifically accurate, and tailored specifically to this user's needs. Use a friendly, supportive tone.

RECOMMENDATION:
"""
        
        return prompt

# Singleton instance
_llm_service = None

def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        model_id = os.getenv("LLM_MODEL_ID", "HuggingFaceH4/zephyr-7b-beta")
        _llm_service = LLMService(model_id=model_id)
    return _llm_service 