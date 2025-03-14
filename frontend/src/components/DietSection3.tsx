import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import ketoImage from './images/keto.png'; // Replace with actual image path
import './DietSection3.css'; // Import CSS file for styling

const ketoDietData = [
  {
    foodGroup: 'Healthy Fats',
    intake: '70-80%',
    benefits: 'Main energy source; supports brain and hormone function.',
  },
  {
    foodGroup: 'Protein',
    intake: '15-25%',
    benefits: 'Builds and repairs tissues, essential for muscle maintenance.',
  },
  {
    foodGroup: 'Low-Carb Vegetables',
    intake: '5-10%',
    benefits: 'Rich in fiber, vitamins, and minerals while keeping carbs low.',
  },
  {
    foodGroup: 'Dairy (Full Fat)',
    intake: 'Moderate',
    benefits: 'Good source of fats and calcium; supports gut health.',
  },
  {
    foodGroup: 'Nuts & Seeds',
    intake: 'Small portions',
    benefits: 'Provides fiber, healthy fats, and micronutrients.',
  },
  {
    foodGroup: 'Berries (Limited)',
    intake: 'Occasional',
    benefits: 'Low in carbs, rich in antioxidants, and high in fiber.',
  },
  {
    foodGroup: 'Eggs & Meat',
    intake: 'Essential',
    benefits: 'High-quality protein and essential fats for satiety and muscle health.',
  },
];

const KetoDietSection: React.FC = () => {
  const { ref: textRef, inView: textInView } = useInView({ triggerOnce: true });
  const { ref: tableRef, inView: tableInView } = useInView({ triggerOnce: true });
  const { ref: imageRef, inView: imageInView } = useInView({ triggerOnce: true });

  return (
    <motion.div className="keto-diet-section">
      {/* Text Section with Table */}
      <div className="text-section" ref={textRef}>
        <motion.h1
          className="heading-keto"
          initial={{ opacity: 0, y: -20 }}
          animate={textInView ? { opacity: 1, y: 0 } : { opacity: 0, y: -20 }}
          transition={{ duration: 1, delay: 0 }}
        >
          Keto Diet Essentials
        </motion.h1>

        {/* Animated Table */}
        <motion.div
          className="table-container"
          ref={tableRef}
          initial={{ opacity: 0 }}
          animate={tableInView ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <table className="keto-diet-table">
            <thead>
              <tr>
                <th>Food Group</th>
                <th>Recommended Intake</th>
                <th>Benefits</th>
              </tr>
            </thead>
            <tbody>
              {ketoDietData.map((item, index) => (
                <tr key={index}>
                  <td>{item.foodGroup}</td>
                  <td>{item.intake}</td>
                  <td>{item.benefits}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </motion.div>
      </div>

      {/* Image Section */}
      <motion.div
        className="image-section"
        ref={imageRef}
        initial={{ opacity: 0, x: 50 }}
        animate={imageInView ? { opacity: 1, x: 0 } : { opacity: 0, x: 50 }}
        transition={{ duration: 1.5, delay: 0 }}
      >
        <img src={ketoImage} alt="Keto Diet Food" className="keto-food-image" />
      </motion.div>
    </motion.div>
  );
};

export default KetoDietSection;
