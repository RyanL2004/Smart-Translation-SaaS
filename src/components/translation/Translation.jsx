// Translation.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import openai from 'openai';
import './translation.css';

console.log('OpenAI API Key:', process.env.REACT_APP_OPENAI_API_KEY);
openai.apiKey = process.env.REACT_APP_OPENAI_API_KEY;

const Translation = () => {
    const navigate = useNavigate();

    const navigateToGpt = () => {
      navigate('gpt')
    };
    
    
    

  

  return (
      <div className="translation-container">

      <div className="translation-button-container">
        <h1 className="gradient__text">Talk, Translate, Listen: Your Multilingual Companion with GPT-4 Magic!</h1>

      
              <Link to="/gpt">
                <button type="button" onClick={navigateToGpt}>
                  Start Translating using AI!
                </button>
              </Link>
      </div>
      </div>
    
      

    )
};


export default Translation;
