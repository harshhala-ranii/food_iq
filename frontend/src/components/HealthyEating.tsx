import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './HealthyEating.css';
import img1 from './images/img1.jpg';
import img2 from './images/img2.png';
import img3 from './images/img3.jpg';

const images = [img1, img2, img3];

const HealthyEating: React.FC = () => {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveIndex(prevIndex => (prevIndex + 1) % images.length);
    }, 3000); // Change image every 3 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="healthy-eating">
      <div className="content">
        <h2>Healthy Eating</h2>
        <p>Discover nutritious meals to fuel your performance.</p>

        <div className="buttons">
          <Link to="/about">
            <button>Learn More</button>
          </Link>
          <Link to="/get-started">
            <button>Get Started</button>
          </Link>
        </div>
      </div>
      {images.map((img, index) => (
        <img
          key={index}
          src={img}
          alt={`Healthy food ${index + 1}`}
          className={index === activeIndex ? 'active' : ''}
        />
      ))}
    </section>
  );
};

export default HealthyEating;
