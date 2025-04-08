import React, { useState, useEffect } from 'react';
import { getFoodClasses } from '../services/api';
import './FoodClasses.css';

interface FoodClassesProps {
  title?: string;
}

const FoodClasses: React.FC<FoodClassesProps> = ({ title = 'Available Food Classes' }) => {
  const [foodClasses, setFoodClasses] = useState<string[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchFoodClasses = async () => {
      try {
        setLoading(true);
        const classes = await getFoodClasses();
        setFoodClasses(classes);
        setError(null);
      } catch (err) {
        console.error('Error fetching food classes:', err);
        setError('Failed to load available food classes');
      } finally {
        setLoading(false);
      }
    };

    fetchFoodClasses();
  }, []);

  if (loading) {
    return (
      <div className="food-classes loading">
        <h2>{title}</h2>
        <div className="loading-spinner">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="food-classes error">
        <h2>{title}</h2>
        <div className="error-message">{error}</div>
      </div>
    );
  }

  return (
    <div className="food-classes">
      <h2>{title}</h2>
      <div className="food-classes-grid">
        {foodClasses.map((foodClass, index) => (
          <div key={index} className="food-class-item">
            {foodClass}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FoodClasses; 