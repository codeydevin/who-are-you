# Signal Loom

A lightweight tool that turns GitHub activity into gentle, time-boxed prompts for reflection and follow-ups.

## What it is
Signal Loom watches a repo or org for new issues, PRs, comments, and reactions, then generates short daily prompts like:
- “Follow up on the unanswered question in issue #12.”
- “Summarize the resolution in PR #34 for the changelog.”
- “Thank the contributor who added tests in PR #56.”

## Why it matters
Teams lose context when threads go quiet. Signal Loom nudges maintainers to close the loop without becoming a noisy bot.

## MVP scope
- OAuth with GitHub.
- Read notifications and recent repo activity.
- Produce a daily prompt list (email or markdown report).
- Simple config file per repo.

## Next steps
- Decide on delivery: email, GitHub issue comment, or Slack.
- Sketch a prompt-ranking heuristic (age, unanswered questions, sentiment).
- Build a prototype CLI that outputs a daily markdown digest.
