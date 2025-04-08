import React from 'react';
import './NutritionFacts.css';

interface NutritionInfo {
  food_product: string;
  amount: string;
  energy: string;
  carbohydrate: string;
  protein: string;
  total_fat: string;
  sodium: string;
  iron: string;
}

interface NutritionFactsProps {
  nutrition: NutritionInfo;
}

const NutritionFacts: React.FC<NutritionFactsProps> = ({ nutrition }) => {
  return (
    <div className="nutrition-facts">
      <div className="nutrition-facts-header">
        <h2>Nutrition Facts</h2>
        <p className="food-name">{nutrition.food_product}</p>
        <p className="serving-size">Serving Size: {nutrition.amount}</p>
      </div>
      
      <div className="nutrition-facts-divider thick"></div>
      
      <div className="nutrition-facts-calories">
        <span className="label">Calories</span>
        <span className="value">{nutrition.energy}</span>
      </div>
      
      <div className="nutrition-facts-divider"></div>
      
      <div className="nutrition-facts-item">
        <span className="label">Total Fat</span>
        <span className="value">{nutrition.total_fat}</span>
      </div>
      
      <div className="nutrition-facts-divider"></div>
      
      <div className="nutrition-facts-item">
        <span className="label">Sodium</span>
        <span className="value">{nutrition.sodium}</span>
      </div>
      
      <div className="nutrition-facts-divider"></div>
      
      <div className="nutrition-facts-item">
        <span className="label">Total Carbohydrate</span>
        <span className="value">{nutrition.carbohydrate}</span>
      </div>
      
      <div className="nutrition-facts-divider"></div>
      
      <div className="nutrition-facts-item">
        <span className="label">Protein</span>
        <span className="value">{nutrition.protein}</span>
      </div>
      
      <div className="nutrition-facts-divider"></div>
      
      <div className="nutrition-facts-item">
        <span className="label">Iron</span>
        <span className="value">{nutrition.iron}</span>
      </div>
      
      <div className="nutrition-facts-divider thick"></div>
      
      <div className="nutrition-facts-footer">
        <p>* Percent Daily Values are based on a 2,000 calorie diet.</p>
      </div>
    </div>
  );
};

export default NutritionFacts; 