import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';
import '../styles/Auth.css';

const Register: React.FC = () => {
  // User account info
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  // Profile info
  const [name, setName] = useState('');
  const [age, setAge] = useState('');
  const [number, setNumber] = useState('');
  const [weight, setWeight] = useState('');
  const [height, setHeight] = useState('');
  const [healthIssues, setHealthIssues] = useState('');
  const [allergies, setAllergies] = useState('');
  const [medications, setMedications] = useState('');
  const [bloodType, setBloodType] = useState('');
  const [smokingStatus, setSmokingStatus] = useState('');
  const [alcoholConsumption, setAlcoholConsumption] = useState('');
  const [physicalActivityLevel, setPhysicalActivityLevel] = useState('');
  
  // Form state
  const [passwordError, setPasswordError] = useState('');
  const [step, setStep] = useState(1); // 1 for account info, 2 for profile info
  
  const { registerWithProfile, error, clearError, loading } = useAuth();
  const navigate = useNavigate();

  const validatePasswordMatch = () => {
    if (password !== confirmPassword) {
      setPasswordError('Passwords do not match');
      return false;
    }
    
    if (password.length < 8) {
      setPasswordError('Password must be at least 8 characters long');
      return false;
    }
    
    setPasswordError('');
    return true;
  };

  const handleNextStep = (e: React.FormEvent) => {
    e.preventDefault();
    if (validatePasswordMatch()) {
      setStep(2);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    
    if (!validatePasswordMatch()) {
      return;
    }
    
    try {
      await registerWithProfile({
        email,
        password,
        profile: {
          name,
          age: parseInt(age),
          number,
          weight: parseFloat(weight),
          height: parseFloat(height),
          health_issues: healthIssues || undefined,
          allergies: allergies || undefined,
          medications: medications || undefined,
          blood_type: bloodType || undefined,
          smoking_status: smokingStatus || undefined,
          alcohol_consumption: alcoholConsumption || undefined,
          physical_activity_level: physicalActivityLevel || undefined,
        }
      });
      navigate('/profile');
    } catch (err) {
      // Error is handled in the auth context
    }
  };

  return (
    <>
      <Navbar />
      <div className="auth-container">
        <div className="auth-card">
          <h1>Create Account</h1>
          <p className="auth-description">Join Food IQ to track your nutrition and get personalized insights.</p>
          
          {error && <div className="auth-error">{error}</div>}
          
          {step === 1 ? (
            <form onSubmit={handleNextStep} className="auth-form">
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  autoComplete="email"
                  placeholder="Enter your email"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="new-password"
                  placeholder="Create a password (min. 8 characters)"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm Password</label>
                <input
                  id="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                  autoComplete="new-password"
                  placeholder="Confirm your password"
                />
                {passwordError && <div className="input-error">{passwordError}</div>}
              </div>
              
              <button 
                type="submit" 
                className="auth-button"
              >
                Next
              </button>
              
              <div className="auth-links">
                <p>Already have an account? <Link to="/login">Login</Link></p>
                <Link to="/" className="back-link">Back to Home</Link>
              </div>
            </form>
          ) : (
            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="name">Full Name</label>
                <input
                  id="name"
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                  placeholder="Enter your full name"
                />
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="age">Age</label>
                  <input
                    id="age"
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    required
                    placeholder="Years"
                    min="1"
                    max="120"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="number">Phone Number</label>
                  <input
                    id="number"
                    type="tel"
                    value={number}
                    onChange={(e) => setNumber(e.target.value)}
                    required
                    placeholder="Phone number"
                  />
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="weight">Weight (kg)</label>
                  <input
                    id="weight"
                    type="number"
                    value={weight}
                    onChange={(e) => setWeight(e.target.value)}
                    required
                    placeholder="Kilograms"
                    step="0.1"
                    min="1"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="height">Height (cm)</label>
                  <input
                    id="height"
                    type="number"
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                    required
                    placeholder="Centimeters"
                    step="0.1"
                    min="1"
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="healthIssues">Health Issues (Optional)</label>
                <textarea
                  id="healthIssues"
                  value={healthIssues}
                  onChange={(e) => setHealthIssues(e.target.value)}
                  placeholder="List any health issues"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="allergies">Allergies (Optional)</label>
                <textarea
                  id="allergies"
                  value={allergies}
                  onChange={(e) => setAllergies(e.target.value)}
                  placeholder="List any food allergies"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="medications">Medications (Optional)</label>
                <textarea
                  id="medications"
                  value={medications}
                  onChange={(e) => setMedications(e.target.value)}
                  placeholder="List any medications"
                />
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="bloodType">Blood Type (Optional)</label>
                  <select
                    id="bloodType"
                    value={bloodType}
                    onChange={(e) => setBloodType(e.target.value)}
                  >
                    <option value="">Select Blood Type</option>
                    <option value="A+">A+</option>
                    <option value="A-">A-</option>
                    <option value="B+">B+</option>
                    <option value="B-">B-</option>
                    <option value="AB+">AB+</option>
                    <option value="AB-">AB-</option>
                    <option value="O+">O+</option>
                    <option value="O-">O-</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="smokingStatus">Smoking Status (Optional)</label>
                  <select
                    id="smokingStatus"
                    value={smokingStatus}
                    onChange={(e) => setSmokingStatus(e.target.value)}
                  >
                    <option value="">Select Status</option>
                    <option value="Never">Never</option>
                    <option value="Former">Former</option>
                    <option value="Current">Current</option>
                  </select>
                </div>
              </div>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="alcoholConsumption">Alcohol Consumption (Optional)</label>
                  <select
                    id="alcoholConsumption"
                    value={alcoholConsumption}
                    onChange={(e) => setAlcoholConsumption(e.target.value)}
                  >
                    <option value="">Select Level</option>
                    <option value="None">None</option>
                    <option value="Occasional">Occasional</option>
                    <option value="Regular">Regular</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="physicalActivityLevel">Physical Activity (Optional)</label>
                  <select
                    id="physicalActivityLevel"
                    value={physicalActivityLevel}
                    onChange={(e) => setPhysicalActivityLevel(e.target.value)}
                  >
                    <option value="">Select Level</option>
                    <option value="Sedentary">Sedentary</option>
                    <option value="Active">Active</option>
                    <option value="Very Active">Very Active</option>
                  </select>
                </div>
              </div>
              
              <div className="form-buttons">
                <button 
                  type="button" 
                  className="auth-button secondary"
                  onClick={() => setStep(1)}
                >
                  Back
                </button>
                
                <button 
                  type="submit" 
                  className="auth-button" 
                  disabled={loading}
                >
                  {loading ? 'Creating Account...' : 'Create Account'}
                </button>
              </div>
            </form>
          )}
          
          {step === 2 && (
            <div className="auth-links">
              <Link to="/" className="back-link">Back to Home</Link>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Register; 