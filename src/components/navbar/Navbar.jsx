import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { RiMenu3Line, RiCloseLine } from 'react-icons/ri';
import logo from '../../assets/logo.svg';
import './navbar.css';

const Menu = () => (
  <>
    <p><Link to="#home">Home</Link></p>
    <p><Link to="#wgpt3">What is GPT?</Link></p>
    <p><Link to="#possibility">Open AI</Link></p>
    <p><Link to="#features">Case Studies</Link></p>
    <p><Link to="#blog">Library</Link></p>
  </>
);

const Navbar = () => {
  const [toggleMenu, setToggleMenu] = useState(false);
  const navigate = useNavigate();

  const navigateToSignUp = () => {
    navigate('/signup');
  };

  return (
    <div className="gpt3__navbar">
      <div className="gpt3__navbar-links">
        <div className="gpt3__navbar-links_logo">
          <h1>WeTranslate</h1>
        </div>
        <div className="gpt3__navbar-links_container">
          <Menu />
        </div>
      </div>
      <div className="gpt3__navbar-sign">
        <div className="gpt3__navbar-login_button">
          <Link to="/login">
            <button type="button">Login</button>
          </Link>
        </div>
        <div className="gpt3__navbar-signin_button">
          <Link to="/signup">
            <button type="button" onClick={navigateToSignUp}>Sign up</button>
          </Link>
        </div>
      </div>
      <div className="gpt3__navbar-menu">
        {toggleMenu
          ? <RiCloseLine color="#fff" size={27} onClick={() => setToggleMenu(false)} />
          : <RiMenu3Line color="#fff" size={27} onClick={() => setToggleMenu(true)} />
        }
        {toggleMenu && (
          <div className="gpt3__navbar-menu_container">
            <div className="gpt3__navbar-menu_container-links">
              <Menu />
            </div>
            <div className="gpt3__navbar-menu_container-links-sign">
              <Link to="/signup">
                <button type="button" onClick={navigateToSignUp}>Sign up</button>
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
