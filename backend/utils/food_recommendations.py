from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FoodRecommendation:
    def __init__(self, food_name: str, user_conditions: List[str] = None, user_goals: Optional[List[str]] = None):
        self.food_name = food_name
        # Clean up conditions - remove any JSON string formatting
        self.user_conditions = []
        if user_conditions:
            for condition in user_conditions:
                # Remove any JSON string formatting
                clean_condition = condition.strip('[]"\'')
                if clean_condition and clean_condition != "none":
                    self.user_conditions.append(clean_condition)
        
        # Clean up goals
        self.user_goals = []
        if user_goals:
            for goal in user_goals:
                clean_goal = goal.strip('[]"\'')
                if clean_goal:
                    self.user_goals.append(clean_goal)
        
        logger.info(f"Initializing FoodRecommendation for {food_name}")
        logger.info(f"User conditions: {self.user_conditions}")
        logger.info(f"User goals: {self.user_goals}")
        self.warnings = []
        self.alternatives = []
        self.approval_message = None

    def evaluate(self) -> Dict:
        """
        Evaluate the food based on user conditions and goals
        Returns a dictionary with warnings, alternatives, and approval message
        """
        logger.info(f"Evaluating food {self.food_name} for conditions: {self.user_conditions}")
        
        # Log the evaluation methods being called
        logger.debug(f"Evaluating desserts for {self.food_name}")
        self._evaluate_desserts()
        logger.debug(f"Evaluating fried foods for {self.food_name}")
        self._evaluate_fried_foods()
        logger.debug(f"Evaluating rich dishes for {self.food_name}")
        self._evaluate_rich_dishes()
        logger.debug(f"Evaluating south Indian dishes for {self.food_name}")
        self._evaluate_south_indian()
        logger.debug(f"Evaluating dhokla for {self.food_name}")
        self._evaluate_dhokla()
        logger.debug(f"Evaluating samosa for {self.food_name}")
        self._evaluate_samosa()
        logger.debug(f"Evaluating pav bhaji for {self.food_name}")
        self._evaluate_pav_bhaji()
        logger.debug(f"Evaluating paneer dishes for {self.food_name}")
        self._evaluate_paneer_dishes()
        logger.debug(f"Evaluating dal dishes for {self.food_name}")
        self._evaluate_dal_dishes()
        logger.debug(f"Evaluating chicken dishes for {self.food_name}")
        self._evaluate_chicken_dishes()
        logger.debug(f"Evaluating aloo matar for {self.food_name}")
        self._evaluate_aloo_matar()

        recommendations = {
            "is_safe": True,
            "warnings": self.warnings,
            "suggestions": self.alternatives,
            "approval_message": self.approval_message
        }
        logger.info(f"Evaluation complete. Results: {recommendations}")
        return recommendations

    def _evaluate_desserts(self):
        if self.food_name in ["gulab_jamun", "jalebi"]:
            logger.debug(f"Evaluating dessert {self.food_name}")
            if "diabetes" in self.user_conditions:
                logger.info(f"Adding diabetes warning for {self.food_name}")
                self.warnings.append("This dessert is high in sugar, which may not be suitable for diabetes.")
                self.alternatives.append("Try a low-sugar fruit salad or a sugar-free dessert option.")
            elif "obesity" in self.user_conditions:
                logger.info(f"Adding obesity warning for {self.food_name}")
                self.warnings.append("This sweet item may be high in calories and sugar. Consider healthier alternatives.")
                self.alternatives.append("Try a small portion of dark chocolate or Greek yogurt with berries.")
            else:
                logger.info(f"Adding general dessert warning for {self.food_name}")
                self.warnings.append("Jalebi is deep-fried and soaked in sugar syrup; consume in very small quantities if at all.")
                self.alternatives.append("Cut back on frequency and portion size, or look for baked, sugar-free sweets.")

    def _evaluate_fried_foods(self):
        if self.food_name in ["chole_bhature", "samosa"]:
            logger.debug(f"Evaluating fried food {self.food_name}")
            if any(condition in self.user_conditions for condition in ["obesity", "cholesterol", "high-bp"]):
                logger.info(f"Adding health condition warning for fried food {self.food_name}")
                self.warnings.append("This is deep-fried and high in saturated fats.")
                self.alternatives.append("Consider a baked version or use heart-healthy oils like olive oil for cooking.")

    def _evaluate_rich_dishes(self):
        if self.food_name in ["butter_chicken", "biryani"]:
            logger.debug(f"Evaluating rich dish {self.food_name}")
            self.alternatives.append("This dish may be rich in carbs and heavy. Try healthier options like grilled chicken or a chicken salad.")

    def _evaluate_south_indian(self):
        if self.food_name in ["idli", "masala_dosa"]:
            logger.debug(f"Evaluating south Indian dish {self.food_name}")
            if "diabetes" in self.user_conditions:
                logger.info(f"Adding diabetes warning for south Indian dish {self.food_name}")
                self.warnings.append("South Indian dishes like dosa and idli can have a high glycemic index.")
                self.alternatives.append("Consider ragi dosa or oats idli, which have a lower glycemic index.")
            elif "obesity" in self.user_conditions:
                logger.info(f"Adding obesity warning for south Indian dish {self.food_name}")
                self.warnings.append("Watch portion sizes and avoid excessive oil or ghee.")
                self.alternatives.append("Try steamed food over fried, and skip chutneys with too much coconut or oil.")
            elif "gluten intolerance" in self.user_conditions:
                logger.info(f"Adding approval message for gluten intolerance with {self.food_name}")
                self.approval_message = "Idli and dosa are naturally gluten-free and suitable for your condition."
            else:
                logger.info(f"Adding general approval message for {self.food_name}")
                self.approval_message = "Idli and dosa are generally healthy choices when cooked with minimal oil."

    def _evaluate_dhokla(self):
        if self.food_name == "dhokla":
            logger.debug(f"Evaluating dhokla")
            if "diabetes" in self.user_conditions:
                logger.info(f"Adding approval message for diabetes with dhokla")
                self.approval_message = "Dhokla is steamed and low in fat. It's a good choice when made with minimal sugar. Pair it with mint chutney instead of sweet chutney."
            else:
                logger.info(f"Adding general approval message for dhokla")
                self.approval_message = "Dhokla is a healthy snack. Pair it with mint chutney instead of sweet chutney for fewer calories."

    def _evaluate_samosa(self):
        if self.food_name == "samosa":
            logger.debug(f"Evaluating samosa")
            if any(condition in self.user_conditions for condition in ["obesity", "cholesterol", "high-bp"]):
                logger.info(f"Adding health condition warning for samosa")
                self.warnings.append("Samosas are deep-fried and high in saturated fat.")
                self.alternatives.append("Try a baked samosa or fill it with vegetables and use whole wheat dough.")
            else:
                logger.info(f"Adding general warning for samosa")
                self.warnings.append("Limit intake of fried foods like samosas for better heart health.")

    def _evaluate_pav_bhaji(self):
        if self.food_name == "pav_bhaji":
            logger.debug(f"Evaluating pav bhaji")
            if any(condition in self.user_conditions for condition in ["cholesterol", "diabetes", "obesity"]):
                logger.info(f"Adding health condition warning for pav bhaji")
                self.warnings.append("Pav Bhaji often contains a lot of butter and refined carbs.")
                self.alternatives.append("Opt for whole wheat pav, reduce butter, or try the bhaji with millet rotis.")
            else:
                logger.info(f"Adding general warning for pav bhaji")
                self.warnings.append("Use minimal butter and go for whole grain pav to make it a healthier meal.")

    def _evaluate_paneer_dishes(self):
        if self.food_name == "paneer_butter_masala":
            logger.debug(f"Evaluating paneer butter masala")
            if any(condition in self.user_conditions for condition in ["cholesterol", "diabetes", "obesity", "high-bp"]):
                logger.info(f"Adding health condition warning for paneer butter masala")
                self.warnings.append("Paneer Butter Masala is rich in cream and butter, which may not suit your condition.")
                self.alternatives.append("Try grilled paneer, palak paneer with less oil, or tofu curry made with low-fat ingredients.")
            else:
                logger.info(f"Adding general warning for paneer butter masala")
                self.warnings.append("Enjoy in moderation. Consider using less butter and cream for a lighter version.")

        elif self.food_name == "kadai_paneer":
            logger.debug(f"Evaluating kadai paneer")
            if "acidity" in self.user_conditions or "high-bp" in self.user_conditions:
                logger.info(f"Adding acidity/high-bp warning for kadai paneer")
                self.warnings.append("Kadai Paneer can be spicy and oily, which may trigger acidity or raise blood pressure.")
                self.alternatives.append("Try paneer sautée with minimal spices or combine with bell peppers and herbs instead of heavy masala.")
            elif "obesity" in self.user_goals:
                logger.info(f"Adding obesity suggestion for kadai paneer")
                self.alternatives.append("Use less oil, pair with whole grains, or swap paneer with tofu for a lighter option.")
            else:
                logger.info(f"Adding approval message for kadai paneer")
                self.approval_message = "Kadai Paneer is a decent option when made with minimal oil and fresh spices."

    def _evaluate_dal_dishes(self):
        if self.food_name == "dal_makhani":
            logger.debug(f"Evaluating dal makhani")
            if any(condition in self.user_conditions for condition in ["cholesterol", "obesity", "diabetes", "high-bp"]):
                logger.info(f"Adding health condition warning for dal makhani")
                self.warnings.append("Dal Makhani is rich in butter and cream, which can be heavy for your condition.")
                self.alternatives.append("Opt for plain whole dal like moong or masoor, or make dal makhani with less butter and use low-fat milk or curd instead of cream.")
            else:
                logger.info(f"Adding approval message for dal makhani")
                self.approval_message = "Dal Makhani can be enjoyed in moderation. Try making it with less ghee and cream for a lighter meal."

    def _evaluate_chicken_dishes(self):
        if self.food_name == "chicken_tikka":
            logger.debug(f"Evaluating chicken tikka")
            if "acidity" in self.user_conditions:
                logger.info(f"Adding acidity warning for chicken tikka")
                self.warnings.append("Chicken Tikka can be spicy and might trigger acidity.")
                self.alternatives.append("Go for lightly spiced grilled chicken or chicken stew.")
            elif "weight loss" in self.user_goals or "high protein" in self.user_goals:
                logger.info(f"Adding approval message for weight loss/high protein with chicken tikka")
                self.approval_message = "Chicken Tikka is high in protein and low in carbs — a great option for your goals!"
            else:
                logger.info(f"Adding general approval message for chicken tikka")
                self.approval_message = "Grilled and flavorful, chicken tikka is a good lean protein source when not overly spicy."

    def _evaluate_aloo_matar(self):
        if self.food_name == "aloo_matar":
            logger.debug(f"Evaluating aloo matar")
            if "diabetes" in self.user_conditions:
                logger.info(f"Adding diabetes warning for aloo matar")
                self.warnings.append("Aloo Matar contains potatoes which have a high glycemic index and may affect blood sugar levels.")
                self.alternatives.append("Consider replacing potatoes with low glycemic vegetables like cauliflower or green beans.")
            elif "obesity" in self.user_conditions:
                logger.info(f"Adding obesity warning for aloo matar")
                self.warnings.append("Aloo Matar can be high in calories due to potatoes and possible oil content.")
                self.alternatives.append("Try making it with less oil, or replace some potatoes with more peas for a lower calorie option.")
            elif "high-bp" in self.user_conditions:
                logger.info(f"Adding high blood pressure warning for aloo matar")
                self.warnings.append("Aloo Matar may contain significant salt content which can affect blood pressure.")
                self.alternatives.append("Prepare with minimal salt and use herbs and spices for flavor instead.")
            elif "gluten intolerance" in self.user_conditions:
                logger.info(f"Adding approval message for gluten intolerance with aloo matar")
                self.approval_message = "Aloo Matar is naturally gluten-free and suitable for your condition."
            else:
                logger.info(f"Adding general approval message for aloo matar")
                self.approval_message = "Aloo Matar is a balanced dish with protein from peas and carbohydrates from potatoes. Enjoy in moderation as part of a balanced meal." 