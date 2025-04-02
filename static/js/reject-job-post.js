// This file handles job posting rejection

const { pendingJobPostings } = require("./process-job-posting")

async function rejectJobPosting(req, res) {
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

    // Check if the job posting exists
    if (!pendingJobPostings[postingId]) {
      return res.status(404).json({
        success: false,
        error: "Job posting not found",
      })
    }

    // Remove from pending
    delete pendingJobPostings[postingId]

    // Return a simple HTML response
    res.setHeader("Content-Type", "text/html")
    return res.send(
      `<html>
        <head>
          <title>Job Posting Rejected</title>
          <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
            .rejected { color: red; }
          </style>
        </head>
        <body>
          <h1 class="rejected">Job Posting Rejected</h1>
          <p>The job posting has been rejected and will not be sent to the graduates channel.</p>
          <p>You can close this window now.</p>
        </body>
      </html>`,
    )
  } catch (error) {
    console.error("Error rejecting job posting:", error)
    return res.status(500).json({
      success: false,
      error: "Failed to reject job posting",
    })
  }
}

module.exports = {
  rejectJobPosting,
}
