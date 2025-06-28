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
});

function validateForm() {
  const form = document.getElementById("app-form-6");
  const requiredFields = form.querySelectorAll("[required]");
  let allValid = true;

  requiredFields.forEach((field) => {
    const parentElement = field.parentNode;
    parentElement.style.border = "";

    if (
      (field.type === "radio" || field.type === "checkbox") &&
      !form.querySelector(`[name="${field.name}"]:checked`)
    ) {
      allValid = false;
      parentElement.style.border = "2px solid red";
    }
  });

  if (!allValid) {
    alert("Please fill out the missing field(s).");
  } else {
    window.location.href = "/app-additional";
  }
}
