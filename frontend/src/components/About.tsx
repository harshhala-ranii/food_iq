'use client';
import './About.css';

const About = () => {
  return (
    <section className="aboutSection">
      <div className="containerabout">
        <div className="contentabout">
          <h2>About Us</h2>
          <p>
            Welcome to FOOD-IQ, your intelligent food recognition and recommendation system. Our
            platform leverages advanced image processing and machine learning to identify food items
            from images, estimate their nutritional values, and offer personalized recommendations
            based on your dietary preferences and health profile.
          </p>
          <p>
            Whether you're tracking your daily intake, managing a specific diet, or simply curious
            about what’s on your plate, FOOD-IQ provides accurate insights to help you make informed
            choices. By combining technology with nutrition science, we aim to enhance healthy
            eating habits and support your wellness journey. Stay smart about your food with FOOD-IQ
            – because every meal matters! 🍎🥗💡
          </p>
        </div>
      </div>
    </section>
  );
};

export default About;
