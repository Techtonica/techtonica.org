// Form validation and interaction logic for application form
document.addEventListener("DOMContentLoaded", function () {
  // Gender identity custom input toggle
  document
    .getElementById("gender-identity")
    ?.addEventListener("change", function () {
      const customGenderInput = document.getElementById("custom-gender");

      if (this.value === "Other") {
        customGenderInput.style.display = "block";
        customGenderInput.removeAttribute("disabled");
        this.removeAttribute("name");
        customGenderInput.setAttribute("name", "gender-identity");
      } else {
        customGenderInput.style.display = "none";
        customGenderInput.setAttribute("disabled", "true");
        customGenderInput.removeAttribute("name");
        this.setAttribute("name", "gender-identity");
      }
    });

  // Pronouns custom input toggle
  const pronounsCheckboxes = document.querySelectorAll(
    "input[name='pronouns']",
  );
  const customPronounsInput = document.getElementById("custom-pronouns");
  pronounsCheckboxes?.forEach((checkbox) => {
    checkbox.addEventListener("change", () => {
      if (document.getElementById("pronouns-other").checked) {
        customPronounsInput.style.display = "block";
        customPronounsInput.removeAttribute("disabled");
        customPronounsInput.setAttribute("name", "pronouns");
      } else {
        customPronounsInput.style.display = "none";
        customPronounsInput.setAttribute("disabled", "true");
        customPronounsInput.removeAttribute("name");
      }
    });
  });

  // Race/ethnicity custom input toggle
  document
    .getElementById("race-ethnicity")
    ?.addEventListener("change", function () {
      const customRaceEthnicityInput = document.getElementById(
        "custom-race-ethnicity",
      );

      if (this.value === "Other") {
        customRaceEthnicityInput.style.display = "block";
        customRaceEthnicityInput.removeAttribute("disabled");
        this.removeAttribute("name");
        customRaceEthnicityInput.setAttribute("name", "custom-race-ethnicity");
      } else {
        customRaceEthnicityInput.style.display = "none";
        customRaceEthnicityInput.setAttribute("disabled", "true");
        customRaceEthnicityInput.removeAttribute("name");
        this.setAttribute("name", "custom-race-ethnicity");
      }
    });

  // Learn more expandable sections
  const learnMoreWrappers = document.querySelectorAll(".learn-more-wrapper");

  learnMoreWrappers?.forEach((wrapper) => {
    const title = wrapper.querySelector(".learn-more-title");
    const content = wrapper.querySelector(".learn-more-content");
    const toggleIcon = wrapper.querySelector(".toggle-icon");

    toggleIcon.style.cursor = "pointer";

    toggleIcon.querySelector(".toggle-icon-plus").style.display = "inline";
    toggleIcon.querySelector(".toggle-icon-minus").style.display = "none";
    content.style.display = "none";

    let isExpanded = false;

    title.addEventListener("click", () => {
      if (!isExpanded) {
        content.style.display = "block";
        toggleIcon.querySelector(".toggle-icon-plus").style.display = "none";
        toggleIcon.querySelector(".toggle-icon-minus").style.display = "inline";
        title.setAttribute("aria-expanded", true);
      } else {
        content.style.display = "none";
        toggleIcon.querySelector(".toggle-icon-plus").style.display = "inline";
        toggleIcon.querySelector(".toggle-icon-minus").style.display = "none";
        title.setAttribute("aria-expanded", false);
      }

      isExpanded = !isExpanded;
    });
  });
});

function navigateToPage(pageToNavigateTo) {
  window.location.href = pageToNavigateTo;
}

// Form validation function if not using live validation
function validateAppForm(elementId, nextUrl) {
  // const form = document.getElementById("app-form-1");
  const form = document.getElementById(elementId);
  const requiredFields = form.querySelectorAll("[required]");
  let allValid = true;

  requiredFields.forEach((field) => {
    const parentElement = field.parentNode;
    parentElement.style.border = "";
    field.style.border = "";

    const tag = field.tagName.toUpperCase();

    if (field.type === "radio" || field.type === "checkbox") {
      const isChecked = form.querySelector(`[name="${field.name}"]:checked`);
      if (!isChecked) {
        allValid = false;
        parentElement.style.border = "2px solid red";
      }
    } else if (tag === "SELECT") {
      if (field.value === "") {
        allValid = false;
        field.style.border = "2px solid red";
      }
    } else if (
      field.type === "text" ||
      field.type === "email" ||
      field.type === "tel" ||
      field.type === "number" ||
      tag === "TEXTAREA"
    ) {
      if (!field.value.trim()) {
        allValid = false;
        field.style.border = "2px solid red";
      }
    }
  });

  if (!allValid) {
    alert("Please fill out the missing field(s).");
  } else {
    window.location.href = nextUrl;
  }
}

// Function to attach event listeners for live validation
function attachLiveValidation(elementId, nextUrl, clear = false) {
  const form = document.getElementById(elementId);
  const fields = form.querySelectorAll("[required]");
  fields.forEach((field) => {
    field.addEventListener("input", () => validateField(field)); // Text inputs
    field.addEventListener("change", () => validateField(field)); // Dropdowns, radio buttons, file uploads
  });

  const submitButton = document.querySelector(".continue-to-app-btn");
  if (submitButton) {
    submitButton.addEventListener("click", function (event) {
      event.preventDefault();
      validateAndSubmit(elementId, nextUrl, clear);
    });
  }
}

// Function to validate individual fields
function validateField(field) {
  const validationType = field.dataset.validation || field.type; // Field type based on custom input data-validation="" or the type listed

  if (validateFieldByType(field, validationType)) {
    clearValidation(field); // Clear red border and error message if valid
  } else {
    markInvalid(field); // Highlight with red border and show error message if invalid
  }
}

// Function to validate fields by type
function validateFieldByType(field, validationType) {
  switch (validationType) {
    case "url":
      return isValidURL(field.value); // Validate URL format
    case "radio":
      return isRadioGroupValid(field.name); // Validate radio group selection
    case "checkbox":
      return isRadioGroupValid(field.name); // Validate radio group selection
    case "file":
      return field.files.length > 0; // Ensure file is uploaded
    default:
      return field.value.trim() !== ""; // Ensure field is not empty
  }
}

// Validation helpers
function isValidURL(value) {
  const urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i; // Regex to check URL formatting
  return urlPattern.test(value);
}

function isRadioGroupValid(name) {
  const radios = document.getElementsByName(name);
  return Array.from(radios).some((radio) => radio.checked); // Collects radio buttons in group and checks if at least one is selected
}

// Handle invalid fields
function markInvalid(field) {
  let errorMessageText = "This field is required."; // Default error message

  if (field.type === "url") {
    errorMessageText = "A valid URL is required.";
  } else if (field.type === "radio") {
    errorMessageText = "Please select an option.";
  } else if (field.type === "file") {
    errorMessageText = "Please upload a file.";
  }

  if (field.type === "radio") {
    // Append the error message only once for the radio group container
    const radioGroup = field.closest('[role="radiogroup"]');
    if (!radioGroup.querySelector(".error-message")) {
      const errorMessage = document.createElement("span");
      errorMessage.className = "error-message";
      errorMessage.style.color = "red";
      errorMessage.innerText = errorMessageText;
      radioGroup.insertBefore(errorMessage, radioGroup.firstChild); // Append message to radio group container instead of to each radio button
    }
    // Highlight each radio button in the group
    const radioButtons = radioGroup.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
      radio.style.outline = "2px solid red"; // Add a red outline to the radio buttons
      radio.style.outlineOffset = "2px"; // Optional: Add some spacing around the outline
    });
  } else {
    // For other field types
    let parent = field.parentElement;
    if (!parent) {
      console.error("Parent element not found");
      return;
    }
    let errorMessage = parent.querySelector(".error-message");
    if (!errorMessage) {
      // Create error message element
      errorMessage = document.createElement("span");
      errorMessage.className = "error-message";
      errorMessage.style.color = "red";
      errorMessage.innerText = errorMessageText;

      // Insert error message before the field
      parent.insertBefore(errorMessage, field);
    }
    field.style.border = "2px solid red";
  }
}

// Clear invalid styling and error message
function clearValidation(field) {
  if (field.type === "radio") {
    const radioGroup = field.closest('[role="radiogroup"]');
    const errorMessage = radioGroup.querySelector(".error-message");
    if (errorMessage) {
      errorMessage.remove(); // Remove radio group error message
    }
    // Remove red outline from each radio button in the group
    const radioButtons = radioGroup.querySelectorAll('input[type="radio"]');
    radioButtons.forEach((radio) => {
      radio.style.outline = ""; // Clear the red outline
      radio.style.outlineOffset = ""; // Clear the spacing
    });
  } else {
    // Handle other input types
    const parent = field.parentElement;
    const errorMessage = parent.querySelector(".error-message"); // Check for error message above the field
    if (errorMessage) {
      errorMessage.remove(); // Remove error message
    }
    field.style.border = ""; // Remove red border for valid inputs
  }
}

// Final validation before navigation
function validateAndSubmit(elementId, nextUrl) {
  const form = document.getElementById(elementId);
  const fields = form.querySelectorAll("[required]");
  let isValid = true;

  fields.forEach((field) => {
    if (!validateFieldByType(field, field.dataset.validation || field.type)) {
      markInvalid(field); // Highlight invalid fields
      isValid = false; // Set flag to false if any field is invalid
    }
  });

  if (isValid) {
    if (!nextUrl) {
      // Code is setup to clear localStorage on submit, not to submit the form
      clearLocal(elementId);
    } else {
      window.location.href = nextUrl;
    }
  } else {
    alert("Please complete all required fields.");
  }
}

function clearLocal(elementId) {
  localStorage.clear();
  // Reset all form fields
  const form = document.getElementById(elementId);
  form.reset(); // Resets form fields to their initial state
}
