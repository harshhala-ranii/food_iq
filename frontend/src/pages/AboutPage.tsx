import React from 'react';
import About from '../components/About';
import Navbar from '../components/Navbar';
import './AboutPage.css'; // Import the CSS file

const AboutPage: React.FC = () => {
  return (
    <div className="about-page-wrapper">
      <Navbar />
      <div className="about-page">
        <div className="about-content">
          <About />
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
