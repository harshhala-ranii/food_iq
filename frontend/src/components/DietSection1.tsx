import React from 'react';
import { motion } from 'framer-motion';
import './DietSection1.css'; // Import the CSS file
import diets1 from './images/diets1.png'; // Import the image

const DietSection1: React.FC = () => {
  return (
    <motion.div
      className="diet-section"
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 2 }}
    >
      <div className="text-section">
        <motion.h1
          className="heading"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0 }}
        >
          Diets for a Healthy Lifestyle
        </motion.h1>
        <motion.p
          className="paragraph"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1.5, delay: 0 }}
        >
          Discover various diets that promote health and wellness.
        </motion.p>
      </div>
      <motion.div
        className="image-section"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 0 }}
      >
        <img src={diets1} alt="Healthy Food" className="food-image" />
      </motion.div>
    </motion.div>
  );
};

export default DietSection1;
