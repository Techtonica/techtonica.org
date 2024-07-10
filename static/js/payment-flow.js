async function SquarePaymentFlow() {

    // Create card payment object and attach to page
    CardPay(document.getElementById('card-container'), document.getElementById('card-button'));

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
      const response = await fetch('/fast/process-payment', {
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

  SquarePaymentFlow();