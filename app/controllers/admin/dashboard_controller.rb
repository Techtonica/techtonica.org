class Admin::DashboardController < ApplicationController
  before_action :authenticate_admin!

  def index
    @stats = {
      totalUsers: 2000,
      totalApplications: 750,
      acceptanceRate: "6.67%",
      rejectionRate: "26.67%",
      percentDifferenceFromLastMonth: "+15%"
    }

    @applicationsByStatus = {
      "applicationFormSubmitted": 700,
      "initialScreeningPassed": 500,
      "applicationWorkshop": 400,
      "pairProgrammingWithStaff": 300,
      "takeHomeCodeChallenge": 250,
      "staffInterview": 200,
      "boardInterview": 150,
      "referenceSubmitted": 120,
      "financialConversation": 100,
      "pending": 80,
      "approved": 50,
      "prescreenRejected": 300,
      "rejected": 200
    }

    @applicants = [
      {
        id: 1, name: "Jane Doe", email: "jane.doe@example.com", eligibility_score: 90, status: "Eligible", date_submitted: "2025-01-15",
        details: { wpm_score: 55, wpm_accuracy: "85%", two_references: true, freecodecamp_complete: true, gender: "Non-binary", computer_literate: "Yes", recent_bootcamp: "No", stable_housing: "Yes" },
        admin_notes: ["Follow-up required after interview.", "Strong technical background"]
      },
      {
        id: 2, name: "John Smith", email: "john.smith@example.com", eligibility_score: 75, status: "Eligible", date_submitted: "2025-01-12",
        details: { wpm_score: 52, wpm_accuracy: "82%", two_references: true, freecodecamp_complete: false, gender: "Woman", computer_literate: "Yes", recent_bootcamp: "No", stable_housing: "Yes" },
        admin_notes: ["Pending reference check."]
      },
      {
        id: 3, name: "Alice Johnson", email: "alice.johnson@example.com", eligibility_score: 45, status: "Ineligible", date_submitted: "2025-01-10",
        details: { wpm_score: 30, wpm_accuracy: "70%", two_references: false, freecodecamp_complete: false, gender: "Woman", computer_literate: "No", recent_bootcamp: "Yes", stable_housing: "No" },
        admin_notes: ["Did not meet eligibility requirements."]
      },
      {
        id: 4, name: "Bob Williams", email: "bob.williams@example.com", eligibility_score: 60, status: "Pending", date_submitted: "2025-01-18",
        details: { wpm_score: 50, wpm_accuracy: "80%", two_references: false, freecodecamp_complete: false, gender: "Non-binary", computer_literate: "Yes", recent_bootcamp: "No", stable_housing: "Yes" },
        admin_notes: ["Awaiting staff interview."]
      },
      {
        id: 5, name: "Chris Adams", email: "chris.adams@example.com", eligibility_score: 50, status: "Manual Review Needed", date_submitted: "2025-01-20",
        details: { wpm_score: 49, wpm_accuracy: "78%", two_references: false, freecodecamp_complete: false, gender: "Man", computer_literate: "Yes", recent_bootcamp: "No", stable_housing: "Yes" },
        admin_notes: ["Requires additional financial documents."]
      }
    ]
  end

  private

  def authenticate_admin!
    # Implement admin check logic here
    # redirect_to root_path unless current_user&.admin?
  end
end
