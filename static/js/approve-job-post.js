// This file handles job posting approval

const { pendingJobPostings } = require("./process-job-posting")

async function approveJobPosting(req, res) {
  try {
    // Get the posting ID from the query parameters
    const url = new URL(req.url, `http://${req.headers.host}`)
    const postingId = url.searchParams.get("id")

    if (!postingId) {
      return res.status(400).json({
        success: false,
        error: "Missing posting ID",
      })
    }

    // Get the job posting data
    const jobData = pendingJobPostings[postingId]

    if (!jobData) {
      return res.status(404).json({
        success: false,
        error: "Job posting not found",
      })
    }

    // Send to graduates channel
    await sendToGraduatesChannel(jobData)

    // Remove from pending
    delete pendingJobPostings[postingId]

    // Return a simple HTML response
    res.setHeader("Content-Type", "text/html")
    return res.send(
      `<html>
        <head>
          <title>Job Posting Approved</title>
          <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .success { color: green; }
          </style>
        </head>
        <body>
          <h1 class="success">Job Posting Approved</h1>
          <p>The job posting has been approved and sent to the graduates channel.</p>
          <p>You can close this window now.</p>
        </body>
      </html>`,
    )
  } catch (error) {
    console.error("Error approving job posting:", error)
    return res.status(500).json({
      success: false,
      error: "Failed to approve job posting",
    })
  }
}

async function sendToGraduatesChannel(jobData) {
  const graduatesWebhook = process.env.SLACK_GRADUATES_WEBHOOK

  if (!graduatesWebhook) {
    throw new Error("SLACK_GRADUATES_WEBHOOK environment variable is not set")
  }

  const message = {
    text: "A new job has been posted to Techtonica! Read the details below to see if you're a good fit!",
    blocks: [
      {
        type: "header",
        text: {
          type: "plain_text",
          text: "New Job Opportunity",
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
    ],
  }

  const response = await fetch(graduatesWebhook, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(message),
  })

  if (!response.ok) {
    throw new Error(`Failed to send to graduates channel: ${response.statusText}`)
  }

  return response
}

module.exports = {
  approveJobPosting,
}
