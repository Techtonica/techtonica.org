async function CardPay(fieldEl, buttonEl) {
  // Create a card payment object and attach to page
  const card = await window.payments.card({
    style: {
      '.input-container.is-focus': {
        borderColor: '#006AFF'
      },
      '.message-text.is-error': {
        color: '#BF0020'
      }
    }
  });
  await card.attach(fieldEl);

  async function eventHandler(event) {
    // Clear any existing messages
    window.paymentFlowMessageEl.innerText = '';
    
    // Check if the checkbox is checked first, before other validation
    const conductCheckbox = document.getElementById('code-of-conduct-checkbox');
    if (!conductCheckbox.checked) {
      conductCheckbox.parentElement.classList.add('invalid');
      conductCheckbox.focus();
      window.showError('Please accept the Code of Conduct to proceed.');
      return;
    }
    
    // Show loading message
    window.showError('Validating form...');
    
    // Then validate the rest of the form including profanity check
    const isValid = await window.validateForm();
    if (!isValid) {
      return;
    }

    // Show processing message
    window.showError('Processing payment information...');

    try {
      const result = await card.tokenize();
      if (result.status === 'OK') {
        // Use global method from sq-payment-flow.js
        window.createPayment(result.token);
      }
    } catch (e) {
      if (e.message) {
        window.showError(`Error: ${e.message}`);
      } else {
        window.showError('Something went wrong');
      }
    }
  }

  buttonEl.addEventListener('click', eventHandler);
}