document.addEventListener("DOMContentLoaded", function () {
  window.onload = function () {
    attachLiveValidation("app-form-2", "/app-questionnaire");
  };

  function greaterThanZero(input) {
    if (input.value <= 0) {
      input.setCustomValidity("Please enter a number greater than 0.");
    } else {
      input.setCustomValidity("");
    }
    input.reportValidity();
  }

  function greaterThan25000(input) {
    if (input.value <= 25000) {
      input.setCustomValidity(
        "Please enter a number greater than or equal to 25000.",
      );
    } else {
      input.setCustomValidity("");
    }
    input.reportValidity();
  }

  function inputIsWholeNumber(input) {
    if (!Number.isInteger(Number(input.value))) {
      input.setCustomValidity("Please enter a whole number.");
    } else {
      input.setCustomValidity("");
    }
    input.reportValidity();
  }

  window.greaterThanZero = greaterThanZero;
  window.greaterThan25000 = greaterThan25000;
  window.inputIsWholeNumber = inputIsWholeNumber;

  const usBankRadios = document.querySelectorAll(
    'input[name="US-bank-account"]',
  );

  usBankRadios.forEach((radio) => {
    radio.addEventListener("change", function () {
      const radioWrapper = document.getElementById("radio-wrapper");
      radioWrapper.style.border = "";
    });
  });
});
