// This file handles the initial job posting submission

const crypto = require("crypto")

// Store pending job postings in memory (in production, use a database)
const pendingJobPostings = {}

async function processJobPosting(req, res) {
  try {
    const jobData = req.body

    // Generate a unique ID for this job posting
    const postingId = crypto.randomUUID()

    // Store the job posting with its ID
    pendingJobPostings[postingId] = jobData

    // Send to staff channel for approval
    await sendToStaffChannel(jobData, postingId)

    return res.json({
      success: true,
      message: "Job posting sent for staff approval",
      postingId,
    })
  } catch (error) {
    console.error("Error processing job posting:", error)
    return res.status(500).json({
      success: false,
      error: "Failed to process job posting",
    })
  }
}

async function sendToStaffChannel(jobData, postingId) {
  const staffWebhook = process.env.SLACK_STAFF_WEBHOOK

  if (!staffWebhook) {
    throw new Error("SLACK_STAFF_WEBHOOK environment variable is not set")
  }

  // Create approval buttons with the posting ID
  const baseUrl = process.env.VERCEL_URL || "http://localhost:3000"
  const approveUrl = `${baseUrl}/public/static/js/approve-job-post.js?id=${postingId}`
  const rejectUrl = `${baseUrl}/public/static/js/reject-job-post.js?id=${postingId}`

  const message = {
    text: "A new job posting requires approval",
    blocks: [
      {
        type: "header",
        text: {
          type: "plain_text",
          text: "New Job Posting Requires Approval",
          emoji: true,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Job Title:* ${jobData.jobTitle}\n*Company:* ${jobData.company}\n*Type:* ${jobData.type || "Not specified"}\n*Education Requirement:* ${jobData.educationReq || "Not specified"}\n*Location:* ${jobData.location}\n*Referral offered:* ${jobData.referral}\n*Salary Range:* ${jobData.salaryRange || "Not specified"}`,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Description:*\n${jobData.description || "No description provided"}`,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Application Link:*\n${jobData.applicationLink || "No link provided"}`,
        },
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Contact:*\n${jobData.firstName} ${jobData.lastName} (${jobData.email})`,
        },
      },
      {
        type: "actions",
        elements: [
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "Approve",
              emoji: true,
            },
            style: "primary",
            url: approveUrl,
          },
          {
            type: "button",
            text: {
              type: "plain_text",
              text: "Reject",
              emoji: true,
            },
            style: "danger",
            url: rejectUrl,
          },
        ],
      },
    ],
  }

  const response = await fetch(staffWebhook, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(message),
  })

  if (!response.ok) {
    throw new Error(`Failed to send to staff channel: ${response.statusText}`)
  }

  return response
}

// Export the function and the pendingJobPostings object
module.exports = {
  processJobPosting,
  pendingJobPostings,
}
