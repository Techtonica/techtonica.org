document.addEventListener("DOMContentLoaded", function () {
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
        "Please enter a number greater than or equal to 25000."
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

  window.validateForm = function () {
    const form = document.getElementById("app-form-2");
    const requiredSelects = form.querySelectorAll("input[required]");
    let allValid = true;

    requiredSelects.forEach((select) => {
      select.style.border = "";

      if (select.type === "radio") {
        const group = form.querySelectorAll(`input[name="${select.name}"]`);
        const isChecked = Array.from(group).some((radio) => radio.checked);
        if (!isChecked) {
          allValid = false;
          group.forEach((radio) => {
            radio.parentElement.style.border = "2px solid red";
          });
        }
      } else if (select.value === "") {
        allValid = false;
        select.style.border = "2px solid red";
      }
    });

    if (!allValid) {
      alert("Please select an option for all questions.");
    } else {
      window.location.href = "/app-questionnaire";
    }
  };
});
