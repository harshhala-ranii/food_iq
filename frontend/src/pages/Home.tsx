import React, { useEffect, useState } from 'react';
import Title from '../components/Title';
import HealthyEating from '../components/HealthyEating';
import Navbar from '../components/Navbar';
import CalorieIntake from '../components/CalorieIntake';
import Footer from '../components/Footer';
import './Home.css';

const Home: React.FC = () => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    setLoaded(true);
  }, []);

  return (
    <div className={`home-page ${loaded ? 'loaded' : ''}`}>
      <Navbar />
      <div className="home-content">
        <Title />
        <HealthyEating />
        <CalorieIntake />
      </div>
      <Footer />
    </div>
  );
};

export default Home;
