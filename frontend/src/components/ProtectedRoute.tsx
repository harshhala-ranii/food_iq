import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  redirectTo = '/login'
}) => {
  const { isLoggedIn, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    // While checking auth status, show a loading state
    return <div className="loading">Loading...</div>;
  }

  if (!isLoggedIn) {
    // If not logged in, redirect to login page with the intended destination
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // If logged in, render the protected component
  return <>{children}</>;
};

export default ProtectedRoute; 