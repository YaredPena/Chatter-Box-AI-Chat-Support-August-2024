///this  is ai generated I must comeback to this later

import { useState } from 'react';

const Chat = () => {
  const [message, setMessage] = useState('');
  const [chat, setChat] = useState<{ sender: string; message: string }[]>([]);

  const sendMessage = async () => {
    if (!message.trim()) return;
  
    setChat([...chat, { sender: 'user', message }]);
  
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
  
      const text = await response.text(); // Get the response as text for debugging
      console.log('Response Text:', text); // Log the response
      
      const data = JSON.parse(text); // Parse JSON manually
      setChat([...chat, { sender: 'user', message }, { sender: 'bot', message: data.reply }]);
    } catch (error) {
      console.error('Failed to send message:', error);
      setChat([...chat, { sender: 'user', message }, { sender: 'bot', message: 'Failed to get response' }]);
    }
  
    setMessage('');
  };
  

  return (
    <div className="flex flex-col max-w-lg mx-auto p-4 border rounded-lg shadow-lg">
      <div className="flex-1 overflow-y-auto mb-4">
        {chat.map((entry, index) => (
          <div key={index} className={`my-2 p-2 ${entry.sender === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded-lg ${entry.sender === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`}>
              {entry.message}
            </span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          type="text"
          className="flex-1 p-2 border rounded-l-lg focus:outline-none text-black"
          placeholder="Type your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button
          className="p-2 bg-blue-500 text-white rounded-r-lg"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
