import React, { useState, useEffect } from 'react';
import { FaRobot } from 'react-icons/fa';

const Home = () => {
  // State for chatbot popup visibility and language
  const [showChatbotPopup, setShowChatbotPopup] = useState(true);
  const [popupLanguage, setPopupLanguage] = useState('English');

  useEffect(() => {
    // Show chatbot popup every 5 minutes
    const interval = setInterval(() => {
      setShowChatbotPopup(true);
    }, 300000); // 300000 ms = 5 minutes

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Toggle popup language every 30 seconds
    const languageInterval = setInterval(() => {
      setPopupLanguage(prevLanguage => (prevLanguage === 'English' ? 'Hindi' : 'English'));
    }, 30000); // 30000 ms = 30 seconds

    return () => clearInterval(languageInterval);
  }, []);

  const handleClosePopup = () => {
    setShowChatbotPopup(false);
  };

  const getPopupMessage = () => {
    if (popupLanguage === 'Hindi') {
      return 'मदद चाहिए? हमारे एआई सहायक से चैट करें!';
    }
    return 'Need help? Chat with our AI assistant!';
  };

  return (
    <div className="min-h-screen">
      {/* ...existing code... */}
      
      {/* Chatbot Helper */}
      <div className="fixed bottom-4 right-4">
        <button className="bg-blue-600 text-white p-6 rounded-full shadow-lg hover:bg-blue-700 focus:outline-none transition-transform transform hover:scale-110">
          <FaRobot className="text-3xl" />
        </button>
      </div>

      {/* Chatbot Popup */}
      {showChatbotPopup && (
        <div className="fixed bottom-20 right-4 bg-white p-4 rounded-lg shadow-lg border border-gray-300 animate-bounce">
          <div className="flex justify-between items-center">
            <p className="text-gray-800">{getPopupMessage()}</p>
            <button onClick={handleClosePopup} className="text-gray-600 hover:text-gray-800">
              &times;
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Home;