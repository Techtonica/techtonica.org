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

// Function to check text for profanity using PurgoMalum API
window.checkProfanity = async function(text) {
  if (!text || text.trim() === '') return { containsProfanity: false };
  
  try {
    // Encode the text for URL
    const encodedText = encodeURIComponent(text);
    // Use PurgoMalum's containsprofanity endpoint
    const response = await fetch(`https://www.purgomalum.com/service/containsprofanity?text=${encodedText}`);
    const result = await response.text();
    
    return { 
      containsProfanity: result.trim() === 'true',
      text: text
    };
  } catch (error) {
    console.error('Error checking profanity:', error);
    // If the API fails, we'll let the text pass to not block users
    return { containsProfanity: false };
  }
}

// Validate form fields
window.validateForm = async function() {
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
  
  // Check if code of conduct checkbox is checked
  const conductCheckbox = document.getElementById('code-of-conduct-checkbox');
  if (!conductCheckbox.checked) {
    conductCheckbox.parentElement.classList.add('invalid');
    isValid = false;
    // Make the checkbox a priority for focus if it's not checked
    firstInvalidField = conductCheckbox;
  } else {
    conductCheckbox.parentElement.classList.remove('invalid');
  }
  
  // Check for profanity in text fields
  const textFieldsToCheck = [
    { id: 'jobtitle', label: 'Job Title' },
    { id: 'company', label: 'Company' },
    { id: 'type', label: 'Type' },
    { id: 'educationreq', label: 'Education Requirement' },
    { id: 'location', label: 'Location' },
    { id: 'salaryrange', label: 'Salary Range' },
    { id: 'description', label: 'Description' },
    { id: 'applicationlink', label: 'Application Link' }
  ];
  
  // Show loading message while checking profanity
  if (isValid) {
    window.showError('Checking content for inappropriate language...');
  }
  
  // Check each field for profanity
  for (const field of textFieldsToCheck) {
    const element = document.getElementById(field.id);
    const text = element.value.trim();
    
    if (text) {
      const profanityCheck = await window.checkProfanity(text);
      
      if (profanityCheck.containsProfanity) {
        element.classList.add('invalid');
        isValid = false;
        if (!firstInvalidField) firstInvalidField = element;
        window.showError(`Inappropriate language detected in ${field.label}. Please revise your content.`);
        break; // Stop checking after first profanity found
      }
    }
  }
  
  // Scroll to first invalid field if validation fails
  if (!isValid && firstInvalidField) {
    firstInvalidField.focus();
    if (!window.paymentFlowMessageEl.innerText.includes('Inappropriate language')) {
      window.showError('Please fill in all required fields and accept the Code of Conduct.');
    }
  } else if (isValid) {
    // Clear the "checking content" message if everything is valid
    window.paymentFlowMessageEl.innerText = '';
  }
  
  return isValid;
}

window.createPayment = async function(token) {
  // Show loading message
  window.showError('Validating form...');
  
  // Validate form before processing payment
  const isValid = await window.validateForm();
  if (!isValid) {
    return;
  }
  
  // Show processing message
  window.showError('Processing payment...');
  
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

// Form and checkbox functionality
document.addEventListener("DOMContentLoaded", () => {
  const termsCheckbox = document.getElementById("code-of-conduct-checkbox");
  const cardButton = document.getElementById("card-button");
  
  // Set initial button state
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
  document.getElementById('fast-checkout').addEventListener('submit', async function(e) {
    e.preventDefault(); // Always prevent default to handle validation
    
    // Show loading message
    window.showError('Validating form...');
    
    const isValid = await window.validateForm();
    if (isValid) {
      // If valid, the form will be processed by the payment flow
      window.showError('Form is valid. Please complete payment.');
    }
  });
});

SquarePaymentFlow();