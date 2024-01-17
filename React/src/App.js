import './chatbox.css'; // Import your CSS file for styling


import React, { useState, useRef, useEffect } from 'react';

const Chatbox = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesContainerRef = useRef(null);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === '') return;

    try {
      // Add user message to messages
      setMessages((prevMessages) => [...prevMessages, { text: inputValue, sender: 'user' }]);

      // Hit the API
      const response = await fetch(' https://eaa3-2607-fea8-659c-5400-2c81-fb85-3cc2-291c.ngrok-free.app/get_answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ Question: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      // Parse the API response
      const data = await response.json();

      // Add assistant message with the API answer to messages
      setMessages((prevMessages) => [...prevMessages, { text: data.Answer, sender: 'assistant' }]);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Handle error, e.g., set an error message in the messages state
    } finally {
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  useEffect(() => {
    // Scroll the messages container to the bottom whenever messages change
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div>
      <div className="logo-container">
        <img src="lplogoremade.png" alt="Your Logo" className="logo" />
      </div>
      <div className="chatbox">
        <div ref={messagesContainerRef} className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <span className="sender">{message.sender === 'user' ? 'You' : 'Bruno Mama'}:</span>
              {message.text}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            placeholder="Type your question here..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default Chatbox;