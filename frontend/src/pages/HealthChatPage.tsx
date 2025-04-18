import React from 'react';
import Navbar from '../components/Navbar';
import HealthChat from '../components/HealthChat';
import './HealthChatPage.css';

const HealthChatPage: React.FC = () => {
  return (
    <div className="health-chat-page">
      <Navbar />
      <div className="health-chat-container">
        <div className="health-chat-header">
          <h1>Health Assistant Chat</h1>
          <p>Get personalized Indian food recommendations based on your health conditions and goals.</p>
        </div>
        <div className="health-chat-features">
          <div className="feature">
            <span className="feature-icon">🍽️</span>
            <span className="feature-text">Indian food suggestions</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🏥</span>
            <span className="feature-text">Health condition aware</span>
          </div>
          <div className="feature">
            <span className="feature-icon">🎯</span>
            <span className="feature-text">Personalized advice</span>
          </div>
        </div>
        <HealthChat />
      </div>
    </div>
  );
};

export default HealthChatPage; 