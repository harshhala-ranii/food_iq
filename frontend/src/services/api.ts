import axios from 'axios';
import { API_CONFIG } from '../config';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Food image prediction API
export const predictFood = async (imageFile: File) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  try {
    const token = localStorage.getItem('token');
    const response = await apiClient.post(API_CONFIG.ENDPOINTS.PREDICT_FOOD, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error predicting food:', error);
    throw error;
  }
};

// Get available food classes
export const getFoodClasses = async () => {
  try {
    const response = await apiClient.get(API_CONFIG.ENDPOINTS.FOOD_CLASSES);
    return response.data.food_classes;
  } catch (error) {
    console.error('Error fetching food classes:', error);
    throw error;
  }
};

export interface NutritionResponse {
  nutrition: {
    food_product: string;
    amount: string;
    energy: number;
    carbohydrate: number;
    protein: number;
    total_fat: number;
    sodium: number;
    iron: number;
  };
  recommendations: {
    is_safe: boolean;
    warnings: string[];
    suggestions: string[];
    approval_message: string | null;
  };
}

// Get nutrition information by food name
export const getNutritionByFoodName = async (foodName: string): Promise<NutritionResponse> => {
  try {
    const token = localStorage.getItem('token');
    const response = await apiClient.get(`${API_CONFIG.ENDPOINTS.NUTRITION}/${encodeURIComponent(foodName)}`, {
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nutrition by food name:', error);
    throw error;
  }
};

export default {
  predictFood,
  getFoodClasses,
  getNutritionByFoodName,
}; 