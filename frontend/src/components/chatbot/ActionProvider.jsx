import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {

  const handleBye = () => {
    const botMessage = createChatBotMessage("Glad I could help. See you next time!")
    setState((prevState) => ({
      ...prevState,
      messages: [...prevState.messages, botMessage],
    }));
  }

  const handleProductInfo = async (name_product) => {
    try {
      const token = sessionStorage.getItem('token');
      console.log("token: " + token);

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/product/${name_product}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      // Create an array of chatbot messages
      const messages = data.split('\n').map(message => createChatBotMessage(message));

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, ...messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleTransactionInfo = async (productName) => {
    try {
      const token = sessionStorage.getItem('token');
      console.log("token: " + token);

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/detail_transaction/?name_product=${productName}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      const messages = createChatBotMessage(data);

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleProductRec = async (productID) => {
    try {
      const token = sessionStorage.getItem('token');
      console.log("token: " + token);

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/detail_transaction/${productID}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      const messages = createChatBotMessage(data);

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleMenuRec = async (calories) => {
    try {
      const token = sessionStorage.getItem('token');
      const username = sessionStorage.getItem('username');
      console.log("token: " + token);
      console.log("username: " + username)

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/recommendations/${username}?target_kalori=${calories}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      // Create an array of chatbot messages
      const messages = data.split('\n').map(message => createChatBotMessage(message));

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, ...messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleStandarRec = async (age, gender) => {
    try {
      const token = sessionStorage.getItem('token');
      const username = sessionStorage.getItem('username');
      console.log("token: " + token);
      console.log("username: " + username)

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/recommendations?user_name=${username}&umur=${age}&jenis_kelamin=${gender}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      // Create an array of chatbot messages
      const messages = data.split('\n').map(message => createChatBotMessage(message));

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, ...messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleAllMenu = async () => {
    try {
      const token = sessionStorage.getItem('token');
      console.log("token: " + token);

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/recommendations`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      // Create an array of chatbot messages
      const messages = data.split('\n').map(message => createChatBotMessage(message));

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, ...messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  const handleIngredients = async (menu) => {
    try {
      const token = sessionStorage.getItem('token');
      console.log("token: " + token);

      const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/menus/${menu}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      const data = response.data;

      const messages = createChatBotMessage(data);

      setState(prevState => ({
        ...prevState,
        messages: [...prevState.messages, messages],
      }));
    } catch (error) {
      console.log(error);
    }
  }

  // const handleAssignCart = async () => {
  //   try {
  //     const token = sessionStorage.getItem('token');
  //     const username = sessionStorage.getItem('username');
  //     console.log("token: " + token);
  //     console.log("username: " + username)

  //     const response = await axios.get(`http://smartcart3.dpabdmdug3daatbx.southeastasia.azurecontainer.io/cart`, {
  //       headers: {
  //         Authorization: `Bearer ${token}`
  //       }
  //     });

  //     const data = response.data;

  //     const messages = createChatBotMessage(data);

  //     setState(prevState => ({
  //       ...prevState,
  //       messages: [...prevState.messages, messages],
  //     }));
  //   } catch (error) {
  //     console.log(error);
  //   }
  // }

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleProductInfo,
            handleTransactionInfo,
            handleProductRec,
            handleMenuRec,
            handleStandarRec,
            handleAllMenu,
            handleIngredients,
            handleBye,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;