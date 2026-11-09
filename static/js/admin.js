
const applicants = [
  {
    id: 1,
    name: "Jane Doe",
    email: "jane.doe@example.com",
    eligibility_score: 90,
    status: "Eligible",
    date_submitted: "2025-01-15",
    details: {
      wpm_score: 55,
      wpm_accuracy: "85%",
      two_references: true,
      freecodecamp_complete: true,
      gender: "Non-binary",
      computer_literate: "Yes",
      recent_bootcamp: "No",
      stable_housing: "Yes",
    },
    admin_notes: [
      "Follow-up required after interview.",
      "Strong technical background",
      "Needs financial assistance verification",
    ],
  },
  {
    id: 2,
    name: "John Smith",
    email: "john.smith@example.com",
    eligibility_score: 75,
    status: "Eligible",
    date_submitted: "2025-01-12",
    details: {
      wpm_score: 52,
      wpm_accuracy: "82%",
      two_references: true,
      freecodecamp_complete: false,
      gender: "Woman",
      computer_literate: "Yes",
      recent_bootcamp: "No",
      stable_housing: "Yes",
    },
    admin_notes: [
      "Pending reference check.",
      "Good problem-solving skills",
      "Completed take-home challenge successfully",
    ],
  },
  {
    id: 3,
    name: "Alice Johnson",
    email: "alice.johnson@example.com",
    eligibility_score: 45,
    status: "Ineligible",
    date_submitted: "2025-01-10",
    details: {
      wpm_score: 30,
      wpm_accuracy: "70%",
      two_references: false,
      freecodecamp_complete: false,
      gender: "Woman",
      computer_literate: "No",
      recent_bootcamp: "Yes",
      stable_housing: "No",
    },
    admin_notes: [
      "Did not meet eligibility requirements.",
      "Incomplete application",
      "Short-form ineligible criteria flagged",
    ],
  },
  {
    id: 4,
    name: "Bob Williams",
    email: "bob.williams@example.com",
    eligibility_score: 60,
    status: "Pending",
    date_submitted: "2025-01-18",
    details: {
      wpm_score: 50,
      wpm_accuracy: "80%",
      two_references: false,
      freecodecamp_complete: false,
      gender: "Non-binary",
      computer_literate: "Yes",
      recent_bootcamp: "No",
      stable_housing: "Yes",
    },
    admin_notes: [
      "Awaiting staff interview.",
      "Great enthusiasm for program",
      "Awaiting final eligibility review",
    ],
  },
  {
    id: 5,
    name: "Chris Adams",
    email: "chris.adams@example.com",
    eligibility_score: 50,
    status: "Manual Review Needed",
    date_submitted: "2025-01-20",
    details: {
      wpm_score: 49,
      wpm_accuracy: "78%",
      two_references: false,
      freecodecamp_complete: false,
      gender: "Man",
      computer_literate: "Yes",
      recent_bootcamp: "No",
      stable_housing: "Yes",
    },
    admin_notes: [
      "Requires additional financial documents.",
      "Income verification pending",
      "Needs further assessment for eligibility",
    ],
  },
];

const statuses = [
  "All",
  "Eligible",
  "Ineligible",
  "Pending",
  "Manual Review Needed",
];

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("applicant-search");
  const statusFilter = document.getElementById("status-filter");
  const missingReferences = document.getElementById("missing-references");
  const incompleteChallenge = document.getElementById("incomplete-challenge");
  const tableBody = document.getElementById("applicant-table-body");
  const resultCount = document.getElementById("applicant-count");

  if (!searchInput || !statusFilter || !tableBody) {
    return;
  }

  // Populate status choices.
  statuses.forEach((status) => {
    const option = document.createElement("option");
    option.value = status;
    option.textContent = status;
    statusFilter.appendChild(option);
  });

  // Escape data before inserting it into HTML.
  function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, (character) => {
      const entities = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      };
      return entities[character];
    });
  }

  function renderApplicants() {
    const searchTerm = searchInput.value.trim().toLowerCase();
    const selectedStatus = statusFilter.value;

    const filteredApplicants = applicants.filter((applicant) => {
      const matchesSearch =
        applicant.name.toLowerCase().includes(searchTerm) ||
        applicant.email.toLowerCase().includes(searchTerm);

      const matchesStatus =
        selectedStatus === "All" ||
        applicant.status === selectedStatus;

      const matchesReferences =
        !missingReferences.checked ||
        !applicant.details.two_references;

      const matchesChallenge =
        !incompleteChallenge.checked ||
        !applicant.details.freecodecamp_complete;

      return (
        matchesSearch &&
        matchesStatus &&
        matchesReferences &&
        matchesChallenge
      );
    });

    tableBody.innerHTML = filteredApplicants
      .map(
        (applicant) => `
          <tr>
            <td>${escapeHTML(applicant.name)}</td>
            <td>${escapeHTML(applicant.email)}</td>
            <td>
              <span class="applicant-status">
                ${escapeHTML(applicant.status)}
              </span>
            </td>
            <td>${escapeHTML(applicant.eligibility_score)}</td>
            <td>${escapeHTML(applicant.date_submitted)}</td>
            <td>
              ${applicant.details.two_references ? "Complete" : "Missing"}
            </td>
            <td>
              ${applicant.details.freecodecamp_complete ? "Complete" : "Incomplete"}
            </td>
          </tr>
        `
      )
      .join("");

    if (filteredApplicants.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="7">No applicants found.</td>
        </tr>
      `;
    }

    if (resultCount) {
      resultCount.textContent =
        `${filteredApplicants.length} applicant(s) found`;
    }
  }

  searchInput.addEventListener("input", renderApplicants);
  statusFilter.addEventListener("change", renderApplicants);
  missingReferences.addEventListener("change", renderApplicants);
  incompleteChallenge.addEventListener("change", renderApplicants);

  renderApplicants();
});
