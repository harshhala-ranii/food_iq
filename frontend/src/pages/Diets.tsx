import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import './Diets.css'; // Import your custom styles
import DietSection2 from '../components/DietSection2';
import Navbar from '../components/Navbar';
import DietSection1 from '../components/DietSection1';
import DietSection3 from '../components/DietSection3';
const Diets: React.FC = () => {
  return (
    <div className="diets-page-wrapper">
      <Navbar />
      <DietSection1 />
      <DietSection2 />
      <DietSection3 />
    </div>
  );
};

export default Diets;
