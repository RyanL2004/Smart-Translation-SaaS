import React from 'react'
import './header.css'
import people from '../../assets/people.png'
import ai from '../../assets/ai.png'
import { Link, useNavigate, navigate } from 'react-router-dom'
import Signup from '../../components/Signup'

const Header = () => {
  const navigate = useNavigate();
  const navigateToSignUp = () => {
    navigate('/signup');
  };
  return (
    <div className="gpt3__header section__padding" id="home"> 
      <div className="gpt3__header-content">
        <h1 className="gradient__text">Let’s Build Something amazing with GPT-4</h1>
        <p> Yet bed any for travelling assistance indulgence unpleasing. Not thoughts all exercise blessing. Indulgence way everything joy alteration boisterous the attachment. Party we years to order allow asked of.</p>
      
        <div className="gpt3__header-content__input">
          <input type="email" placeholder="Your Email Address"></input>
          <Link to="/signup">
          <button type="button" onClick={navigateToSignUp}>Get Started</button>
          </Link>
        </div>

        <div className="gpt3__header-content__people">
          <img src={people} alt="people" />
          <p>Over 1000 people requested access a visit in last 2 weeks</p>
        </div>
      </div>
      <div className="gpt3__header-image">
        <img src={ai} alt="ai" />
      </div>
    </div> 
    
  )
}

export default Header