import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { updateUserProfile } from '../services/auth';
import Navbar from '../components/Navbar';
import '../styles/Profile.css';
import { HealthIssue, HealthIssueLabels } from '../types/health';

// Interface for user profile data
interface UserProfile {
  id?: number;
  user_id?: number;
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
  [key: string]: any; // For additional fields that might be added later
}

const Profile: React.FC = () => {
  const { user, profile, loading, logout } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editedProfile, setEditedProfile] = useState<UserProfile>({
    ...(profile || {} as UserProfile),
    health_issues: HealthIssue.NONE
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (profile) {
      setEditedProfile(profile);
    }
  }, [profile]);

  // If still loading, show a loading state
  if (loading) {
    return (
      <>
        <Navbar />
        <div className="profile-loading">Loading profile...</div>
      </>
    );
  }

  // If no user or profile, prompt to login
  if (!user) {
    return (
      <>
        <Navbar />
        <div className="profile-not-found">
          <h2>Not Logged In</h2>
          <p>Please log in to view your profile.</p>
          <Link to="/login" className="profile-button">Login</Link>
        </div>
      </>
    );
  }

  const handleEditToggle = () => {
    if (isEditing) {
      // Cancel editing, revert to original profile
      setEditedProfile(profile || {} as UserProfile);
    }
    setIsEditing(!isEditing);
    setSaveError(null);
    setSaveSuccess(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setEditedProfile({
      ...editedProfile,
      [name]: value
    });
  };

  const handleNumberInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    // For numeric fields, parse as numbers
    if (['age', 'weight', 'height'].includes(name)) {
      setEditedProfile({
        ...editedProfile,
        [name]: value ? parseFloat(value) : ''
      });
    } else {
      setEditedProfile({
        ...editedProfile,
        [name]: value
      });
    }
  };

  const handleSaveProfile = async () => {
    try {
      setIsSaving(true);
      setSaveError(null);
      setSaveSuccess(false);
      
      // Prepare data for update (only send changed fields)
      const updateData: Record<string, any> = {};
      Object.entries(editedProfile).forEach(([key, value]) => {
        // Skip id and user_id fields
        if (key !== 'id' && key !== 'user_id') {
          updateData[key] = value;
        }
      });
      
      await updateUserProfile(updateData);
      setIsEditing(false);
      setSaveSuccess(true);
      
      // Refresh the page after a short delay to show updated profile
      setTimeout(() => {
        window.location.reload();
      }, 1500);
      
    } catch (error: any) {
      console.error('Error saving profile:', error);
      setSaveError(error.response?.data?.detail || 'Failed to save profile changes. Please try again.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (!profile) {
    // User is logged in but has no profile
    return (
      <>
        <Navbar />
        <div className="profile-wrapper">
          <div className="profile-container">
            <div className="profile-header">
              <h1>Profile</h1>
              <div className="profile-actions">
                <button onClick={handleLogout} className="profile-button logout">Logout</button>
              </div>
            </div>
            
            <div className="profile-not-found">
              <h2>Profile Not Found</h2>
              <p>You don't have a profile yet. Please create one to access all features.</p>
              <Link to="/create-profile" className="profile-button">Create Profile</Link>
            </div>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />
      <div className="profile-wrapper">
        <div className="profile-container">
          <div className="profile-header">
            <h1>My Profile</h1>
            <div className="profile-actions">
              <button 
                onClick={handleEditToggle} 
                className={`profile-button ${isEditing ? 'cancel' : 'edit'}`}
              >
                {isEditing ? 'Cancel' : 'Edit Profile'}
              </button>
              <button onClick={handleLogout} className="profile-button logout">Logout</button>
            </div>
          </div>
          
          {saveSuccess && (
            <div className="profile-success">Profile updated successfully!</div>
          )}
          
          {saveError && (
            <div className="profile-error">{saveError}</div>
          )}
          
          <div className="profile-content">
            <div className="profile-section">
              <h2>Personal Information</h2>
              <div className="profile-grid">
                <div className="profile-field">
                  <span className="field-label">Email</span>
                  <span className="field-value">{user.email}</span>
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Full Name</span>
                  {isEditing ? (
                    <input 
                      type="text" 
                      name="name" 
                      value={editedProfile.name || ''} 
                      onChange={handleInputChange}
                      required
                    />
                  ) : (
                    <span className="field-value">{profile.name}</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Age</span>
                  {isEditing ? (
                    <input 
                      type="number" 
                      name="age" 
                      value={editedProfile.age || ''} 
                      onChange={handleNumberInputChange}
                      required
                      min="1"
                      max="120"
                    />
                  ) : (
                    <span className="field-value">{profile.age} years</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Phone Number</span>
                  {isEditing ? (
                    <input 
                      type="tel" 
                      name="number" 
                      value={editedProfile.number || ''} 
                      onChange={handleInputChange}
                      required
                    />
                  ) : (
                    <span className="field-value">{profile.number}</span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="profile-section">
              <h2>Physical Information</h2>
              <div className="profile-grid">
                <div className="profile-field">
                  <span className="field-label">Weight</span>
                  {isEditing ? (
                    <input 
                      type="number" 
                      name="weight" 
                      value={editedProfile.weight || ''} 
                      onChange={handleNumberInputChange}
                      required
                      step="0.1"
                      min="1"
                    />
                  ) : (
                    <span className="field-value">{profile.weight} kg</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Height</span>
                  {isEditing ? (
                    <input 
                      type="number" 
                      name="height" 
                      value={editedProfile.height || ''} 
                      onChange={handleNumberInputChange}
                      required
                      step="0.1"
                      min="1"
                    />
                  ) : (
                    <span className="field-value">{profile.height} cm</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">BMI</span>
                  <span className="field-value">
                    {(profile.weight / Math.pow(profile.height / 100, 2)).toFixed(1)}
                  </span>
                </div>
              </div>
            </div>
            
            <div className="profile-section">
              <h2>Health Information</h2>
              <div className="profile-grid">
                <div className="profile-field">
                  <span className="field-label">Health Issues</span>
                  {isEditing ? (
                    <select 
                      name="health_issues" 
                      value={editedProfile.health_issues || HealthIssue.NONE}
                      onChange={handleInputChange}
                      className="form-control"
                    >
                      {Object.entries(HealthIssueLabels).map(([value, label]) => (
                        <option key={value} value={value}>
                          {label}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <span className="field-value">
                      {editedProfile.health_issues ? HealthIssueLabels[editedProfile.health_issues as HealthIssue] : 'None'}
                    </span>
                  )}
                </div>
                
                <div className="profile-field full-width">
                  <span className="field-label">Allergies</span>
                  {isEditing ? (
                    <textarea 
                      name="allergies" 
                      value={editedProfile.allergies || ''} 
                      onChange={handleInputChange}
                      placeholder="List any food allergies"
                    />
                  ) : (
                    <span className="field-value">{profile.allergies || 'None specified'}</span>
                  )}
                </div>
                
                <div className="profile-field full-width">
                  <span className="field-label">Medications</span>
                  {isEditing ? (
                    <textarea 
                      name="medications" 
                      value={editedProfile.medications || ''} 
                      onChange={handleInputChange}
                      placeholder="List any medications"
                    />
                  ) : (
                    <span className="field-value">{profile.medications || 'None specified'}</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Blood Type</span>
                  {isEditing ? (
                    <select 
                      name="blood_type" 
                      value={editedProfile.blood_type || ''} 
                      onChange={handleInputChange}
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
                  ) : (
                    <span className="field-value">{profile.blood_type || 'Not specified'}</span>
                  )}
                </div>
              </div>
            </div>
            
            <div className="profile-section">
              <h2>Lifestyle</h2>
              <div className="profile-grid">
                <div className="profile-field">
                  <span className="field-label">Smoking Status</span>
                  {isEditing ? (
                    <select 
                      name="smoking_status" 
                      value={editedProfile.smoking_status || ''} 
                      onChange={handleInputChange}
                    >
                      <option value="">Select Status</option>
                      <option value="Never">Never</option>
                      <option value="Former">Former</option>
                      <option value="Current">Current</option>
                    </select>
                  ) : (
                    <span className="field-value">{profile.smoking_status || 'Not specified'}</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Alcohol Consumption</span>
                  {isEditing ? (
                    <select 
                      name="alcohol_consumption" 
                      value={editedProfile.alcohol_consumption || ''} 
                      onChange={handleInputChange}
                    >
                      <option value="">Select Level</option>
                      <option value="None">None</option>
                      <option value="Occasional">Occasional</option>
                      <option value="Regular">Regular</option>
                    </select>
                  ) : (
                    <span className="field-value">{profile.alcohol_consumption || 'Not specified'}</span>
                  )}
                </div>
                
                <div className="profile-field">
                  <span className="field-label">Physical Activity</span>
                  {isEditing ? (
                    <select 
                      name="physical_activity_level" 
                      value={editedProfile.physical_activity_level || ''} 
                      onChange={handleInputChange}
                    >
                      <option value="">Select Level</option>
                      <option value="Sedentary">Sedentary</option>
                      <option value="Active">Active</option>
                      <option value="Very Active">Very Active</option>
                    </select>
                  ) : (
                    <span className="field-value">{profile.physical_activity_level || 'Not specified'}</span>
                  )}
                </div>
              </div>
            </div>
          </div>
          
          {isEditing && (
            <div className="profile-save-bar">
              <button 
                onClick={handleSaveProfile} 
                className="profile-button save"
                disabled={isSaving}
              >
                {isSaving ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          )}
          
          <div className="profile-navigation">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/get-started" className="nav-link">Food Analysis</Link>
          </div>
        </div>
      </div>
    </>
  );
};

export default Profile;
