# Missing Image on Full Time Page Mobile View #750

- Environment successfully set up
- Branch created: develop-issue-750

# What the Issue Is About

On the Full-Time Program page of the Techtonica site, the hero/leading image does not appear on real mobile devices. Instead, users see a black background.

Important detail:

- The bug does NOT appear in Chrome DevTools mobile emulator
- The bug only appears on real mobile devices (iOS Safari, Chrome on Android)
- This indicates a mobile‑specific CSS compatibility issue, not a missing file or broken path

<b>Root Cause Identified</b>

- Inside style.scss, the .program-header block uses:
  `background-attachment: fixed;`

Mobile browsers do not support background-attachment: fixed.
When they encounter it, they often drop the entire background image, leaving only the background color.

<b>Code Location</b>

The problematic code is inside:<br>
`.program-header {
  background: url(../img/2024-H2-Launch-Celebration-min.png) #0093b5 no-repeat top fixed;`
}

I split this shorthand into explicit properties to make the fix clearer:<br>
`background-image:url(../img/2024-H2-Launch-Celebration-min.png);`<br>
`background-color: $main-blue;`<br>
`background-repeat: no-repeat;`<br>
`background-position: top;`<br>
`background-size: cover;`<br>
`background-attachment: fixed;`<br>

<b>Fix Implemented</b> <br>
Added a mobile override to disable the unsupported fixed attachment:<br>
`@media (max-width: 768px) {
  .program-header {
    background-attachment: scroll;
    background-position: top center;
  }
}`<br>
This restores the hero image on real mobile devices.
