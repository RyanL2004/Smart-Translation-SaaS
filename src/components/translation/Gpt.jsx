// ChatBox.jsx

import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import SpeechToText from './SpeechToText'; // Import the SpeechToText component

const API_KEY = process.env.REACT_APP_API_KEY;



// Prompts to determine ChatGPT functionality
const systemMessage = {
  "role": "system",
"content":"Translate the following legal document excerpt from French to English.",
"content":"Convert the scientific paper abstract provided in French into English.",
"content":"Translate the medical diagnosis report from French to English.",
"content":"Provide an English translation for the technical manual section written in French.",
"content":"Convert the financial report summary from French to English.",
"content":"Translate the culinary recipe instructions from French to English.",
"content":"Provide an English translation for the academic research paper introduction written in French.",
"content":"Convert the software user interface guide from French to English.",
"content":"Translate the engineering specifications document from French to English.",
"content":"Provide an English translation for the marketing brochure content written in French.",
};

function ChatBox() {
  const [messages, setMessages] = useState([
    {
      message: "Hello, I'm the Turbo Translation AI! I can translate for you anything!",
      sentTime: "just now",
      sender: "ChatGPT"
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const inputRef = useRef(null);
  const messageListRef = useRef(null);
  const isRecordingRef = useRef(false); // Ref to track if recording is in progress

  useEffect(() => {
    // Scroll to the bottom of the message list when new messages are added
    messageListRef.current.scrollTop = messageListRef.current.scrollHeight;
  }, [messages]);

  const handleSend = async () => {
    const message = inputRef.current.value.trim();
    if (message !== '') {
      const newMessage = {
        message,
        direction: 'outgoing',
        sender: "user"
      };

      const newMessages = [...messages, newMessage];

      setMessages(newMessages);
      setIsTyping(true);

      await processMessageToChatGPT(newMessages);
      inputRef.current.value = '';
    }
  };
  

  async function processMessageToChatGPT(chatMessages) {
    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant";
      } else {
        role = "user";
      }
      return { role: role, content: messageObject.message };
    });

    const apiRequestBody = {
      "model": "gpt-3.5-turbo",
      "messages": [
        systemMessage,
        ...apiMessages
      ]
    };

    await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(apiRequestBody)
    }).then((data) => {
      return data.json();
    }).then((data) => {
      console.log(data);
      setMessages([...chatMessages, {
        message: data.choices[0].message.content,
        sender: "ChatGPT"
      }]);
      setIsTyping(false);
    });
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  const handleStartRecording = () => {
    // Start recording speech
    isRecordingRef.current = true;
    // Implement logic to start recording speech here
  };

  const handleStopRecording = () => {
    // Stop recording speech
    isRecordingRef.current = false;
    // Implement logic to stop recording speech here
    // You can call handleSend function here with the recorded speech
  };

  const handleVoiceInput = () => {
    // Implement hold-to-speak functionality
    if (!isRecordingRef.current) {
      handleStartRecording();
    }
  };

  // Function to handle speech recognition result
  const handleSpeechRecognitionResult = (transcript) => {
    // Set the transcript as the value of the input field
    inputRef.current.value = transcript;
    // Send the transcript as a message
    handleSend();
  };

  return (
    <div className="chat-box">
      <div className="message-list" ref={messageListRef}>
        {messages.map((message, i) => (
          <div className={`message ${message.sender}`} key={i}>{message.message}</div>
        ))}
        {isTyping && <div className="typing-indicator">ChatGPT is typing...</div>}
      </div>
      <div className="input-container">
        <input ref={inputRef} type="text" placeholder="Type your message here" onKeyPress={handleKeyPress} />
        <button onClick={handleSend}>Send</button>
        <SpeechToText onSpeechRecognitionResult={handleSpeechRecognitionResult} /> {/* Add SpeechToText component */}
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <div className="container">
        <ChatBox />
      </div>
    </div>
  );
}

export default App;
