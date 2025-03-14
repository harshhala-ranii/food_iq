'use client';
import { useEffect, useState } from 'react';
import './CalorieIntake.css';

const CalorieIntake = () => {
  const calorieIntake = 4000; // Example: Change dynamically
  const calorieTarget = 3000;

  const [currentDate, setCurrentDate] = useState('--/--/----');
  const [currentTime, setCurrentTime] = useState('--:--');
  const [pointerPosition, setPointerPosition] = useState({ x: 90, y: 10 });
  const [progress, setProgress] = useState('0 502');
  const [extraProgress, setExtraProgress] = useState('0 502');
  const [extraVisible, setExtraVisible] = useState(false);

  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      setCurrentDate(now.toLocaleDateString());
      setCurrentTime(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    };

    const interval = setInterval(updateDateTime, 1000);
    updateDateTime();
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const baseRotation = (calorieIntake / calorieTarget) * 360;
    const totalRotation = Math.min(baseRotation, 360);
    const extraRotation = Math.max(0, baseRotation - 360);

    let currentAngle = -90;
    const step = 3;

    let animationFrameId: number;

    const animate = () => {
      if (currentAngle >= -90 + totalRotation) {
        if (extraRotation > 0) {
          setExtraProgress(`${(extraRotation / 360) * 502} 502`);
          setExtraVisible(true);
        }
        return;
      }

      currentAngle += step;
      const radians = (currentAngle * Math.PI) / 180;
      const radius = 80;
      const centerX = 90,
        centerY = 90;

      setPointerPosition({
        x: centerX + radius * Math.cos(radians),
        y: centerY + radius * Math.sin(radians),
      });

      setProgress(`${((currentAngle + 90) / 360) * 502} 502`);

      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrameId);
  }, [calorieIntake, calorieTarget]);

  return (
    <section className="trainingPrograms">
      <div className="timer">
        <div className="calorie">Calorie</div>
        <div className="circle">
          <svg width="300" height="300" viewBox="0 0 180 180">
            <circle cx="90" cy="90" r="80" stroke="#ddd" strokeWidth="5" fill="none" />
            <circle
              cx="90"
              cy="90"
              r="80"
              stroke="black"
              strokeWidth="5"
              fill="none"
              strokeDasharray={progress}
              strokeLinecap="round"
              transform="rotate(-90 90 90)"
            />
            <circle
              cx="90"
              cy="90"
              r="80"
              stroke="red"
              strokeWidth="5"
              fill="none"
              strokeDasharray={extraProgress}
              strokeLinecap="round"
              opacity={extraVisible ? '1' : '0'}
              transform="rotate(-90 90 90)"
            />
            <circle cx={pointerPosition.x} cy={pointerPosition.y} r="5" fill="black" />
          </svg>
          <div className="circleContent">
            <p>{currentDate}</p>
            <p className="calories">2800 Cal</p>
            <p>{currentTime}</p>
          </div>
        </div>
      </div>
      <p className="calorieTarget">Calorie Target: 2500 Cal</p>
      <p className="calorieIntake">Extra Calorie: 300 Cal</p>
    </section>
  );
};

export default CalorieIntake;
