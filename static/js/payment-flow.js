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

// Function to display success page after payment
window.showSuccessPage = function(jobTitle, company) {
  // Get the form container
  const formContainer = document.getElementById('fast-checkout');
  
  // Create success content
  const successContent = document.createElement('div');
  successContent.className = 'success-container';
  successContent.innerHTML = `
    <div class="success-icon">✓</div>
    <h2>Payment Successful!</h2>
    <p>Thank you for submitting your job posting for "${jobTitle}" at "${company}".</p>
    <p>Your job posting has been sent to our staff for review and will be shared with our graduates after approval.</p>
    <p>If you have any questions, please contact us at <a href="mailto:info@techtonica.org">info@techtonica.org</a>.</p>
    <button id="post-another-job" class="sponsor">
      <h2>Post Another Job</h2>
    </button>
  `;
  
  // Clear the form container and append success content
  formContainer.innerHTML = '';
  formContainer.appendChild(successContent);
  
  // Add event listener to "Post Another Job" button
  document.getElementById('post-another-job').addEventListener('click', function() {
    // Reload the page to start fresh
    window.location.reload();
  });
  
  // Scroll to top of success message
  window.scrollTo({
    top: formContainer.offsetTop - 100,
    behavior: 'smooth'
  });
}

// Function to check text for profanity using PurgoMalum API with improved word boundary handling
window.checkProfanity = async function(text) {
  if (!text || text.trim() === '') return { containsProfanity: false };
  
  try {
    // Split the text into words to check them individually
    // This helps avoid false positives in names like "Harshitha"
    const words = text.split(/\s+/);
    
    // Check each word individually
    for (const word of words) {
      // Skip very short words (likely not profanity)
      if (word.length <= 2) continue;
      
      // Skip words that look like they might be names (first letter capitalized)
      // This is a simple heuristic to reduce false positives on names
      if (/^[A-Z][a-z]+$/.test(word)) continue;
      
      // Encode the word for URL
      const encodedWord = encodeURIComponent(word);
      
      // Use PurgoMalum's containsprofanity endpoint for this specific word
      const response = await fetch(`https://www.purgomalum.com/service/containsprofanity?text=${encodedWord}`);
      const result = await response.text();
      
      if (result.trim() === 'true') {
        return { 
          containsProfanity: true,
          text: word // Return the specific word that was flagged
        };
      }
    }
    
    // If we get here, no individual word was flagged
    return { containsProfanity: false };
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
  
  // If basic validation fails, return early before checking profanity
  if (!isValid) {
    if (firstInvalidField) {
      firstInvalidField.focus();
      window.showError('Please fill in all required fields and accept the Code of Conduct.');
    }
    return false;
  }
  
  // Show loading message while checking profanity
  window.showError('Checking content for inappropriate language...');
  
  // Get all text inputs and textareas in the form
  const form = document.getElementById('fast-checkout');
  const textInputs = form.querySelectorAll('input[type="text"], input[type="email"], textarea');
  
  // Create a mapping of field IDs to readable labels
  const fieldLabels = {
    'firstname': 'First Name',
    'lastname': 'Last Name',
    'email': 'Email',
    'jobtitle': 'Job Title',
    'company': 'Company',
    'type': 'Type',
    'educationreq': 'Education Requirement',
    'location': 'Location',
    'salaryrange': 'Salary Range',
    'description': 'Description',
    'applicationlink': 'Application Link'
  };
  
  // Check each text field for profanity
  for (const input of textInputs) {
    const text = input.value.trim();
    
    if (text) {
      const profanityCheck = await window.checkProfanity(text);
      
      if (profanityCheck.containsProfanity) {
        input.classList.add('invalid');
        isValid = false;
        if (!firstInvalidField) firstInvalidField = input;
        
        // Get a readable label for the field
        const fieldLabel = fieldLabels[input.id] || input.id;
        window.showError(`Potentially inappropriate word "${profanityCheck.text}" detected in ${fieldLabel}. Please revise your content.`);
        break; // Stop checking after first profanity found
      }
    }
  }
  
  // If profanity was found, focus the first invalid field
  if (!isValid && firstInvalidField) {
    firstInvalidField.focus();
    return false;
  }
  
  // Clear the "checking content" message if everything is valid
  window.paymentFlowMessageEl.innerText = '';
  return true;
}

window.createPayment = async function(token) {
  // If we have a token, the card info must be complete
  // No need to check window.cardInfoComplete here
  
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
      // Get job title and company for the success message
      const jobTitle = document.getElementById('jobtitle').value;
      const company = document.getElementById('company').value;
      
      // Send notification to Slack
      await window.sendSlackNotification();
      
      // Show success page (this replaces the form)
      window.showSuccessPage(jobTitle, company);
    }
  } catch (error) {
    console.error('Error:', error);
    window.showError('An error occurred while processing your payment.');
  }
}

window.sendSlackNotification = async () => {
  var referralValue = "no"

  document.getElementsByName("referral").forEach((radio) => {
    if (radio.checked) {
      referralValue = radio.value
    }
  })

  var notificationValues = {
    firstName: document.getElementById("firstname").value,
    lastName: document.getElementById("lastname").value,
    email: document.getElementById("email").value,
    jobTitle: document.getElementById("jobtitle").value,
    company: document.getElementById("company").value,
    type: document.getElementById("type").value,
    educationReq: document.getElementById("educationreq").value,
    location: document.getElementById("location").value,
    referral: referralValue,
    salaryRange: document.getElementById("salaryrange").value,
    description: document.getElementById("description").value,
    applicationLink: document.getElementById("applicationlink").value,
  }

  var dataJsonString = JSON.stringify(notificationValues)

  try {
    // Use the process-job-posting.js endpoint
    const response = await fetch("/process-job-posting", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: dataJsonString,
    })

    const data = await response.json()

    if (!data.success) {
      console.error("Error sending job posting:", data.error)
      return false
    }

    console.log("Job posting sent for approval:", data.postingId || "Unknown ID")
    return true
  } catch (error) {
    console.error("Error:", error)
    return false
  }
}

// Form and code of conduct checkbox functionality
document.addEventListener("DOMContentLoaded", () => {
  // Initialize the cardInfoComplete flag
  window.cardInfoComplete = false;
  
  const termsCheckbox = document.getElementById("code-of-conduct-checkbox");
  const cardButton = document.getElementById("card-button");
  const cardContainer = document.getElementById('card-container');
  
  // Set initial button state
  cardButton.disabled = !termsCheckbox.checked;
  
  // Visual indicator for disabled state
  if (cardButton.disabled) {
    cardButton.classList.add('disabled');
  } else {
    cardButton.classList.remove('disabled');
  }
  
  // Add visual indicator for card container
  if (cardContainer) {
    // Add a subtle border that changes color when card info is complete
    cardContainer.style.transition = 'border-color 0.3s ease';
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
  
  // Input event listeners to clear error styling when user types
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
    
    // First validate the form fields
    const isFormValid = await window.validateForm();
    if (!isFormValid) {
      return;
    }
    
    // If form is valid, let the card button handle the payment
    // This will trigger the eventHandler in sq-card-pay.js
    document.getElementById('card-button').click();
  });
});

SquarePaymentFlow();