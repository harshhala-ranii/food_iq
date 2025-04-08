// pages/Programs.tsx
import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import FoodImageUpload from '../components/FoodImageUpload';
import FoodClasses from '../components/FoodClasses';
import './GetStarted.css';

const GetStarted: React.FC = () => {
  return (
    <div className="get-started-page">
      <Navbar />
      
      <div className="get-started-hero">
        <div className="hero-content">
          <h1>Analyze Your Food</h1>
          <p>Upload a photo of your meal or search by name to get instant nutrition information</p>
        </div>
      </div>
      
      <div className="get-started-container">
        <section className="upload-section">
          <FoodImageUpload />
        </section>
        
        <section className="search-info">
          <div className="search-methods">
            <div className="search-method">
              <h3>Image Recognition</h3>
              <p>Upload a photo of your food and our AI will identify it and provide nutrition information.</p>
              <ul>
                <li>Works best with clear, well-lit photos</li>
                <li>Supports JPG/JPEG image formats</li>
                <li>Instantly analyzes your meal</li>
              </ul>
            </div>
            
            <div className="search-method">
              <h3>Manual Search</h3>
              <p>Know what you're eating? Simply type the name to get nutrition details.</p>
              <ul>
                <li>Quick search by food name</li>
                <li>Auto-suggestions as you type</li>
                <li>Keyboard navigation (use arrow keys and Enter)</li>
              </ul>
            </div>
          </div>
        </section>
        
        <section className="food-classes-section">
          <FoodClasses title="Foods We Can Identify" />
        </section>
        
        <section className="how-it-works">
          <h2>How It Works</h2>
          <div className="steps-container">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Take a Photo or Search</h3>
              <p>Take a clear photo of your Indian food dish or search by name</p>
            </div>
            
            <div className="step">
              <div className="step-number">2</div>
              <h3>Upload &amp; Analyze</h3>
              <p>Upload the photo or enter the food name and get results</p>
            </div>
            
            <div className="step">
              <div className="step-number">3</div>
              <h3>Get Results</h3>
              <p>View detailed nutrition information for your meal</p>
            </div>
          </div>
        </section>
      </div>
      
      <Footer />
    </div>
  );
};

export default GetStarted;
