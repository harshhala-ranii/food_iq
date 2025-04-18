import React from 'react';
import { Link } from 'react-router-dom';
import './HealthChatPromo.css';

const HealthChatPromo: React.FC = () => {
  return (
    <div className="health-chat-promo">
      <div className="health-chat-promo-content">
        <h2>Ask Our Health Assistant</h2>
        <p>Get personalized Indian food recommendations based on your health conditions and goals.</p>
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
        <Link to="/chat" className="chat-button">
          Start Chatting
        </Link>
      </div>
    </div>
  );
};

export default HealthChatPromo; 