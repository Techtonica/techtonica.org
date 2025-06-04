// Form validation and interaction logic for application form
document.addEventListener('DOMContentLoaded', function () {
  // Gender identity custom input toggle
  document
    .getElementById("gender-identity")
    .addEventListener("change", function () {
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
  pronounsCheckboxes.forEach((checkbox) => {
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
    .addEventListener("change", function () {
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
        toggleIcon.querySelector(".toggle-icon-minus").style.display =
          "inline";
        title.setAttribute("aria-expanded", true);
      } else {
        content.style.display = "none";
        toggleIcon.querySelector(".toggle-icon-plus").style.display =
          "inline";
        toggleIcon.querySelector(".toggle-icon-minus").style.display = "none";
        title.setAttribute("aria-expanded", false);
      }

      isExpanded = !isExpanded;
    });
  });
});

// Form validation function
function validateForm() {
  const form = document.getElementById("app-form-1");
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
    window.location.href = "/household";
  }
} 