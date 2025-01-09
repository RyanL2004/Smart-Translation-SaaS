import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './translation.css';

const Translation = () => {
    const navigate = useNavigate();

    const navigateToGpt = () => {
        navigate('gpt');
    };

    return (
        <div className="translation-container">
            <header className="translation-header">
                <h1 className="gradient-text">
                    Talk, Translate, Listen: Your Multilingual Companion with GPT-4 Magic!
                </h1>
            </header>

            <main className="translation-content">
                <Link to="/gpt">
                    <button
                        type="button"
                        className="translate-button"
                        onClick={navigateToGpt}
                        aria-label="Start Translating"
                    >
                        Start Translating using AI!
                    </button>
                </Link>
            </main>
        </div>
    );
};

export default Translation;

