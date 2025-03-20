async function SquarePaymentFlow() {
  // Create card payment object and attach to page
  CardPay(
    document.getElementById('card-container'),
    document.getElementById('card-button')
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

// Validate form fields
window.validateForm = function() {
  const requiredFields = [
    'firstname', 'lastname', 'email', 'jobtitle', 
    'company', 'location'
  ];
  
  let isValid = true;
  let firstInvalidField = null;
  
  // Check all required fields
  for (const fieldId of requiredFields) {
    const field = document.getElementById(fieldId);
    if (!field.value.trim()) {
      field.classList.add('invalid');
      isValid = false;
      if (!firstInvalidField) firstInvalidField = field;
    } else {
      field.classList.remove('invalid');
    }
  }
  
  // Validate email format
  const emailField = document.getElementById('email');
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailField.value.trim() && !emailPattern.test(emailField.value)) {
    emailField.classList.add('invalid');
    isValid = false;
    if (!firstInvalidField) firstInvalidField = emailField;
  }
  
  // Check if referral radio is selected
  const referralRadios = document.getElementsByName('referral');
  let referralSelected = false;
  referralRadios.forEach(radio => {
    if (radio.checked) {
      referralSelected = true;
    }
  });
  
  if (!referralSelected) {
    document.getElementById('radio-wrapper').classList.add('invalid');
    isValid = false;
    if (!firstInvalidField) firstInvalidField = document.getElementById('radio-wrapper');
  } else {
    document.getElementById('radio-wrapper').classList.remove('invalid');
  }
  
  // Check if code of conduct checkbox is checked - this is critical
  const conductCheckbox = document.getElementById('code-of-conduct-checkbox');
  if (!conductCheckbox.checked) {
    conductCheckbox.parentElement.classList.add('invalid');
    isValid = false;
    // Make the checkbox a priority for focus if it's not checked
    firstInvalidField = conductCheckbox;
  } else {
    conductCheckbox.parentElement.classList.remove('invalid');
  }
  
  // Scroll to first invalid field if validation fails
  if (!isValid && firstInvalidField) {
    firstInvalidField.focus();
    window.showError('Please fill in all required fields and accept the Code of Conduct.');
  }
  
  return isValid;
}

window.createPayment = async function(token) {
  // Validate form before processing payment
  if (!window.validateForm()) {
    return;
  }
  
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
    window.showError('An error occurred while processing your payment.');
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
  } catch (error) {
    console.error('Error:', error);
  }
}

// Form and code of conduct checkbox functionality
document.addEventListener("DOMContentLoaded", () => {
  const termsCheckbox = document.getElementById("code-of-conduct-checkbox");
  const cardButton = document.getElementById("card-button");
  
  // Set initial button state - ensure it's disabled if checkbox is not checked
  cardButton.disabled = !termsCheckbox.checked;
  
  // Add visual indicator for disabled state
  if (cardButton.disabled) {
    cardButton.classList.add('disabled');
  } else {
    cardButton.classList.remove('disabled');
  }
  
  termsCheckbox.addEventListener("change", function() {
    cardButton.disabled = !this.checked;
    
    if (this.checked) {
      cardButton.classList.remove('disabled');
      this.parentElement.classList.remove('invalid');
      window.paymentFlowMessageEl.innerText = '';
    } else {
      cardButton.classList.add('disabled');
    }
  });
  
  // Add input event listeners to clear error styling when user types
  const allInputs = document.querySelectorAll('input, textarea');
  allInputs.forEach(input => {
    input.addEventListener('input', function() {
      this.classList.remove('invalid');
      if (this.parentElement.classList.contains('checkbox-container')) {
        this.parentElement.classList.remove('invalid');
      }
      window.paymentFlowMessageEl.innerText = '';
    });
  });
  
  // Add listeners for radio buttons
  const referralRadios = document.getElementsByName('referral');
  referralRadios.forEach(radio => {
    radio.addEventListener('change', function() {
      document.getElementById('radio-wrapper').classList.remove('invalid');
    });
  });
  
  // Prevent form submission if validation fails
  document.getElementById('fast-checkout').addEventListener('submit', function(e) {
    if (!window.validateForm()) {
      e.preventDefault();
    }
  });
});

SquarePaymentFlow();