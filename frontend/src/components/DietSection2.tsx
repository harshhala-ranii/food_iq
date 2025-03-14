import React from 'react';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';
import diets2 from './images/food.png';
import './DietSection2.css'; // Import the CSS file

const dietData = [
  {
    foodGroup: 'Vegetables',
    intake: '350g - 500g',
    benefits: 'Rich in vitamins, minerals, fiber, and antioxidants.',
  },
  {
    foodGroup: 'Fruits',
    intake: '150g',
    benefits: 'Provides vitamins, minerals, fiber, and natural sugars.',
  },
  {
    foodGroup: 'Cereals & Millets',
    intake: '240g',
    benefits: 'Primary source of carbohydrates for energy.',
  },
  {
    foodGroup: 'Pulses, Eggs & Meat',
    intake: '90g',
    benefits: 'High in protein, essential for muscle repair and iron intake.',
  },
  {
    foodGroup: 'Nuts & Seeds',
    intake: '30g',
    benefits: 'Healthy fats, proteins, and micronutrients for heart and brain health.',
  },
  {
    foodGroup: 'Fats & Oils',
    intake: '27g',
    benefits: 'Needed for vitamin absorption and brain function (consume in moderation).',
  },
  {
    foodGroup: 'Milk/Curd',
    intake: '300ml',
    benefits: 'Good source of calcium and protein for bone health.',
  },
];

const DietSection2: React.FC = () => {
  const { ref: textRef, inView: textInView } = useInView({ triggerOnce: true });
  const { ref: tableRef, inView: tableInView } = useInView({ triggerOnce: true });
  const { ref: imageRef, inView: imageInView } = useInView({ triggerOnce: true });

  return (
    <motion.div className="diet-section2">
      <motion.div
        className="image-section2"
        ref={imageRef}
        initial={{ opacity: 0, x: -50 }}
        animate={imageInView ? { opacity: 1, x: 0 } : { opacity: 0, x: -50 }}
        transition={{ duration: 1.5, delay: 0 }}
      >
        <img src={diets2} alt="Healthy Food" className="food-image2" />
      </motion.div>

      <div className="text-section2" ref={textRef}>
        <motion.h1
          className="headingdiet2"
          initial={{ opacity: 0, y: -20 }}
          animate={textInView ? { opacity: 1, y: 0 } : { opacity: 0, y: -20 }}
          transition={{ duration: 1, delay: 0 }}
        >
          My Plate for the day!
        </motion.h1>

        {/* Animated Table */}
        <motion.div
          className="table-container"
          ref={tableRef}
          initial={{ opacity: 0 }}
          animate={tableInView ? { opacity: 1 } : { opacity: 0 }}
          transition={{ duration: 1, delay: 0.5 }}
        >
          <table className="diet-table">
            <thead>
              <tr>
                <th>Food Group</th>
                <th>Recommended Intake</th>
                <th>Benefits</th>
              </tr>
            </thead>
            <tbody>
              {dietData.map((item, index) => (
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
    </motion.div>
  );
};

export default DietSection2;
