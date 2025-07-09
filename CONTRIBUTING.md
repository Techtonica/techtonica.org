# Step 1: Register as a Volunteer

Before doing anything else, you must [register as a volunteer](https://docs.google.com/forms/d/e/1FAIpQLSeW0mo-Dpsig70374UEPvzexpas-31Ost_HsFwm0kjNOxtbtg/viewform?c=0&w=1).

# Step 2: Read through and Agree to the Code of Conduct

Before opening an issue, commenting, etc you must read and agree to the [Code of Conduct](https://docs.google.com/document/d/16LUxODmHN3N2r4GPA-YeNgXP0MIQCl6gW_twJralb5w/edit?tab=t.0).

# Step 3: Finding an Issue to Work On

## External Hackathon Participants

- **Follow Step 1 and Step 2 above**
- If you are new to contributing to GitHub projects, review the [GSSoC guide](https://github.com/GSSoC24/Contributor/tree/main/gssoc-guidelines), read the [best practices](#best-practices) section below, contact Techtonica [program staff](https://techtonica.org/team/) or talk to a Techtonica mentor via Slack (in #mentors).
  - [Issues tagged with GSSoC](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3Agssoc%20no%3Aassignee)
  - [Issues tagged with Only Dust Hackathon](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20state%3Aopen%20no%3Aassignee%20label%3Aonlydust-wave)
  - [Issues tagged with Hacktoberfest](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3AHacktoberfest%20no%3Aassignee)
  - [Issues tagged with GHC](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20is%3Aopen%20label%3AGHC%20no%3Aassignee)
  - [Issues tagged with 100daysofcode](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20state%3Aopen%20label%3A100daysofcode)
  - [Issues tagged with 'good first issue'](https://github.com/Techtonica/techtonica.org/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22)

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
- Review our [Style Guide](https://github.com/Techtonica/techtonica.org/wiki#links-to-styling-guides) to make sure your changes conform to it. See also:
  - [Style Guide & Logo Folder](https://www.dropbox.com/scl/fo/sb8ppa0qxuuott515euei/h?rlkey=1ghfh6urkf2rakbonngk9z3bd&st=q935c0bj&dl=0)
  - [sass style folder](https://github.com/Techtonica/techtonica.org/tree/develop/static/sass) - settings has some built in site wide variables, styles.css has the site wide styling
  - [Post a job feature styling](https://techtonica.org/share-a-job)

🎗️ _**Please note, all repo support will operate within U.S. Pacific Timezone.**_

## Working on your Issue
- Comment on the issue directly if you have a question (feel free to follow it up with a Slack message).
- People are welcome to team up on an issue. If you see someone is already assigned but you want to help, leave the other assignee a message on the issue about collaborating.
- Please note any time senstive due dates or labels! Any amount of help is appreciated, but if the deadline approaches and you won't be able to complete it, please leave a comment about your progress and unassign yourself from the issue so someone else can pick it up. If you forked the repo, go ahead and make a pull request with what you have.

## Slack Communication
If you are in Techtonica's slack space, please communicate about website related work or requests in the #website channel. If you are not in the Techtonica slack community and would like to be added, after having completed [the volunteer form](https://docs.google.com/forms/d/e/1FAIpQLSeW0mo-Dpsig70374UEPvzexpas-31Ost_HsFwm0kjNOxtbtg/viewform?c=0&w=1), please kindly search your email for `You can join our Slack by clicking here` or send info@techtonica.org an email.

## Application Automaton Work
- You can find the app-based or application automation files on the `mvp` branch
- Please point any of this related work to be merged back into `mvp` rather than `develop` branch, via your PR
- Please get clarification from program staff when in doubt or having related questions

## Best Practices
These best practices are very important when working on a development team. Having code reviews from a team means that there will potentially be multiple request for changes from several reviewers. It helps everyone in the code review to understand what has been addressed, iterated on, what remains outstanding, and even gives opportunity to provide any missing context to one another.

#### Communicate Proactively
If you're unsure about something, **ask questions** in the relevant GitHub Issue or discussion thread. It's always better to ask for clarification than to spend time building something that doesn't align with the project's goals.

#### GitHub Issues
- Leave a comment to request an issue for assignment.
- Communicate status updates about work on issue frequently throughout each sprint week.
- Communicate any blockers or work dependencies on the issue why ensuring that relevant stakeholders are aware.
- Communicate when their work is complete with reference to relevant PRs.

#### Learn from the Existing Code
Before writing new code, take a few minutes to explore the existing codebase. How are other components structured? What naming conventions are used for CSS classes? Following existing patterns helps maintain consistency across the project.

#### Keep Your Changes Focused
- A pull request should address **one issue at a time**. If you notice another bug or have an idea for a different improvement while working, finish your current task first, and then open a new issue for the other item. This makes your changes much easier and faster to review.
- Use small, logical commits with clear messages (e.g., `feat: Create new sponsor card component`, `style: Apply brand colors to tier buttons`).
- A great practice in larger projects is to think in terms of **components**. Treat the 'sponsor tier card' as a self-contained block. All of its styles—the header, the list, the button—should be scoped within its main class (`.sponsor-tier-card`). This prevents styles from 'leaking out' and affecting other parts of the site, and it makes the component much easier to maintain or reuse in the future.

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
- Complete the PR template in its entirety: write a clear and descriptive title and body, explain *what* problem you're solving and *how* you've solved it, link the PR to the issue it resolves (e.g., "Closes #123").
- If you have updated any styling, please include a full visual review of your updates in your pull request.

#### Embrace the Feedback Loop
- Code review is a collaborative process, not a critique of you as a person. Every developer, from junior to senior, receives feedback on their code. View it as a learning opportunity.
- When you receive feedback, respond to each comment (a simple "Done" or a thumbs-up emoji is often enough) and push your changes to the same branch to update the PR. Please don't close the PR and open a new one.

## Styling Best Practices
By scoping the CSS to the new components and using our existing design tokens (colors, fonts), we can ensure the page looks great without causing unintended side effects elsewhere.

#### 1. Remove Global Style Overrides
Universal selectors or global styles are too broad and are changing the look and feel of the entire website. They should be removed. The `*` (universal selector) and `body` styles are resetting margins, padding, and changing the default font and background color for every page on the site.

**Recommendation:** Please do not adjust the universal (`*`) and `body` style rules. Our site already has base styles defined, and adding new rules could override them, causing inconsistencies in fonts, colors, and layout across all pages.

#### 2. Scope Component-Specific Styles
New styles are great, but they need to be properly contained. While the new styles can be placed within the `style.scss` file, some existing class definitions like `.main-content`, `.row`, `.column`, and `.blue-background` can be unintentionally modified. These are utility classes used across the entire site. Modifying them affects every page that uses them.

**Recommendation:** To ensure your new styles only affect your specific component, please make sure all new style rules are nested inside the their component specific class. This will prevent them from accidentally affecting other elements on the site. You can also create a component specific style sheet if applicable.

#### 3. Use Existing Design System Variables
To maintain visual consistency, it's important to use the project's predefined variables for colors and fonts instead of hardcoding new values. Rather than introducing new styles introduce hardcoded color values (e.g., `#05556d`, `#f67625`, `#16c1f3`) and new font families (`'Segoe UI'`, `Lato`). The original `style.scss` uses variables like `$main-blue` and `$focal-orange` from an imported `_settings.scss` file.

**Recommendation:** Our project uses SCSS variables for colors to maintain a consistent theme. Instead of using hardcoded hex values, please use the corresponding variables from our `_settings.scss` file. For example, use `$focal-orange` for buttons instead of `#f67625`. Similarly, please use the site's existing font family instead of introducing `Lato` or `Segoe UI`.

_**Your willingness to learn and adapt is what makes a great open source contributor. We're really happy to have you working with us!**_
