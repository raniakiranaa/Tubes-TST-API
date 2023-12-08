import React from 'react';

const MessageParser = ({ children, actions }) => {
  const parse = (message) => {
  
    // search product info
    const productKeywords = ['about product', 'product info', 'details on'];
    const productKeyword = productKeywords.find(keyword => message.toLowerCase().includes(keyword));
    const extractProductName = (message, keyword) => {
      const startIndex = message.toLowerCase().indexOf(keyword) + keyword.length;
      const endIndex = message.length;
      const productName = message.substring(startIndex, endIndex).trim();
      return productName;
    };

    if (productKeyword) {
      const productName = extractProductName(message, productKeyword);
      if (productName) {
        actions.handleProductInfo(productName);
      } else {
        console.log("Please provide a valid product name.");
      }
    }

    // get information transaction
    const transactionKeywords = ['transaction for', 'order for', 'purchase for', 'most bought brand for'];
    const transactionKeyword = transactionKeywords.find(keyword => message.toLowerCase().includes(keyword));
    const extractTransactionName = (message, keyword) => {
      const startIndex = message.toLowerCase().indexOf(keyword) + keyword.length;
      const endIndex = message.length;
      const transactionName = message.substring(startIndex, endIndex).trim();
      return transactionName;
    };

    if (transactionKeyword) {
      const productName = extractTransactionName(message, transactionKeyword);
      if (productName) {
        actions.handleTransactionInfo(productName);
      } else {
        console.log("Please provide a valid product name.");
      }
    }

    // get product recommendation
    const recommendationKeywords = ['recommendation for', 'recommend me product'];
    const recommendationKeyword = recommendationKeywords.find(keyword => message.toLowerCase().includes(keyword));
    const extractRecommendationName = (message, keyword) => {
      const startIndex = message.toLowerCase().indexOf(keyword) + keyword.length;
      const endIndex = message.length;
      const recommendationName = message.substring(startIndex, endIndex).trim();
      return recommendationName;
    };

    if (recommendationKeyword) {
      const productID = extractRecommendationName(message, recommendationKeyword);
      if (productID) {
        actions.handleProductRec(productID);
      } else {
        console.log("Please provide a valid product ID.");
      }
    }

    // get menu recommendation based on calories
    const menuKeywords = ['calories are below', 'calories below'];
    const menuKeyword = menuKeywords.find(keyword => message.toLowerCase().includes(keyword));
    const extractMenuName = (message, keyword) => {
      const startIndex = message.toLowerCase().indexOf(keyword) + keyword.length;
      const endIndex = message.length;
      const menuName = message.substring(startIndex, endIndex).trim();
      return menuName;
    };

    if (menuKeyword) {
      const calories = extractMenuName(message, menuKeyword);
      if (calories) {
        actions.handleMenuRec(calories);
      } else {
        console.log("Please provide a valid calories amount.");
      }
    }

    // get menu recommendation based on age and gender
    if (message.includes('I am a')) {
      // match the pattern of message
      const userMessage = message;
      const pattern = /I am a (\d+) year old (\w+)/i;
      const match = userMessage.match(pattern);
      if (match) {
        const age = match[1]; 
        const gender = match[2];

        console.log(`Input: ${userMessage}`);
        console.log(`Age: ${age}`);
        console.log(`Gender: ${gender}`);

        actions.handleStandarRec(age, gender);
      } else {
        console.log("Message does not match the expected pattern.");
      }
    }

    // get all menu
    if (message.includes('cooking something')) {
      actions.handleAllMenu();
    }

    // get ingredients of menu
    const ingredientsKeywords = ['ingredients for', 'ingredient for'];
    const ingredientsKeyword = ingredientsKeywords.find(keyword => message.toLowerCase().includes(keyword));
    const extractIngredientsName = (message, keyword) => {
      const startIndex = message.toLowerCase().indexOf(keyword) + keyword.length;
      const endIndex = message.length;
      const ingredientsName = message.substring(startIndex, endIndex).trim();
      return ingredientsName;
    };

    if (ingredientsKeyword) {
      const menuName = extractIngredientsName(message, ingredientsKeyword);
      if (menuName) {
        actions.handleIngredients(menuName);
      } else {
        console.log("Please provide a valid menu name.");
      }
    }

    // handle assign cart
    // if (message.includes('assign to a cart')) {
    //   actions.handleAssignCart();
    // }

    // handle bye
    if (message.includes('bye') || message.includes('thank you') ) {
      actions.handleBye();
    }

  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse,
          actions,
        });
      })}
    </div>
  );
};

export default MessageParser;