# Application Form Style Guidelines

This guide documents the UI, content, formatting, validation, and accessibility conventions for Techtonica’s application form pages.

Use this guide when building or updating the application form, or when creating future multi-step form features on the Techtonica website.

## What Should Appear Before the Form?

Before users reach the first form page, show a descriptive information page. This page gives applicants the context they need before starting the application.

### Required headings

The pre-form information page should include placeholder text, to be updated by program staff, under the following headings in this order:

1. The Program
2. Pre-Req and Form Deadline
3. Eligibility
4. Application Process
5. What We Look For
6. How to Prepare
7. Acceptance & Onboarding

## How Should the Multi-Step Progress Indicator Work?

The application form has six pages. A progress indicator must always be visible at the top of each page so users know which step they are on and how many steps remain.

### Acceptable formats

Use one of the following formats:

- A progress bar showing percentage of completion
- Step dots showing each step as a numbered or labeled point

### Required form pages

1. General Applicant Demographics
2. Applicant & Household Financial Information
3. Additional Applicant Information
4. Applicant Long-Text Answers
5. Administrative Questions
6. Confirmation / Submission Page

### Behavior requirements

- The current step must be clearly highlighted or visually distinguished.
- Completed steps may be shown with a filled dot, checkmark, or similar indicator.
- Users must not be able to skip ahead by manually changing the URL.

## When Should We Use Info Icon Hover Bubbles?

An info icon hover bubble places a small info icon next to a question label. When the user hovers over or focuses on the icon, a tooltip appears with additional guidance.

### When to use an info icon

Use an info icon when:

- The question label is not self-explanatory.
- Additional context would help the applicant answer correctly.
- The guidance is useful, but too long to include directly in the label.

Do not use info icons on every question. Use them only where they add real value.

Place the icon directly next to the question label, not below it.

### Accessibility requirements

- The tooltip must appear on mouse hover.
- The tooltip must also appear on keyboard focus.
- The tooltip must disappear when the cursor or keyboard focus moves away.
- The icon must include appropriate ARIA attributes, such as `aria-label` or `aria-describedby`.

### Tooltip text by form section

Use the following tooltip text exactly as written.

#### Demographics page

- **How to pronounce your full name** — "You can make a recording here (name-coach.com), generate your link and share in the text field if preferred"
- **Email address** — "Please use the same business-minded Gmail with your name (like janedoe@gmail.com, jdoe@gmail.com) that you used in the shorter form. This is the email we will contact you with for the duration of the application process and program."
- **What is your birth date?** — "In this format: Month/Date/Year"
- **Cell phone number with area code** — "In this format: 555-555-5555"
- **Do you have a disability?** — "You are considered to have a disability if you have a physical or mental impairment or medical condition that substantially limits a major life activity, or if you have a history or record of such an impairment or medical condition. Disabilities include, but are not limited to: Blindness, Deafness, Cancer, Diabetes, Epilepsy, Autism, Cerebral Palsy, HIV/AIDS, Schizophrenia, Muscular Dystrophy, Bipolar Disorder, Major Depression, Multiple Sclerosis (MS), missing limbs or partially missing limbs, Post-Traumatic Stress Disorder (PTSD), Obsessive Compulsive Disorder, impairments requiring the use of a wheelchair, intellectual disability."

#### Financial page

- **Annual household income** — "In this format: 40000. If you have any special circumstances that make you question your eligibility for Techtonica's program, please feel free to contact us (info@techtonica.org) and we will be happy to discuss with you."
- **Net worth** — "In this format: 1500. This info helps us calculate overall stipend needs. Please give a summation and verification for your total wealth or financial assets as an individual (or shared household, if that applies, including cash, stocks, bonds, mutual funds, and bank deposits); excluding financial liabilities. If you believe you have none of these whatsoever, then report the value as such and submit documentation in the next question to that end (such as a termination letter, public benefits verification, etc). If you need to provide an explanation for your answers, please do so in the 'Anything else you want to share with us?' question which is second-to-last in this form."
- **Net worth verification upload** — "This info helps us calculate overall stipend needs."
- **Average monthly costs** — "This includes things like: groceries, phone & internet, medical expenses, childcare, rent, insurance, utilities, loan payments, etc. Please only put a total whole number in this field (i.e. 1200, not 1200.09)"

#### Additional information page

- **How many times have you applied?** — "If you have already applied three times in the past, you are not eligible to apply again and should stop filling out this form."
- **Are you willing to quit your job(s)?** — "We advise AGAINST working part-time during this intensive program."

#### Long-text answers page

- **Self-assessment rating scale** — "1=Disagree, 2=Somewhat disagree, 3=Somewhat agree, 4=Agree"
- **List all the steps to make a sandwich** — "This is to help us assess your logical thinking; please be specific and thorough."
- **How did you find out about Techtonica?** — "The more specific you can be, the better—was it a flyer, and if so, where? Did a friend tell you, and if so, how did they find out? Was it a Facebook group, and if so, which one? Etc."
- **Other full URLs to you online** — "For example, 'https://twitter.com/TechtonicaOrg'"
- **Reference #1** — "This may not be a relative, significant other, or friend. It must be someone who can speak to your work quality in an unbiased manner."
- **Reference #2** — "This may not be a relative, significant other, or friend. It must be someone who can speak to your work quality in an unbiased manner."

#### Administrative questions page

- **Do you have a MacBook?** — "This is to let us know if we will need to help you secure a MacBook during the program."
- **Would you be willing to move to a new city?** — "While this is not currently a requirement, it may be a requirement again in the near future, and it increases your chances of securing a job."

## What Form Input Types Should We Use?

Use the input type that best matches the type of answer the applicant needs to provide.

### When to use multiple choice

Use multiple choice when:

- The set of valid answers is fixed and known in advance.
- You want to prevent free-text errors or inconsistent responses.
- The question has a Yes/No answer.

### When to use a text input

Use a text input when:

- The answer is open-ended or unique to the applicant.
- The answer requires a sentence, paragraph, or explanation.
- The answer is a URL, email address, or numeric value that requires format validation.

### When to use a dropdown

Use a dropdown when there are roughly five or more options.

Dropdowns save vertical space and work better for longer lists.

Examples:

- Gender identity
- Race/ethnicity
- Age group

### When to use a bubble list

Use a bubble list when there are roughly four or fewer options.

Bubble lists are easier to scan and feel lighter for short selections.

Examples:

- Yes/No questions
- Number of prior applications

### How should “Other” options work?

If a dropdown includes an **Other** option, selecting it must activate a text input field so the user can type their own answer.

This applies to:

- Gender identity
- Pronouns
- Race/ethnicity

## What Other Input Types Are Used?

Use the following input types where appropriate:

- **Text input** — Open-ended answers, names, and free-text responses
- **Text input with email validation** — Applicant email and reference email fields
- **Text input with URL validation** — LinkedIn URL and MIT Living Wage Calculator URL fields
- **Number input with value greater than or equal to 0** — Annual household income and net worth
- **Number input with value greater than or equal to 25000** — MIT Living Wage Calculator annual income amount
- **Whole number input** — Average monthly costs and typing accuracy percentage
- **Multiple choice grid rated 1–4** — Self-assessment statements
- **Upload field** — Income verification, net worth verification, typing test screenshot, and FreeCodeCamp screenshot
- **Checkbox** — Single confirmation or agreement statement
- **Multiple text input** — Related sub-fields within one question, such as reference contact info or emergency contact

## What Data Formats Should the Form Enforce?

Where a tooltip specifies a format, that format is the enforced standard.

Validate all fields on the client side before allowing the user to proceed to the next page.

### Phone number format

Use this format in forms:

    555-555-5555

Example:

    415-123-4567

Do not use this format in forms:

    (555) 555-5555

Enforce the `555-555-5555` format with input validation.

### Date format

Two input methods are acceptable.

#### Text input

Use `Month/Date/Year`.

Example:

    01/15/1990

#### Calendar popup

A date picker is acceptable as an alternative input method.

Choose the input method based on implementation context.

### Money and numeric value format

Inside form fields, use whole numbers only.

Do not include:

- Currency symbols
- Commas
- Decimals

Correct examples:

    40000
    1500
    1200

Incorrect examples:

    $40,000
    $1,500.80
    40000.00
    1,200

For the monthly costs field specifically, use whole numbers only. Do not allow decimals.

## How Should the Self-Assessment Rating Scale Work?

The self-assessment section on the Long-Text Answers page uses a rated 1–4 scale displayed as a multiple choice grid.

The hover bubble for this section must display all four values and their labels.

### Rating labels

- **1** = Disagree
- **2** = Somewhat disagree
- **3** = Somewhat agree
- **4** = Agree

### Self-assessment statements

Include the following nine statements:

1. I am comfortable presenting a project or short talk to a group.
2. I am comfortable collaborating with others on a team.
3. I am comfortable asking others for help when I'm stuck.
4. I do not hide that I'm struggling from friends, colleagues, or managers.
5. I care greatly about diversity, equity, and inclusion.
6. I learn brand-new concepts quickly.
7. When working with others, I'm the person who likes to help everyone get up to speed.
8. I would be interested in mentoring future participants after I graduate from Techtonica.
9. I would be actively involved with Techtonica's graduates group after completion of the program.

## How Should File Upload Fields Work?

All upload fields connect to a private Google Drive folder. Files are not stored in a public database.

The maximum file size per upload is 10MB.

### Upload field specifications

- **Household income verification documents** — Financial page; up to 10 files; no file type restriction
- **Net worth verification documents** — Financial page; one file; no file type restriction
- **Typing test screenshot** — Additional page; one file; no file type restriction
- **FreeCodeCamp screenshot** — Additional page; one file; images and PDFs only

## What Button Styles Should We Use?

Buttons should follow site-wide visual standards and use SCSS variables from `_settings.scss`.

### Primary buttons

Use primary buttons for actions like:

- Next
- Submit

Primary buttons should use:

- Orange background: `$focal-orange`
- Blue hover state
- White text

### Secondary buttons

Use secondary buttons for actions like:

- Back
- Cancel

Secondary buttons should use:

- Blue background: `$main-blue`
- Lighter blue hover state
- White text

### Button text

Button text must always be white.

Do not use blue text on any button.

Always use SCSS variables from `_settings.scss` for colors. Never hardcode hex values.

### Button font size

Use the site-wide button font size standard:

    22px / 1.375em / 16.5pt

### Button layout

Until a site-wide standard is confirmed, follow these practices for the application form:

- **Letter case** — Use Title Case, such as Next Step, Go Back, and Submit Application.
- **Alignment** — Right-align primary buttons such as Next and Submit.
- **Alignment** — Left-align secondary buttons such as Back.
- **Width** — Size buttons to their content.
- **Width** — Do not use full-width buttons inside form pages.
- **Border radius** — To be determined by the design team.

## How Should the Form Meet Accessibility Standards?

The application form must be responsive and accessible.

### General accessibility requirements

- All form fields must have visible, properly associated `<label>` elements.
- All info icon hover bubbles must include ARIA attributes, such as `aria-label` or `aria-describedby`.
- All info icon hover bubbles must be keyboard accessible.
- Upload fields must have descriptive labels so screen readers can identify them.
- Required fields must be clearly indicated both visually and programmatically.
- The form must use HTML5 semantic elements throughout.

### Color contrast requirements

All of the following elements in the application form must pass WCAG AA contrast requirements before a pull request is submitted:

- Form field labels
- Placeholder text inside inputs
- Helper text and info icon hover bubble text
- Error and validation messages
- Button text on all button types and states, including default and hover
- Any text placed on a colored background

Use the WebAIM Contrast Checker or a browser accessibility extension such as axe DevTools to verify contrast.

## How Should Form Validation Work?

The application form uses client-side validation via HTML5 attributes and JavaScript.

All required fields must be validated before the user can proceed to the next page.

Users must not be able to skip ahead by manually changing the URL.

### Field-specific validation rules

- **Email fields** — Must match a valid email format.
- **URL fields** — Must match a valid URL format and include `https://`.
- **Phone fields** — Must match the `555-555-5555` format.
- **Date fields** — Must match `Month/Date/Year` format if using text input.
- **Income and net worth fields** — Must be a number greater than or equal to 0.
- **MIT Living Wage amount** — Must be a number greater than or equal to 25000.
- **Monthly costs and typing accuracy** — Must be whole numbers with no decimals.
- **File upload fields** — Must not exceed 10MB per file.
- **FreeCodeCamp screenshot field** — Must accept images and PDFs only.
