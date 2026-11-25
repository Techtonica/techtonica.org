
// Sample applicant data used to populate the admin dashboard.
// This will eventually be replaced with data retrieved from the database.



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

// Available application statuses used to populate the status dropdown.
const statuses = [
  "All",
  "Eligible",
  "Ineligible",
  "Pending",
  "Manual Review Needed",
];

// Wait until the HTML document has finished loading before accessing its elements.
document.addEventListener("DOMContentLoaded", () => {
  // Retrieve the search field, filter controls, applicant table, and result counter.
  const searchInput = document.getElementById("applicant-search");
  const statusFilter = document.getElementById("status-filter");
  // const missingReferences = document.getElementById("missing-references");
  // const incompleteChallenge = document.getElementById("incomplete-challenge");
  const tableBody = document.getElementById("applicant-table-body");
  const resultCount = document.getElementById("applicant-count");

  // Stop execution if the required dashboard elements are not present.
  if (!searchInput || !statusFilter || !tableBody) {
    return;
  }

  // Populate the status dropdown using the available statuses array.
  statuses.forEach((status) => {
    const option = document.createElement("option");
    option.value = status;
    option.textContent = status;
    statusFilter.appendChild(option);
  });

  // Escape data before inserting it into HTML to prevent HTML injection.
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
      const matchesName = applicant.name
        .toLowerCase()
        .includes(searchTerm);
      const matchesEmail = applicant.email.toLowerCase().includes(searchTerm);
      const matchesSearch = matchesName || matchesEmail;

      const matchesStatus =
        selectedStatus === "All" ||
        applicant.status === selectedStatus;
// filter by two references
      // const matchesReferences =
      //   !missingReferences ||
      //   !missingReferences.checked ||
      //   !applicant.details.two_references;

// filter by freeCodeCamp challenge completion 
      // const matchesChallenge =
      //   !incompleteChallenge ||
      //   !incompleteChallenge.checked ||
      //   !applicant.details.freecodecamp_complete;

      return (
        matchesSearch &&
        matchesStatus 
        // matchesReferences &&
        // matchesChallenge
      );
    });

    tableBody.innerHTML = filteredApplicants
      .map(
        (applicant) => `
          <tr>
            <td>${escapeHTML(applicant.name)}</td>
            <td>${escapeHTML(applicant.eligibility_score)}</td>
        <td>
  <button
    class="admin-button details-button"
    type="button"
    aria-label="View details for ${escapeHTML(applicant.name)}"
  >
    View Details
    <span aria-hidden="true">⌄</span>
  </button>
</td>
<td>
  <button
    class="admin-button edit-button"
    type="button"
    aria-label="Edit ${escapeHTML(applicant.name)}"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path d="M12 20h9" />
      <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4Z" />
    </svg>
    Edit
  </button>
</td>
          </tr>
        `
      )
      .join("");

    if (filteredApplicants.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="4">No applicants found.</td>
        </tr>
      `;
    }

    if (resultCount) {
      resultCount.textContent =
        `${filteredApplicants.length} applicant(s) found`;
    }
  }

  // Update the table when search or filter values change.
  searchInput.addEventListener("input", renderApplicants);
  statusFilter.addEventListener("change", renderApplicants);

  // if (missingReferences) {
  //   missingReferences.addEventListener("change", renderApplicants);
  // }

  // if (incompleteChallenge) {
  //   incompleteChallenge.addEventListener("change", renderApplicants);
  // }

  // Display all applicants when the page first loads.
  renderApplicants();
});
