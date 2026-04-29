# Mac Setup, Before Workshop Day

Complete this checklist at least one day before the workshop. Each step links to exactly what you need. If something breaks or confuses you, post in the community Slack. We check it regularly in the days before workshop day.

**Estimated time:** 45–60 minutes (most of it is download/install time, not active work)

---

## The Checklist

### 1. Apple ID and macOS Updates

- [ ] Your Mac is running **macOS Ventura (13) or newer** — check under Apple menu > About This Mac
- [ ] All pending system updates are installed
- [ ] You're signed into your Apple ID

> Why this matters: Some tools require newer macOS versions. Outdated systems cause unexpected errors.

---

### 2. Homebrew — Your Mac App Installer

Homebrew is how developers install tools on Mac. Think of it like an App Store for command-line tools. You'll use it to install almost everything else on this list.

- [ ] Open **Terminal** (press Cmd + Space, type "Terminal", hit Enter)
- [ ] Paste this entire line and press Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- [ ] Follow the prompts — it will ask for your Mac password at least once
- [ ] When it finishes, it may show you two commands to run to "add Homebrew to your PATH" — run those too (copy and paste each one)
- [ ] Verify it worked: type `brew --version` and press Enter. You should see a version number.

**If you get an error:** Make sure you have Xcode Command Line Tools installed. Homebrew usually installs these automatically, but if it doesn't: `xcode-select --install`

---

### 3. Node.js

Node.js is the engine that runs Claude Code. You install it once and mostly forget about it.

- [ ] Run: `brew install node`
- [ ] Verify: `node --version` — should show v18 or higher (e.g., `v22.4.0`)

---

### 4. Git

Git is the version control system that keeps track of your files. GitHub is built on top of it.

- [ ] Run: `brew install git`
- [ ] Tell Git who you are (replace with your actual name and email):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@youremail.com"
```

- [ ] Verify: `git --version` — should show a version number

---

### 5. GitHub Account and GitHub CLI

- [ ] Create a free GitHub account at **github.com** (skip if you already have one)
- [ ] Remember your GitHub username and the email address you signed up with
- [ ] Install the GitHub CLI: `brew install gh`
- [ ] Sign in: `gh auth login`
  - Choose: GitHub.com
  - Choose: HTTPS
  - Choose: Yes (authenticate with browser)
  - A browser window will open — follow the prompts to authorize
- [ ] Verify: `gh auth status` — should show your GitHub username

---

### 6. Claude Code CLI

This is the main thing we're building on all day.

- [ ] Install: `npm install -g @anthropic-ai/claude-code`
- [ ] Verify: `claude --version` — should show a version number
- [ ] Start Claude Code once to trigger setup: `claude`
  - It will prompt you to log in. Use your Claude.ai account (the one attached to your Claude Max 5x or Max 20x subscription)
  - Follow the browser prompts
  - Type `/exit` to close Claude Code after you've logged in

> You need a **Claude Max 5x subscription ($100/month minimum)** for this workshop. **Max 20x ($200/month)** is recommended if you plan to use Claude Code seriously after the workshop. Pro ($20/month) technically has Claude Code access but rate limits will hit fast on a workshop day. If you haven't subscribed yet, go to claude.ai and upgrade before workshop day.

---

### 7. 1Password (Password Manager + Secrets Storage)

1Password is how we store API keys and secrets safely. The CLI version is what lets Claude Code access them without you typing passwords repeatedly.

- [ ] Install 1Password app: `brew install --cask 1password`
- [ ] Create or sign into your 1Password account at **1password.com**
- [ ] Install 1Password CLI: `brew install 1password-cli`
- [ ] Link the CLI to your 1Password app:
  - Open 1Password app
  - Go to Settings > Developer
  - Enable "Integrate with 1Password CLI"
- [ ] Verify: `op whoami` — should show your 1Password account email

---

### 8. Clone This Repo

- [ ] Open Terminal and navigate to where you want the folder:

```bash
cd ~/Documents
```

- [ ] Clone the repo (replace `[your-username]` if needed):

```bash
gh repo clone 8Dvibes/agent-native-os
```

- [ ] Enter the folder: `cd agent-native-os`

---

### 9. Run the Verification Script

- [ ] Inside the `agent-native-os` folder, run:

```bash
bash verify.sh
```

- [ ] Everything should show a green checkmark. If something shows red, fix it using the hint it provides, then run `verify.sh` again.

---

### 10. Optional but Recommended

These aren't required for workshop day, but we'll touch them during the workshop:

- [ ] **Obsidian** (knowledge base app): `brew install --cask obsidian` — free at obsidian.md
- [ ] **Visual Studio Code** (code editor): `brew install --cask visual-studio-code`
- [ ] **Ghostty** (a better terminal): Download at ghostty.org — fast, clean, highly recommended

See `setup/mac/recommended-apps.md` for more.

---

## Common Pre-Workshop Issues on Mac

**"command not found: brew"**
Homebrew installed but isn't on your PATH. Run: `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc && source ~/.zshrc`

**"permission denied" when installing things**
You may need to use `sudo` before some commands, or your Mac may need your administrator password.

**Claude Code asks me to log in but I don't have an account**
Go to claude.ai and sign up. Then upgrade to **Max 5x ($100/month)** at minimum (or **Max 20x ($200/month)** for power users) under Settings > Plans.

**"xcrun: error: invalid active developer path"**
Run: `xcode-select --install` and follow the prompts.

---

If you hit something not on this list, post it in the community Slack with a screenshot of the error. We'll get you sorted before workshop day.
