# Step 1: Register as a Volunteer

Before doing anything else, you must [register as a volunteer](https://docs.google.com/forms/d/e/1FAIpQLSeW0mo-Dpsig70374UEPvzexpas-31Ost_HsFwm0kjNOxtbtg/viewform?c=0&w=1).

# Step 2: Read through and Agree to the Code of Conduct

Before opening an issue, commenting, etc you must read and agree to the [Code of Conduct](https://docs.google.com/document/d/16LUxODmHN3N2r4GPA-YeNgXP0MIQCl6gW_twJralb5w/edit?tab=t.0).

# Step 3: Finding an Issue to Work On

## External Hackathon Participants

- **Follow Step 1 and Step 2 above**
- If you are new to contributing to GitHub projects, review the [GSSoC guide](https://github.com/GSSoC24/Contributor/tree/main/gssoc-guidelines), read the [best practices](#best-practices) section below, contact Techtonica [program staff](https://techtonica.org/team/) or talk to a Techtonica mentor via Slack (in #mentors).
  - [Issues tagged with GSSoC](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3Agssoc%20no%3Aassignee)
  - [Issues tagged with ODHack14](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3AODHack14%20no%3Aassignee)
  - [Issues tagged with Hacktoberfest](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3AHacktoberfest%20no%3Aassignee)
  - [Issues tagged with GHC](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3AGHC%20no%3Aassignee)

## Techtonica Volunteers

- Find any [unassigned open issue](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20no%3Aassignee).

## All Contributors

- If you find an issue that sounds interesting to you and you have the knowledge to complete it...
  - **Confirm no one is already assigned to it has in-progress work**
  - **Confirm no one has commented already asking to be assigned** - assignments are assigned to the first commenter
- Leave a comment stating the following:
  - [ ] Formally ask to be assigned to the issue (feel free to follow it up with a slack message).
  - [ ] Formally acknowledge that you agree to the [Code of Conduct](https://docs.google.com/document/d/16LUxODmHN3N2r4GPA-YeNgXP0MIQCl6gW_twJralb5w/edit?tab=t.0).
  - [ ] Include confirmation that you have filled out the [Volunteer Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeW0mo-Dpsig70374UEPvzexpas-31Ost_HsFwm0kjNOxtbtg/viewform?c=0&w=1).
  - [ ] Include any clarification questions you may have after reading the description. Specific questions work better, e.g. "Which file should change?" rather than asking a broader question such as requesting "an explanation" or "more details"
- Once you have been assigned on the issue, **do not request assignment to any other issues until you have opened a Pull Request**. If you changed your mind and would rather work on a different one, comment on the originally assigned issue to request to be **unassigned**.
- Create a pull request of the changes requested by completing the prompted pull request template.
- Review our [Style Guide](https://github.com/Techtonica/techtonica.org/wiki#links-to-styling-guides) to make sure your changes conform to it.

🎗️ _**Please note, all repo support will operate within U.S. Pacific Timezone.**_

## Working on your Issue

- Comment on the issue directly if you have a question (feel free to follow it up with a Slack message).
- People are welcome to team up on an issue. If you see someone is already assigned but you want to help, leave the other assignee a message on the issue about collaborating.
- Please note any time senstive due dates or labels! Any amount of help is appreciated, but if the deadline approaches and you won't be able to complete it, please leave a comment about your progress and unassign yourself from the issue so someone else can pick it up. If you forked the repo, go ahead and make a pull request with what you have.

## Best Practices
These best practices are very important when working on a development team. Having code reviews from a team means that there will potentially be multiple request for changes from several reviewers. It helps everyone in the code review to understand what has been addressed, iterated on, what remains outstanding, and even gives opportunity to provide any missing context to one another.

#### GitHub Issues
- Leave a comment to request an issue for assignment.
- Communicate status updates about work on issue frequently throughout each sprint week.
- Communicate any blockers or work dependencies on the issue why ensuring that relevant stakeholders are aware.
- Communicate when their work is complete with reference to relevant PRs.

#### Pull Request
When addressing requests for changes it is best practice to do so in a visible and tangible way. You can do this by:
- **Acknowleding** each request for change (i.e. feedback was marked with an emoji reaction to show its accepted).
- Provide a **written response** to the request for changes in one of the following ways:
  1. summary comment addressing each individual request for change stating how and where (the commit hash referenced) you made the change
  2. reply to each comments generated via GitHub in your generated request for change
  3. share an alternative thought with explanation of why you do not wish to implement the request for change or ask any clarifying questions
- Once actively stating how you've addressed a request for change alongside referencing the hash in which the change was made, **mark the comment as "resolved"**.
- Connect the GitHub issue being addressed in the “Development” section
- Assign yourself as the PR “Assignee”
- Request a staff, peer, and mentor reviewer
- The PR title should be descriptive enough to give an at a glance understanding of what you're working on

## Application Automaton Work
- You can find the app-based or application automation files on the `mvp` branch
- Please point any of this related work to be merged back into `mvp` rather than `develop` branch, via your PR
- Please get clarification from program staff when in doubt or having related questions
