import axios from 'axios';
import { API_CONFIG } from '../config';

// Create axios instance with default config
const authClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add interceptor to include auth token in requests
authClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Types for authentication
export interface LoginCredentials {
  username: string; // Actually the email
  password: string;
}

export interface UserProfile {
  id: number;
  user_id: number;
  name: string;
  age: number;
  number: string;
  weight: number;
  height: number;
  health_issues?: string;
  allergies?: string;
  medications?: string;
  blood_type?: string;
  smoking_status?: string;
  alcohol_consumption?: string;
  physical_activity_level?: string;
}

export interface ProfileData {
  name: string;
  age: number;
  number: string;
  weight: number;
  height: number;
  health_issues?: string;
  allergies?: string;
  medications?: string;
  blood_type?: string;
  smoking_status?: string;
  alcohol_consumption?: string;
  physical_activity_level?: string;
}

export interface RegisterData {
  email: string;
  password: string;
}

export interface RegisterWithProfileData {
  email: string;
  password: string;
  profile: ProfileData;
}

// Login user
export const login = async (credentials: LoginCredentials) => {
  try {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await axios.post(`${API_CONFIG.BASE_URL}/auth/token`, formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    
    // Store token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      return response.data;
    }
    
    throw new Error('Login failed: No token received');
  } catch (error) {
    console.error('Error logging in:', error);
    throw error;
  }
};

// Register user
export const register = async (userData: RegisterData) => {
  try {
    const response = await authClient.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user:', error);
    throw error;
  }
};

// Register user with profile
export const registerWithProfile = async (userData: RegisterWithProfileData) => {
  try {
    const response = await authClient.post('/auth/register-with-profile', userData);
    return response.data;
  } catch (error) {
    console.error('Error registering user with profile:', error);
    throw error;
  }
};

// Get current user profile
export const getUserProfile = async () => {
  try {
    const response = await authClient.get('/auth/users/me/profile');
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

// Create user profile
export const createUserProfile = async (profileData: ProfileData) => {
  try {
    const response = await authClient.post('/auth/users/me/profile', profileData);
    return response.data;
  } catch (error) {
    console.error('Error creating user profile:', error);
    throw error;
  }
};

// Update user profile
export const updateUserProfile = async (profileData: Partial<ProfileData>) => {
  try {
    const response = await authClient.put('/auth/users/me/profile', profileData);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
};

// Get current user info
export const getCurrentUser = async () => {
  try {
    const response = await authClient.get('/auth/users/me');
    return response.data;
  } catch (error) {
    console.error('Error fetching current user:', error);
    throw error;
  }
};

// Logout user (client-side only)
export const logout = () => {
  localStorage.removeItem('token');
};

// Check if user is logged in
export const isLoggedIn = () => {
  return localStorage.getItem('token') !== null;
};

export default {
  login,
  register,
  registerWithProfile,
  getUserProfile,
  createUserProfile,
  updateUserProfile,
  getCurrentUser,
  logout,
  isLoggedIn,
}; 