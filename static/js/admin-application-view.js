/**
 * Individual Application Review, Edit, Admin-Only Notes, and Applicant Messaging
 * for the Techtonica Admin Dashboard (Issue #579).
 */

const DEFAULT_APPLICANTS = [
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

/**
 * Escapes user-provided strings before inserting into HTML to prevent XSS.
 */
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    };
    return entities[char];
  });
}

/**
 * Formats a Date instance into a readable timestamp string (YYYY-MM-DD HH:MM:SS).
 */
function formatTimestamp(dateInput) {
  const date = dateInput instanceof Date ? dateInput : new Date();
  const pad = (num) => String(num).padStart(2, "0");
  const year = date.getFullYear();
  const month = pad(date.getMonth() + 1);
  const day = pad(date.getDate());
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

/**
 * Parses percentage strings such as "85%" into a numeric value (85).
 */
function parsePercentage(value) {
  if (typeof value === "number") {
    return value;
  }
  const cleaned = String(value ?? "")
    .replace("%", "")
    .trim();
  const parsed = Number.parseFloat(cleaned);
  return Number.isNaN(parsed) ? 0 : parsed;
}

/**
 * Evaluates all 8 eligibility criteria for an applicant's details object.
 * Returns an array of criterion descriptors with status:
 * - "met" (green checkmark)
 * - "ineligible" (red "x")
 * - "manual_review" (yellow warning icon)
 */
function evaluateEligibilityCriteria(details) {
  const safeDetails = details || {};

  // 1. WPM Score (eligibility is 50+)
  const wpmScoreNum = Number(safeDetails.wpm_score);
  const wpmScoreMet = !Number.isNaN(wpmScoreNum) && wpmScoreNum >= 50;

  // 2. WPM Accuracy (eligibility is 80%+)
  const accuracyNum = parsePercentage(safeDetails.wpm_accuracy);
  const wpmAccuracyMet = accuracyNum >= 80;
  const accuracyDisplay = String(safeDetails.wpm_accuracy ?? "").includes("%")
    ? String(safeDetails.wpm_accuracy)
    : `${accuracyNum}%`;

  // 3. Two References (eligibility is both references details are all submitted)
  const twoRefsMet =
    safeDetails.two_references === true ||
    String(safeDetails.two_references).toLowerCase() === "true" ||
    String(safeDetails.two_references).toLowerCase() === "yes";
  const twoRefsDisplay = twoRefsMet ? "Yes" : "No";

  // 4. FreeCodeCamp Complete (warning icon, needs to be manually changed by admin user,
  //    eligibility is the complete single screenshot of all 115 problems)
  let fccStatus = "manual_review";
  let fccDisplay = "Needs Manual Review (115 problems)";
  if (
    safeDetails.freecodecamp_complete === true ||
    String(safeDetails.freecodecamp_complete).toLowerCase() === "true" ||
    String(safeDetails.freecodecamp_complete).toLowerCase() === "yes"
  ) {
    fccStatus = "met";
    fccDisplay = "Yes (115/115 Confirmed)";
  } else if (
    String(safeDetails.freecodecamp_complete).toLowerCase() === "ineligible" ||
    String(safeDetails.freecodecamp_complete).toLowerCase() === "rejected"
  ) {
    fccStatus = "ineligible";
    fccDisplay = "No (Ineligible)";
  }

  // 5. Gender (eligibility is not cis-male)
  const genderRaw = String(safeDetails.gender ?? "").trim();
  const genderNormalized = genderRaw.toLowerCase();
  const ineligibleGenders = [
    "cis-male",
    "cis male",
    "cismale",
    "cisgender male",
    "cisgender man",
    "man",
    "male",
  ];
  const genderMet =
    genderNormalized.length > 0 &&
    !ineligibleGenders.includes(genderNormalized);

  // 6. Computer literate (eligibility is yes)
  const computerLiterateMet =
    String(safeDetails.computer_literate ?? "").toLowerCase() === "yes" ||
    safeDetails.computer_literate === true;
  const computerLiterateDisplay = computerLiterateMet ? "Yes" : "No";

  // 7. Recent bootcamp (eligibility is no)
  const recentBootcampMet =
    String(safeDetails.recent_bootcamp ?? "").toLowerCase() === "no" ||
    safeDetails.recent_bootcamp === false;
  const recentBootcampDisplay = recentBootcampMet ? "No" : "Yes";

  // 8. Stable housing (eligibility is yes)
  const stableHousingMet =
    String(safeDetails.stable_housing ?? "").toLowerCase() === "yes" ||
    safeDetails.stable_housing === true;
  const stableHousingDisplay = stableHousingMet ? "Yes" : "No";

  return [
    {
      key: "wpm_score",
      label: "WPM Score",
      value: String(safeDetails.wpm_score ?? ""),
      status: wpmScoreMet ? "met" : "ineligible",
      rule: "50+ WPM required",
    },
    {
      key: "wpm_accuracy",
      label: "WPM Accuracy",
      value: accuracyDisplay,
      status: wpmAccuracyMet ? "met" : "ineligible",
      rule: "80%+ accuracy required",
    },
    {
      key: "two_references",
      label: "Two References",
      value: twoRefsDisplay,
      status: twoRefsMet ? "met" : "ineligible",
      rule: "Both references submitted",
    },
    {
      key: "freecodecamp_complete",
      label: "FreeCodeCamp Complete",
      value: fccDisplay,
      status: fccStatus,
      rule: "Complete single screenshot of all 115 problems (manual admin confirmation)",
      requiresManualConfirmation: true,
    },
    {
      key: "gender",
      label: "Gender",
      value: genderRaw,
      status: genderMet ? "met" : "ineligible",
      rule: "Not cis-male",
    },
    {
      key: "computer_literate",
      label: "Computer Literate",
      value: computerLiterateDisplay,
      status: computerLiterateMet ? "met" : "ineligible",
      rule: "Must be Yes",
    },
    {
      key: "recent_bootcamp",
      label: "Recent Bootcamp",
      value: recentBootcampDisplay,
      status: recentBootcampMet ? "met" : "ineligible",
      rule: "Must be No",
    },
    {
      key: "stable_housing",
      label: "Stable Housing",
      value: stableHousingDisplay,
      status: stableHousingMet ? "met" : "ineligible",
      rule: "Must be Yes",
    },
  ];
}

/**
 * Returns the visual SVG icon for a criterion status ("met", "ineligible", "manual_review").
 */
function renderCriterionIcon(status) {
  if (status === "met") {
    return `
      <span class="criteria-icon criteria-met" title="Eligible / Criteria Met" aria-label="Criteria met">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <circle cx="12" cy="12" r="10" stroke="#2e7d32" stroke-width="2" fill="#e8f5e9"></circle>
          <path d="M8 12.5L10.8 15.3L16.5 9.5" stroke="#2e7d32" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"></path>
        </svg>
      </span>
    `;
  }
  if (status === "manual_review") {
    return `
      <span class="criteria-icon criteria-warning" title="Manual Review Required" aria-label="Requires manual review">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M12 3L22 20H2L12 3Z" stroke="#b45309" stroke-width="2" stroke-linejoin="round" fill="#fef3c7"></path>
          <path d="M12 9V13.5" stroke="#b45309" stroke-width="2.2" stroke-linecap="round"></path>
          <circle cx="12" cy="17" r="1.2" fill="#b45309"></circle>
        </svg>
      </span>
    `;
  }
  return `
    <span class="criteria-icon criteria-ineligible" title="Ineligible / Criteria Not Met" aria-label="Ineligible">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <circle cx="12" cy="12" r="10" stroke="#c62828" stroke-width="2" fill="#ffebee"></circle>
        <path d="M15 9L9 15M9 9L15 15" stroke="#c62828" stroke-width="2.2" stroke-linecap="round"></path>
      </svg>
    </span>
  `;
}

/**
 * Builds a timestamped admin note when FreeCodeCamp Complete (115 problems screenshot)
 * is manually confirmed or updated by an Admin User or Program Staff.
 */
function buildFccConfirmationNote(isConfirmed, role, dateInput) {
  const timestamp = formatTimestamp(dateInput);
  const reviewerRole = role || "Admin User";
  const statusLabel = isConfirmed
    ? "Confirmed complete single screenshot of all 115 problems"
    : "Marked as pending manual review for 115 problems screenshot";
  return `[${timestamp}] FreeCodeCamp Complete manually updated by ${reviewerRole}: ${statusLabel}.`;
}

/**
 * Compares previous and updated applicant data and builds a timestamped admin note
 * detailing which application fields were changed.
 */
function buildFieldChangeNote(changes, role, dateInput) {
  if (!Array.isArray(changes) || changes.length === 0) {
    return null;
  }
  const timestamp = formatTimestamp(dateInput);
  const reviewerRole = role || "Admin User";
  const summary = changes
    .map((change) => `${change.label} (${change.from} -> ${change.to})`)
    .join(", ");
  return `[${timestamp}] Application edited by ${reviewerRole} - Changed fields: ${summary}.`;
}

/**
 * Builds a timestamped admin-only note entry.
 */
function buildAdminNoteEntry(noteText, role, dateInput) {
  const timestamp = formatTimestamp(dateInput);
  const reviewerRole = role || "Admin User";
  return `[${timestamp}] (${reviewerRole}) ${String(noteText ?? "").trim()}`;
}

/**
 * Builds a timestamped admin-only note entry detailing a message sent to an applicant.
 */
function buildApplicantMessageNote(
  applicantName,
  applicantEmail,
  messageText,
  dateInput,
) {
  const timestamp = formatTimestamp(dateInput);
  return `[${timestamp}] Message sent to ${applicantName} (${applicantEmail}): "${String(messageText ?? "").trim()}"`;
}

/**
 * Maps an application status string to a CSS modifier class matching the dashboard status overview.
 */
function getStatusBadgeClass(status) {
  const normalized = String(status ?? "").toLowerCase();
  if (normalized === "eligible" || normalized === "accepted") {
    return "status-badge-eligible";
  }
  if (normalized === "ineligible" || normalized === "rejected") {
    return "status-badge-ineligible";
  }
  if (normalized === "manual review needed") {
    return "status-badge-manual";
  }
  return "status-badge-pending";
}

/**
 * Initializes the Individual Application Review view and modal controllers on the page.
 */
function initIndividualApplicationView(customApplicants) {
  const tbody = document.getElementById("individual-applications-tbody");
  if (!tbody) {
    return null;
  }

  const applicants = JSON.parse(
    JSON.stringify(customApplicants || DEFAULT_APPLICANTS),
  );
  const expandedDetailsState = { 1: true };
  const expandedNotesState = {};

  const editModal = document.getElementById("edit-application-modal");
  const editForm = document.getElementById("edit-application-form");
  const noteModal = document.getElementById("admin-note-modal");
  const noteForm = document.getElementById("admin-note-form");
  const messageModal = document.getElementById("message-applicant-modal");
  const messageForm = document.getElementById("message-applicant-form");

  let activeApplicantId = null;

  function findApplicant(id) {
    return applicants.find((item) => item.id === Number(id)) || null;
  }

  function renderTable() {
    tbody.innerHTML = applicants
      .map((applicant) => {
        const isDetailsOpen = Boolean(expandedDetailsState[applicant.id]);
        const isNotesOpen = Boolean(expandedNotesState[applicant.id]);
        const criteria = evaluateEligibilityCriteria(applicant.details);
        const statusClass = getStatusBadgeClass(applicant.status);
        const manualWarningIcon =
          applicant.status === "Manual Review Needed"
            ? '<span class="status-warning-indicator" aria-hidden="true">⚠ </span>'
            : "";

        const criteriaHtml = criteria
          .map((item) => {
            const fccManualControls = item.requiresManualConfirmation
              ? `
                <div class="fcc-manual-review-controls">
                  <span class="fcc-warning-badge" title="Needs manual review by admin user">
                    ⚠ Manual Admin Verification (115 problems screenshot)
                  </span>
                  <div class="fcc-verify-actions">
                    <label class="sr-only" for="fcc-role-${applicant.id}">Reviewer Role</label>
                    <select
                      id="fcc-role-${applicant.id}"
                      class="fcc-role-select"
                      data-fcc-role-for="${applicant.id}"
                      aria-label="Role for FreeCodeCamp confirmation for ${escapeHtml(applicant.name)}"
                    >
                      <option value="Admin User">Admin User</option>
                      <option value="Program Staff">Program Staff</option>
                    </select>
                    <button
                      type="button"
                      class="admin-button fcc-confirm-btn"
                      data-action="toggle-fcc"
                      data-applicant-id="${applicant.id}"
                    >
                      ${
                        applicant.details.freecodecamp_complete === true
                          ? "Mark Pending Review"
                          : "Confirm 115 Problems"
                      }
                    </button>
                  </div>
                </div>
              `
              : "";

            return `
              <div class="criterion-item" data-criterion="${escapeHtml(item.key)}">
                <div class="criterion-header">
                  <span class="criterion-label">${escapeHtml(item.label)}:</span>
                  ${renderCriterionIcon(item.status)}
                  <span class="criterion-value">${escapeHtml(item.value)}</span>
                </div>
                ${fccManualControls}
              </div>
            `;
          })
          .join("");

        const notesListHtml = applicant.admin_notes
          .map((note) => `<li class="admin-note-item">${escapeHtml(note)}</li>`)
          .join("");

        return `
          <tr class="applicant-main-row" id="applicant-row-${applicant.id}" data-applicant-id="${applicant.id}">
            <td class="applicant-identity-cell">
              <div class="applicant-name">${escapeHtml(applicant.name)}</div>
              <div class="applicant-email">${escapeHtml(applicant.email)}</div>
              <div class="applicant-meta">
                <span class="status ${statusClass}">${manualWarningIcon}${escapeHtml(applicant.status)}</span>
                <span class="applicant-submitted-date">Submitted: ${escapeHtml(applicant.date_submitted)}</span>
              </div>
            </td>
            <td class="applicant-score-cell">
              <span class="eligibility-score-badge" data-score-for="${applicant.id}">${escapeHtml(applicant.eligibility_score)}</span>
            </td>
            <td class="applicant-details-cell">
              <button
                type="button"
                class="admin-button details-toggle-btn"
                data-action="toggle-details"
                data-applicant-id="${applicant.id}"
                aria-expanded="${isDetailsOpen ? "true" : "false"}"
                aria-controls="applicant-details-${applicant.id}"
              >
                View Details
                <span class="details-chevron" aria-hidden="true">${isDetailsOpen ? "▴" : "▾"}</span>
              </button>
              <div
                id="applicant-details-${applicant.id}"
                class="applicant-details-panel"
                ${isDetailsOpen ? "" : "hidden"}
              >
                <div class="criteria-grid">
                  ${criteriaHtml}
                </div>
              </div>
            </td>
            <td class="applicant-actions-cell">
              <div class="applicant-action-buttons">
                <button
                  type="button"
                  class="admin-button edit-applicant-btn"
                  data-action="open-edit"
                  data-applicant-id="${applicant.id}"
                  aria-label="Edit ${escapeHtml(applicant.name)}"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <path d="M12 20h9"></path>
                    <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4Z"></path>
                  </svg>
                  Edit
                </button>
                <button
                  type="button"
                  class="admin-button leave-note-btn"
                  data-action="open-note"
                  data-applicant-id="${applicant.id}"
                  aria-label="Leave admin-only note for ${escapeHtml(applicant.name)}"
                >
                  Leave Admin Note
                </button>
                <button
                  type="button"
                  class="admin-button message-applicant-btn"
                  data-action="open-message"
                  data-applicant-id="${applicant.id}"
                  aria-label="Message ${escapeHtml(applicant.name)}"
                >
                  Message Applicant
                </button>
              </div>
            </td>
          </tr>
          <tr class="applicant-notes-row" data-notes-row-for="${applicant.id}">
            <td colspan="4" class="applicant-notes-dropdown-cell">
              <details
                class="admin-notes-dropdown"
                id="admin-notes-dropdown-${applicant.id}"
                data-applicant-id="${applicant.id}"
                ${isNotesOpen ? "open" : ""}
              >
                <summary class="admin-notes-summary">
                  <span>Admin-Only Notes (${applicant.admin_notes.length})</span>
                  <span class="notes-dropdown-hint">Click to toggle horizontal notes log ▾</span>
                </summary>
                <ul class="admin-notes-list" id="admin-notes-list-${applicant.id}">
                  ${notesListHtml}
                </ul>
              </details>
            </td>
          </tr>
        `;
      })
      .join("");
  }

  function openEditModal(applicantId) {
    const applicant = findApplicant(applicantId);
    if (!applicant || !editModal || !editForm) {
      return;
    }
    activeApplicantId = applicant.id;

    document.getElementById("edit-applicant-name").value = applicant.name;
    document.getElementById("edit-applicant-email").value = applicant.email;
    document.getElementById("edit-applicant-status").value = applicant.status;
    document.getElementById("edit-applicant-score").value =
      applicant.eligibility_score;
    document.getElementById("edit-wpm-score").value =
      applicant.details.wpm_score;
    document.getElementById("edit-wpm-accuracy").value =
      applicant.details.wpm_accuracy;
    document.getElementById("edit-two-references").value = String(
      Boolean(applicant.details.two_references),
    );
    document.getElementById("edit-freecodecamp-complete").value = String(
      Boolean(applicant.details.freecodecamp_complete),
    );
    document.getElementById("edit-gender").value = applicant.details.gender;
    document.getElementById("edit-computer-literate").value =
      applicant.details.computer_literate;
    document.getElementById("edit-recent-bootcamp").value =
      applicant.details.recent_bootcamp;
    document.getElementById("edit-stable-housing").value =
      applicant.details.stable_housing;

    editModal.hidden = false;
  }

  function openNoteModal(applicantId) {
    const applicant = findApplicant(applicantId);
    if (!applicant || !noteModal || !noteForm) {
      return;
    }
    activeApplicantId = applicant.id;
    const targetLabel = document.getElementById("note-modal-applicant-name");
    if (targetLabel) {
      targetLabel.textContent = `${applicant.name} (${applicant.email})`;
    }
    document.getElementById("admin-note-textarea").value = "";
    noteModal.hidden = false;
  }

  function openMessageModal(applicantId) {
    const applicant = findApplicant(applicantId);
    if (!applicant || !messageModal || !messageForm) {
      return;
    }
    activeApplicantId = applicant.id;
    const recipientLabel = document.getElementById(
      "message-modal-applicant-name",
    );
    if (recipientLabel) {
      recipientLabel.textContent = `${applicant.name} (${applicant.email})`;
    }
    document.getElementById("message-applicant-textarea").value = "";
    messageModal.hidden = false;
  }

  function closeAllModals() {
    if (editModal) {
      editModal.hidden = true;
    }
    if (noteModal) {
      noteModal.hidden = true;
    }
    if (messageModal) {
      messageModal.hidden = true;
    }
    activeApplicantId = null;
  }

  tbody.addEventListener("click", (event) => {
    const actionBtn = event.target.closest("[data-action]");
    if (!actionBtn) {
      return;
    }
    const action = actionBtn.getAttribute("data-action");
    const applicantId = Number(actionBtn.getAttribute("data-applicant-id"));

    if (action === "toggle-details") {
      expandedDetailsState[applicantId] = !expandedDetailsState[applicantId];
      renderTable();
    } else if (action === "toggle-fcc") {
      const applicant = findApplicant(applicantId);
      if (!applicant) {
        return;
      }
      const roleSelect = document.querySelector(
        `[data-fcc-role-for="${applicantId}"]`,
      );
      const role = roleSelect ? roleSelect.value : "Admin User";
      const nextState = !(applicant.details.freecodecamp_complete === true);
      applicant.details.freecodecamp_complete = nextState;
      const fccNote = buildFccConfirmationNote(nextState, role);
      applicant.admin_notes.unshift(fccNote);
      expandedDetailsState[applicantId] = true;
      expandedNotesState[applicantId] = true;
      renderTable();
    } else if (action === "open-edit") {
      openEditModal(applicantId);
    } else if (action === "open-note") {
      openNoteModal(applicantId);
    } else if (action === "open-message") {
      openMessageModal(applicantId);
    }
  });

  tbody.addEventListener(
    "toggle",
    (event) => {
      if (event.target.classList.contains("admin-notes-dropdown")) {
        const id = Number(event.target.getAttribute("data-applicant-id"));
        expandedNotesState[id] = event.target.open;
      }
    },
    true,
  );

  if (editForm) {
    editForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const applicant = findApplicant(activeApplicantId);
      if (!applicant) {
        return;
      }

      const role =
        document.getElementById("edit-reviewer-role")?.value || "Admin User";
      const newName = document
        .getElementById("edit-applicant-name")
        .value.trim();
      const newEmail = document
        .getElementById("edit-applicant-email")
        .value.trim();
      const newStatus = document.getElementById("edit-applicant-status").value;
      const newScore = Number(
        document.getElementById("edit-applicant-score").value,
      );
      const newWpm = Number(document.getElementById("edit-wpm-score").value);
      const rawAccuracy = document
        .getElementById("edit-wpm-accuracy")
        .value.trim();
      const newAccuracy = rawAccuracy.endsWith("%")
        ? rawAccuracy
        : `${rawAccuracy}%`;
      const newTwoRefs =
        document.getElementById("edit-two-references").value === "true";
      const newFcc =
        document.getElementById("edit-freecodecamp-complete").value === "true";
      const newGender = document.getElementById("edit-gender").value.trim();
      const newCompLit = document.getElementById(
        "edit-computer-literate",
      ).value;
      const newBootcamp = document.getElementById("edit-recent-bootcamp").value;
      const newHousing = document.getElementById("edit-stable-housing").value;

      const changes = [];
      const recordChange = (label, oldVal, nextVal) => {
        if (String(oldVal) !== String(nextVal)) {
          changes.push({ label, from: oldVal, to: nextVal });
        }
      };

      recordChange("Name", applicant.name, newName);
      recordChange("Email", applicant.email, newEmail);
      recordChange("Status", applicant.status, newStatus);
      recordChange("Eligibility Score", applicant.eligibility_score, newScore);
      recordChange("WPM Score", applicant.details.wpm_score, newWpm);
      recordChange("WPM Accuracy", applicant.details.wpm_accuracy, newAccuracy);
      recordChange(
        "Two References",
        applicant.details.two_references,
        newTwoRefs,
      );
      const fccChanged =
        Boolean(applicant.details.freecodecamp_complete) !== newFcc;
      recordChange(
        "FreeCodeCamp Complete",
        applicant.details.freecodecamp_complete,
        newFcc,
      );
      recordChange("Gender", applicant.details.gender, newGender);
      recordChange(
        "Computer Literate",
        applicant.details.computer_literate,
        newCompLit,
      );
      recordChange(
        "Recent Bootcamp",
        applicant.details.recent_bootcamp,
        newBootcamp,
      );
      recordChange(
        "Stable Housing",
        applicant.details.stable_housing,
        newHousing,
      );

      applicant.name = newName;
      applicant.email = newEmail;
      applicant.status = newStatus;
      applicant.eligibility_score = newScore;
      applicant.details.wpm_score = newWpm;
      applicant.details.wpm_accuracy = newAccuracy;
      applicant.details.two_references = newTwoRefs;
      applicant.details.freecodecamp_complete = newFcc;
      applicant.details.gender = newGender;
      applicant.details.computer_literate = newCompLit;
      applicant.details.recent_bootcamp = newBootcamp;
      applicant.details.stable_housing = newHousing;

      if (fccChanged) {
        applicant.admin_notes.unshift(buildFccConfirmationNote(newFcc, role));
      }
      const changeNote = buildFieldChangeNote(changes, role);
      if (changeNote) {
        applicant.admin_notes.unshift(changeNote);
      }

      expandedDetailsState[applicant.id] = true;
      expandedNotesState[applicant.id] = true;
      closeAllModals();
      renderTable();
    });
  }

  if (noteForm) {
    noteForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const applicant = findApplicant(activeApplicantId);
      if (!applicant) {
        return;
      }
      const noteText = document
        .getElementById("admin-note-textarea")
        .value.trim();
      const role =
        document.getElementById("note-author-role")?.value || "Admin User";
      if (!noteText) {
        return;
      }
      applicant.admin_notes.unshift(buildAdminNoteEntry(noteText, role));
      expandedNotesState[applicant.id] = true;
      closeAllModals();
      renderTable();
    });
  }

  if (messageForm) {
    messageForm.addEventListener("submit", (event) => {
      event.preventDefault();
      const applicant = findApplicant(activeApplicantId);
      if (!applicant) {
        return;
      }
      const messageText = document
        .getElementById("message-applicant-textarea")
        .value.trim();
      if (!messageText) {
        return;
      }
      applicant.admin_notes.unshift(
        buildApplicantMessageNote(applicant.name, applicant.email, messageText),
      );
      expandedNotesState[applicant.id] = true;
      closeAllModals();
      renderTable();
    });
  }

  document.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", closeAllModals);
  });

  [editModal, noteModal, messageModal].forEach((modal) => {
    if (modal) {
      modal.addEventListener("click", (event) => {
        if (event.target === modal) {
          closeAllModals();
        }
      });
    }
  });

  // Connect the top "Recent Applications" Review buttons to focus the Individual Application View
  const recentReviewButtons = document.querySelectorAll(
    ".recent-applicants .admin-button",
  );
  recentReviewButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const row = btn.closest("tr");
      const nameCell = row ? row.querySelector("td") : null;
      const targetName = nameCell ? nameCell.textContent.trim() : "";
      const matched =
        applicants.find(
          (app) => app.name.toLowerCase() === targetName.toLowerCase(),
        ) || applicants[0];
      if (matched) {
        expandedDetailsState[matched.id] = true;
        expandedNotesState[matched.id] = true;
        renderTable();
        const targetRow = document.getElementById(
          `applicant-row-${matched.id}`,
        );
        if (targetRow && typeof targetRow.scrollIntoView === "function") {
          targetRow.scrollIntoView({ behavior: "smooth", block: "center" });
        }
      }
    });
  });

  renderTable();

  return {
    applicants,
    renderTable,
    openEditModal,
    openNoteModal,
    openMessageModal,
    closeAllModals,
  };
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", () => {
    initIndividualApplicationView();
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    DEFAULT_APPLICANTS,
    escapeHtml,
    formatTimestamp,
    parsePercentage,
    evaluateEligibilityCriteria,
    renderCriterionIcon,
    buildFccConfirmationNote,
    buildFieldChangeNote,
    buildAdminNoteEntry,
    buildApplicantMessageNote,
    getStatusBadgeClass,
    initIndividualApplicationView,
  };
}
