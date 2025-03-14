import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Diets from './pages/Diets';
import Profile from './pages/Profile';
import About from './pages/AboutPage';
import GetStarted from './pages/GetStarted';
const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/diets" element={<Diets />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/about" element={<About />} />
        <Route path="/get-started" element={<GetStarted />} />
      </Routes>
    </Router>
  );
};

export default App;
