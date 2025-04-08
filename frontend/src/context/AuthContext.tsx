import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { 
  login as apiLogin, 
  register as apiRegister, 
  registerWithProfile as apiRegisterWithProfile,
  logout as apiLogout,
  isLoggedIn as apiIsLoggedIn,
  getCurrentUser,
  getUserProfile,
  LoginCredentials,
  RegisterData,
  RegisterWithProfileData,
  UserProfile
} from '../services/auth';

interface User {
  id: number;
  email: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  error: string | null;
  isLoggedIn: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  registerWithProfile: (data: RegisterWithProfileData) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(apiIsLoggedIn());

  // Check if user is already logged in on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      if (apiIsLoggedIn()) {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
          
          try {
            const profileData = await getUserProfile();
            setProfile(profileData);
          } catch (profileError) {
            console.log('No profile found for user');
          }
          
          setIsLoggedIn(true);
        } catch (error) {
          console.error('Error verifying auth status:', error);
          apiLogout();
          setIsLoggedIn(false);
        }
      }
      setLoading(false);
    };

    checkAuthStatus();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    setLoading(true);
    setError(null);
    try {
      await apiLogin(credentials);
      const userData = await getCurrentUser();
      setUser(userData);
      
      try {
        const profileData = await getUserProfile();
        setProfile(profileData);
      } catch (profileError) {
        console.log('No profile found for user');
      }
      
      setIsLoggedIn(true);
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Login failed. Please check your credentials.');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const register = async (data: RegisterData) => {
    setLoading(true);
    setError(null);
    try {
      await apiRegister(data);
      // After registration, log the user in
      await login({ username: data.email, password: data.password });
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Registration failed. Please try again.');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const registerWithProfile = async (data: RegisterWithProfileData) => {
    setLoading(true);
    setError(null);
    try {
      await apiRegisterWithProfile(data);
      // After registration, log the user in
      await login({ username: data.email, password: data.password });
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Registration failed. Please try again.');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    apiLogout();
    setUser(null);
    setProfile(null);
    setIsLoggedIn(false);
  };

  const clearError = () => {
    setError(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        profile,
        loading,
        error,
        isLoggedIn,
        login,
        register,
        registerWithProfile,
        logout,
        clearError
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 