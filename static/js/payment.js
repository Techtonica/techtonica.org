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

async function ACHPay(buttonEl) {
    const accountHolderNameEl = document.getElementById('ach-account-holder-name');
    const achMessageEl = document.getElementById('ach-message');
    const achWrapperEl = document.getElementById('ach-wrapper');
  
    let ach;
    try {
      ach = await window.payments.ach();
      achWrapperEl.style.display = 'block';
    } catch (e) {
      // If the ACH payment method is not supported by your account then
      // do not enable the #ach-account-holder-name input field
      if (e.name === 'PaymentMethodUnsupportedError') {
        achMessageEl.innerText = 'ACH payment is not supported by your account';
        accountHolderNameEl.disabled = true;
      }
  
      // if we can't load ACH, we shouldn't bind events for the button
      return;
    }
  
    async function eventHandler(event) {
      const accountHolderName = accountHolderNameEl.value.trim()
      if (accountHolderName === '') {
        achMessageEl.innerText = 'Please input full name';
        return;
      }
  
      // Clear any existing messages
      window.paymentFlowMessageEl.innerText = '';
  
      try {
        const result = await ach.tokenize({
          accountHolderName,
        });
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

async function ApplePay(buttonEl) {
    const paymentRequest = window.payments.paymentRequest(
      // Use global method from sq-payment-flow.js
      window.getPaymentRequest()
    );
  
    let applePay;
    try {
      applePay = await window.payments.applePay(paymentRequest);
    } catch (e) {
      console.error(e)
      return;
    }
  
    async function eventHandler(event) {
      // Clear any existing messages
      window.paymentFlowMessageEl.innerText = '';
  
      try {
        const result = await applePay.tokenize();
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

async function GooglePay(buttonEl) {
    const paymentRequest = window.payments.paymentRequest(
      // Use global method from sq-payment-flow.js
      window.getPaymentRequest()
    );
    const googlePay = await payments.googlePay(paymentRequest);
    await googlePay.attach(buttonEl);
  
    async function eventHandler(event) {
      // Clear any existing messages
      window.paymentFlowMessageEl.innerText = '';
  
      try {
        const result = await googlePay.tokenize();
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

async function SquarePaymentFlow() {

    // Create card payment object and attach to page
    CardPay(document.getElementById('card-container'), document.getElementById('card-button'));
  
    // Create Apple pay instance
    ApplePay(document.getElementById('apple-pay-button'));
  
    // Create Google pay instance
    GooglePay(document.getElementById('google-pay-button'));
  
    // Create ACH payment
    ACHPay(document.getElementById('ach-button'));
  }
  
  window.payments = Square.payments(window.applicationId, window.locationId);
  
  window.paymentFlowMessageEl = document.getElementById('payment-flow-message');
  
  window.showSuccess = function(message) {
    window.paymentFlowMessageEl.classList.add('success');
    window.paymentFlowMessageEl.classList.remove('error');
    window.paymentFlowMessageEl.innerText = message;
  }
  
  window.showError = function(message) {
    window.paymentFlowMessageEl.classList.add('error');
    window.paymentFlowMessageEl.classList.remove('success');
    window.paymentFlowMessageEl.innerText = message;
  }
  
  window.createPayment = async function(token) {
    const dataJsonString = JSON.stringify({
      token,
      idempotencyKey: window.idempotencyKey
    });
  
    try {
      const response = await fetch('process-payment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: dataJsonString
      });
  
      const data = await response.json();
  
      if (data.errors && data.errors.length > 0) {
        if (data.errors[0].detail) {
          window.showError(data.errors[0].detail);
        } else {
          window.showError('Payment Failed.');
        }
      } else {
        window.showSuccess('Payment Successful!');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }
  
  // Hardcoded for testing purpose, only used for Apple Pay and Google Pay
  window.getPaymentRequest = function() {
    return {
      countryCode: window.country,
      currencyCode: window.currency,
      lineItems: [
        { amount: '1.23', label: 'Cat', pending: false },
        { amount: '4.56', label: 'Dog', pending: false },
      ],
      requestBillingContact: false,
      requestShippingContact: true,
      shippingContact: {
        addressLines: ['123 Test St', ''],
        city: 'San Francisco',
        countryCode: 'US',
        email: 'test@test.com',
        familyName: 'Last Name',
        givenName: 'First Name',
        phone: '1111111111',
        postalCode: '94109',
        state: 'CA',
      },
      shippingOptions: [
        { amount: '0.00', id: 'FREE', label: 'Free' },
        { amount: '9.99', id: 'XP', label: 'Express' },
      ],
      total: { amount: '1.00', label: 'Total', pending: false },
    };
  };
  
  SquarePaymentFlow();