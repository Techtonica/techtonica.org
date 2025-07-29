document.addEventListener("DOMContentLoaded", function () {
  // handle "Learn More" toggle functionality
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

  // handle form validation
  const form = document.getElementById("app-form-5");
  const nextButton = document.querySelector(".continue-to-app-btn");

  nextButton.addEventListener("click", () => {
    const requiredInputs = form.querySelectorAll("input[required]");
    let isValid = true;

    requiredInputs.forEach((input) => {
      input.style.border = "";
      if (!input.value.trim()) {
        isValid = false;
        input.style.border = "2px solid red";
      }
    });

    if (!isValid) {
      alert("Please fill out all required fields.");
    } else {
      window.location.href = "/app-form-admin";
    }
  });
});