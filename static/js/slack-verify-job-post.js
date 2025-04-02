// This file handles Slack signature verification

const crypto = require("crypto")

async function verifySlackRequest(req, res) {
  try {
    // Get the Slack signing secret from environment variables
    const slackSigningSecret = process.env.SLACK_SIGNING_SECRET

    if (!slackSigningSecret) {
      console.error("SLACK_SIGNING_SECRET is not set")
      return res.status(500).json({ error: "Server configuration error" })
    }

    // Get the Slack signature and timestamp from headers
    const slackSignature = req.headers["x-slack-signature"]
    const slackTimestamp = req.headers["x-slack-request-timestamp"]

    if (!slackSignature || !slackTimestamp) {
      return res.status(400).json({ error: "Missing Slack signature headers" })
    }

    // Check if the request is older than 5 minutes
    const currentTime = Math.floor(Date.now() / 1000)
    if (Math.abs(currentTime - Number.parseInt(slackTimestamp)) > 300) {
      return res.status(400).json({ error: "Request timestamp is too old" })
    }

    // Get the request body as text
    const body = req.rawBody || JSON.stringify(req.body)

    // Create the signature base string
    const baseString = `v0:${slackTimestamp}:${body}`

    // Create the signature to compare with the one from Slack
    const mySignature = "v0=" + crypto.createHmac("sha256", slackSigningSecret).update(baseString).digest("hex")

    // Check if the signatures match
    if (crypto.timingSafeEqual(Buffer.from(mySignature), Buffer.from(slackSignature))) {
      // Signatures match, request is from Slack
      return res.json({ success: true })
    } else {
      // Signatures don't match
      return res.status(401).json({ error: "Invalid signature" })
    }
  } catch (error) {
    console.error("Error verifying Slack request:", error)
    return res.status(500).json({ error: "Server error" })
  }
}

module.exports = {
  verifySlackRequest,
}
