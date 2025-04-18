// Configuration settings for the application

// API configuration
export const API_CONFIG = {
  // Base URL for API requests - empty string means use relative paths
  BASE_URL: import.meta.env.VITE_API_BASE_URL || '',
  
  // Endpoints
  ENDPOINTS: {
    PREDICT_FOOD: '/api/image/predict',
    FOOD_CLASSES: '/api/image/food-classes',
    NUTRITION: '/api/food/summary',
    CHAT: '/api/chat/message',
    AUTH: {
      LOGIN: '/api/auth/token',
      REGISTER: '/api/auth/register',
      REGISTER_WITH_PROFILE: '/api/auth/register-with-profile',
      CURRENT_USER: '/api/auth/users/me',
      USER_PROFILE: '/api/auth/users/me/profile',
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