import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'
import config from './Config.js';
import MessageParser from './MessageParser.jsx';
import ActionProvider from './ActionProvider.jsx';

const ChatComponent = () => {
  return (
    <div className="mb-20 shadow-md">
      <Chatbot className="react-chatbot-kit-chat-container"
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
    </div>
  );
};

export default ChatComponent;