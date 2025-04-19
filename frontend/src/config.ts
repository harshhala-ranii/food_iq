// Configuration settings for the application

// API configuration
export const API_CONFIG = {
  // Base URL for API requests - empty string means use relative paths
  BASE_URL: import.meta.env.VITE_API_BASE_URL || '',
  
  // Endpoints
  ENDPOINTS: {
    PREDICT_FOOD: '/image/predict',
    FOOD_CLASSES: '/image/food-classes',
    NUTRITION: '/food/summary',
    CHAT: '/chat/message',
    AUTH: {
      LOGIN: '/auth/token',
      REGISTER: '/auth/register',
      REGISTER_WITH_PROFILE: '/auth/register-with-profile',
      CURRENT_USER: '/auth/users/me',
      USER_PROFILE: '/auth/users/me/profile',
    }
  },
};

// Feature flags
export const FEATURES = {
  ENABLE_FOOD_CLASSES: true,
  ENABLE_NUTRITION_FACTS: true,
  ENABLE_AUTH: true,
  ENABLE_CHAT: true,
};

// Default settings
export const DEFAULTS = {
  IMAGE_SIZE: 224, // Size of images for prediction (in pixels)
};

export default {
  API_CONFIG,
  FEATURES,
  DEFAULTS,
}; 