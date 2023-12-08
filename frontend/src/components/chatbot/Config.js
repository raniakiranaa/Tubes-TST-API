import { createChatBotMessage } from 'react-chatbot-kit';

const botName = 'Buddy';

const config = {
    initialMessages: [createChatBotMessage(`Hi! I'm ${botName}. I'm here as your shopping companion. How can I help you today?`)],
    botName: botName,
    // widgets: [
    //     {
    //       widgetName: 'options',
    //       widgetFunc: (props) => <Options {...props} />,
    //     }
    //   ],
    state: {
        gist: '',
        infoBox: '',
    },
    customComponents: {},
    // customMessages: {
    //     custom: (props) => <CustomMessage {...props} />,
    //   },
    customStyles: {
      botMessageBox: {
        backgroundColor: '#376B7E',
      },
      chatButton: {
        backgroundColor: '#5ccc9d',
      },
    },
};

export default config;