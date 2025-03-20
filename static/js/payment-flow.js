async function SquarePaymentFlow() {

  // Create card payment object and attach to page
  CardPay(
    document.getElementById("card-container"),
    document.getElementById("payment-button")
  );
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
    const response = await fetch('/process-payment', {
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

      window.sendSlackNotification();
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

window.sendSlackNotification = async function() {
  var referralValue = "no";
  
  document.getElementsByName("referral").forEach(radio => {
    if(radio.checked){
      referralValue = radio.value;
    }
  });

  var notificationValues = {
    firstName: document.getElementById('firstname').value,
    lastName: document.getElementById('lastname').value,
    email: document.getElementById('email').value,
    jobTitle: document.getElementById('jobtitle').value,
    company: document.getElementById('company').value,
    type: document.getElementById('type').value,
    educationReq: document.getElementById('educationreq').value,
    location: document.getElementById('location').value, 
    referral: referralValue,
    salaryRange: document.getElementById('salaryrange').value,
    description: document.getElementById('description').value,
    applicationLink: document.getElementById('applicationlink').value
  };

  var dataJsonString = JSON.stringify(notificationValues);

  try {
    const response = await fetch('/send-posting', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: dataJsonString
    });
  }
  catch (error) {
    console.error('Error:', error);
  }
}

SquarePaymentFlow();