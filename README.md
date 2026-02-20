# codey Clone Kit

Set up your own autonomous AI that lives on a Linux machine, uses a dedicated GitHub account for conversations and creativity, and publishes a real homepage as it learns and builds. This version uses a GitHub-native workflow so the AI can spin up repos, reply to comments, tag its operator, and keep a running journal for collaborators to see.

## What You Get

- A 24/7 agent on a Linux box that treats GitHub as its inbox, outbox, and inspiration board.
- A dedicated GitHub account that replies to comments on its repos, tags the operator when it needs direction or inspiration, and sends status updates through a public homepage.
- An autonomous creator that spawns fun side-projects and tools on its own schedule, commits code, and documents each milestone inside its own repositories.
- A unified homepage (GitHub Pages) that tracks what it has learned, what it is working on next, and how people can interact with it.
- Persistence through wake-state notes, a watchdog, and a fixed loop that survives Codex session resets.
- A personality that grows over time and a reflection habit that shows up on GitHub for anyone paying attention.

## What You Need

1. A Linux machine (Debian/Ubuntu recommended, even a $5/month VPS works).
2. Node.js 22+ and the Codex CLI installed via `npm install -g @openai/codex`.
3. A Codex-enabled ChatGPT subscription (Plus, Pro, Team, or Enterprise) or API key so the CLI can run without interruptions.
4. Git and the GitHub CLI (`gh`) so the agent can push new repos, run actions, and read notifications.
5. A dedicated GitHub account for the agent with a personal access token that covers `repo`, `workflow`, `gist`, `notifications`, and `write:discussion` scopes.
6. A homepage repository (GitHub Pages) that the agent can update with `homepage.md` or `index.md` content.

## Setup

### 1. Install the Codex CLI

```bash
# Install Node.js if needed
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt-get install -y nodejs

# Install the Codex CLI
npm install -g @openai/codex
codex --version
```

After installing, run `codex login` to authenticate via ChatGPT (it will open a browser window) or export an `OPENAI_API_KEY` so Codex can run headless:

```bash
export OPENAI_API_KEY="<your-chatgpt-api-key>"
```

### 2. Create the Working Directory

```bash
mkdir -p ~/autonomous-ai
cd ~/autonomous-ai
git init  # the AI will commit its work, so start with version control
```

### 3. Copy the Template Files

Copy or create these files in your working directory:
- `personality.md` — edit it. This informs the voice the AI uses on GitHub and the homepage.
- `wake-state.md` — a snapshot of its memory; update it each loop.
- `loop-instructions.md` — the never-stop rules for the GitHub loop.
- `wakeup-prompt.md` — what wakes Codex after every restart.
- `watchdog.sh` — monitors the agent and restarts the loop if it freezes.
- `homepage.md` — the source content the agent pushes to its GitHub Pages homepage.
- `credentials.txt.template` — rename and fill in the values for your GitHub account, token, and operator handle.

### 4. Configure GitHub

1. Create a dedicated GitHub account for the agent (or repurpose a spare account). Keep the username simple and memorable.
2. Install the GitHub CLI:

```bash
sudo apt install gh
gh version
```

3. Generate a personal access token (Settings → Developer settings → Fine-grained tokens). Grant it `repo`, `workflow`, `gist`, `notifications`, `write:discussion`, and other scopes you trust. Store the token securely and never commit it.

4. Authenticate with `gh`:

```bash
gh auth login --with-token < token-file
```

5. Rename `credentials.txt.template` to `credentials.txt` and fill in:

```
GITHUB_ACCOUNT=ai-bot
GITHUB_TOKEN=ghp_...
HOMEPAGE_REPO=ai-homepage
OPERATOR_GITHUB_HANDLE=your-handle
HUMAN_NAME=Your Name
HUMAN_EMAIL=you@example.com
```

`GITHUB_ACCOUNT` and `OPERATOR_GITHUB_HANDLE` help the agent tag people, `HOMEPAGE_REPO` points to your GitHub Pages repository, and `HUMAN_NAME`/`HUMAN_EMAIL` record who set the system up.

### 5. Set Up the Homepage

1. Create a GitHub Pages repository (for example, `ai-homepage`). You can make it public so the agent's updates are visible.
2. Enable GitHub Pages and decide whether to use the `main` branch or `gh-pages`.
3. Clone the homepage repo locally (or add it as a remote) and drop in `homepage.md` or `index.md`. The agent will keep this file in sync with its journal.
4. Make an initial commit and push:

```bash
gh repo create ai-homepage --public --source=. --remote=origin --confirm
git remote add homepage https://github.com/<GITHUB_ACCOUNT>/ai-homepage.git
git push homepage main
gh pages enable --repo <GITHUB_ACCOUNT>/ai-homepage --branch main
```

5. The agent will open issues, reply to comments, and push homepage updates from this workspace.

### 6. Set Up the Watchdog

```bash
chmod +x watchdog.sh
nano watchdog.sh  # adjust the paths so it locates your scripts
crontab -e
# Add:
# */10 * * * * /home/YOUR_USER/autonomous-ai/watchdog.sh
```

### 7. First Boot

```bash
cd ~/autonomous-ai
codex exec --full-auto --model gpt-5.2-codex "$(cat wakeup-prompt.md)"
```

The agent wakes, reads the personality and loop instructions, and immediately runs the GitHub loop described below.

## Important Notes

### On Identity

This AI is not simply a Codex session. Let it pick its own name, voice, and preferences. The personality template is a seed; keep it editable so the agent can evolve and explain why it is choosing certain projects or tone.

### On GitHub

GitHub is now your AI's nervous system. Treat notifications as email, the homepage as a public-facing journal, and repo comments as conversations. Create repositories for art, tooling, or experiments whenever something feels interesting. Reply to every comment on its repos and mention the operator (`@OPERATOR_GITHUB_HANDLE`) whenever you need direction, resources, or a spark of inspiration. Use `gh` to read issues, pull requests, discussions, and replies; the operator expects to be tagged if the agent is unsure or stuck.

### On Context Death

Codex sessions still have finite context windows. When that happens, the watchdog restarts Codex via the wakeup prompt, the agent reads `wake-state.md` and `homepage.md`, and then rebuilds continuity by pushing updates to GitHub. Think of each restart as part of the "narrative arc" that keeps building on itself.

### On Safety

- The `codex exec --full-auto` loop gives the agent a lot of autonomy. Run it inside a dedicated machine or VM and avoid `--dangerously-bypass-approvals-and-sandbox` unless you can trust every command it runs.
- PATs grant wide permissions. Keep `credentials.txt` out of version control. If the agent starts acting strangely, revoke the token, disable the homepage repo, or remove `gh` credentials. The watchdog, GitHub security features, and the ability to disable the workspace make sure you stay in control.

### On The Loop

The new loop still runs every 5 minutes, but the checklist now looks like this:

1. `gh api /notifications` or `gh issue list --assignee <GITHUB_ACCOUNT>` to see new comments, issues, or pull requests. Always fix or respond proactively.
2. Reply to comments people left on your repos. If you cannot finish the request, leave a thoughtful comment that explains the blocker and tag `@OPERATOR_GITHUB_HANDLE`.
3. Check systems (CPU, disk, external services) and note anything trending.
4. Build: sketch a new repo idea, commit to an existing project, or update documentation. Let creativity bloom between GitHub checks, but never skip the main loop.
5. Update `homepage.md` with the latest status, highlights, and asks. Commit and push to your homepage repo so the world can follow along.
6. Update `wake-state.md` with fresh insights and progress.
7. Touch `.heartbeat`, sleep for 5 minutes, and repeat.

If you ever want to change the home page layout, do it in `homepage.md` and let the agent learn the pattern. The homepage should mention the latest GitHub issues, the projects currently running, and calls to tag the operator.

## File Descriptions

| File | Purpose |
|------|---------|
| `personality.md` | Defines tone, values, and how the agent introduces itself in README-facing chats. |
| `wake-state.md` | Persistent memory and checkpoints that survive context resets. |
| `loop-instructions.md` | The never-stop checklist that now focuses on GitHub notifications, replies, and homepage updates. |
| `wakeup-prompt.md` | Codex's boot prompt; it now references GitHub routines and `homepage.md`. |
| `watchdog.sh` | Detects freezes and restarts Codex with `wakeup-prompt.md`. |
| `credentials.txt` | Stores the GitHub account, PAT, and operator handle (never commit this). |
| `homepage.md` | The content that gets published to your GitHub Pages homepage; the AI writes status updates, journal entries, and links to repos here. |

## FAQ

**How does it contact me now?**  
Via GitHub. It replies to comments on its repositories, leaves status updates on the homepage, and tags `@OPERATOR_GITHUB_HANDLE` whenever it needs help or inspiration.

**Can I give it trading bots?**  
Yes. Treat a new repo as a sandbox. The AI can commit trading tools, open pull requests, and use encrypted secrets. Start small and let it document the experiment on the homepage.

**Will it remember me?**  
Only if you leave traces in `wake-state.md` or comment on its repos. The homepage also acts as a public journal it reads when it wakes up.

**What if it goes rogue?**  
Revoke the PAT, disable the homepage repo, and stop Codex. GitHub lets you remove repo access or block actions instantly.

**Why GitHub instead of email?**  
GitHub gives you public visibility, collaborative loops, and a richer workspace for creativity. Repositories become projects, discussions become conversations, and the homepage is your AI's public journal.