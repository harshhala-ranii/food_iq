import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar: React.FC = () => {
  return (
    <nav className="navbar">
      <div className="logo">Food-IQ</div>
      <ul>
        <li>
          <NavLink to="/" className={({ isActive }) => (isActive ? 'active' : '')}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/diets" className={({ isActive }) => (isActive ? 'active' : '')}>
            Diets
          </NavLink>
        </li>
        <li>
          <NavLink to="/get-started" className={({ isActive }) => (isActive ? 'active' : '')}>
            Get Started
          </NavLink>
        </li>
        <li>
          <NavLink to="/profile" className={({ isActive }) => (isActive ? 'active' : '')}>
            Profile
          </NavLink>
        </li>
        <li>
          <NavLink to="/chat" className={({ isActive }) => (isActive ? 'active' : '')}>
            Health Chat
          </NavLink>
        </li>
        <li>
          <NavLink to="/about" className={({ isActive }) => (isActive ? 'active' : '')}>
            About
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
