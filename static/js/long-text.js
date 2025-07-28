document.addEventListener("DOMContentLoaded", function () {
  const learnMoreWrappers = document.querySelectorAll(".learn-more-wrapper");

  learnMoreWrappers.forEach((wrapper) => {
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

  attachLiveValidation();

  function attachLiveValidation() {
    const form = document.getElementById("app-form-4");
    if (!form) return;
    const fields = form.querySelectorAll("[required]");
    fields.forEach((field) => {
      field.addEventListener("input", () => validateField(field));
      field.addEventListener("change", () => validateField(field));
    });
  }

  function validateField(field) {
    const validationType = field.dataset.validation || field.type;
    if (validateFieldByType(field, validationType)) {
      clearValidation(field);
    } else {
      markInvalid(field);
    }
  }

  function validateFieldByType(field, validationType) {
    switch (validationType) {
      case "url":
        return isValidURL(field.value);
      case "radio":
        return isRadioGroupValid(field.name);
      default:
        return field.value.trim() !== "";
    }
  }

  function isValidURL(value) {
    const urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
    return urlPattern.test(value);
  }

  function isRadioGroupValid(name) {
    const radios = document.getElementsByName(name);
    return Array.from(radios).some((radio) => radio.checked);
  }

  function markInvalid(field) {
    let errorMessageText = "This field is required.";

    if (field.type === "url") {
      errorMessageText = "A valid URL is required.";
    } else if (field.type === "radio") {
      errorMessageText = "Please select an option.";
    }

    if (field.type === "radio") {
      const radioGroup = field.closest('[role="radiogroup"]');
      if (!radioGroup.querySelector(".error-message")) {
        const errorMessage = document.createElement("span");
        errorMessage.className = "error-message";
        errorMessage.style.color = "red";
        errorMessage.innerText = errorMessageText;
        radioGroup.insertBefore(errorMessage, radioGroup.firstChild);
      }

      const radioButtons = radioGroup.querySelectorAll('input[type="radio"]');
      radioButtons.forEach((radio) => {
        radio.style.outline = "2px solid red";
        radio.style.outlineOffset = "2px";
      });
    } else {
      let parent = field.parentElement;
      if (!parent) {
        console.error("Parent element not found");
        return;
      }
      let errorMessage = parent.querySelector(".error-message");
      if (!errorMessage) {
        errorMessage = document.createElement("span");
        errorMessage.className = "error-message";
        errorMessage.style.color = "red";
        errorMessage.innerText = errorMessageText;
        parent.insertBefore(errorMessage, field);
      }
      field.style.border = "2px solid red";
    }
  }

  function clearValidation(field) {
    if (field.type === "radio") {
      const radioGroup = field.closest('[role="radiogroup"]');
      const errorMessage = radioGroup.querySelector(".error-message");
      if (errorMessage) {
        errorMessage.remove();
      }
      const radioButtons = radioGroup.querySelectorAll('input[type="radio"]');
      radioButtons.forEach((radio) => {
        radio.style.outline = "";
        radio.style.outlineOffset = "";
      });
    } else {
      const parent = field.parentElement;
      const errorMessage = parent.querySelector(".error-message");
      if (errorMessage) {
        errorMessage.remove();
      }
      field.style.border = "";
    }
  }

  window.validateAndNavigate = function (nextPage) {
    const form = document.getElementById("app-form-4");
    const fields = form.querySelectorAll("[required]");
    let isValid = true;

    fields.forEach((field) => {
      if (!validateFieldByType(field, field.dataset.validation || field.type)) {
        markInvalid(field);
        isValid = false;
      }
    });

    if (isValid) {
      window.location.href = nextPage;
    } else {
      alert("Please complete all required fields.");
    }
  };

  window.navigateToPage = function (previousPage) {
    window.location.href = previousPage;
  };
});
