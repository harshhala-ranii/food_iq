'use client';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="logoSection">
          <h2 className="logo">Food-IQ</h2>
          <p>Balance your diet now.</p>
        </div>
      </div>

      <div className="bottomBar">
        <p>&copy; {new Date().getFullYear()} Food-IQ. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
