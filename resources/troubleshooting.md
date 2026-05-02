# Troubleshooting — Common Issues and Fixes

This covers the most common problems that come up during the workshop, on both Mac and Windows.

**Rule #1:** Copy the exact error message. Then ask Claude: "I'm getting this error. What does it mean and how do I fix it?" — that's usually faster than Googling.

**Rule #2:** If something worked yesterday and doesn't today, try restarting your terminal first. Many issues are stale sessions.

---

## Installation Issues

### "command not found: brew" (Mac)

**What's happening:** Homebrew installed but isn't in your PATH.

**Fix:**
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
brew --version
```

If that doesn't work, also try:
```bash
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

(Some older Macs install Homebrew at `/usr/local/bin/` instead of `/opt/homebrew/bin/`)

---

### "command not found: claude"

**What's happening:** Claude Code either isn't installed or npm's bin folder isn't in your PATH.

**Fix:**
```bash
# Reinstall Claude Code
npm install -g @anthropic-ai/claude-code

# If that fails, find where npm installs global packages
npm config get prefix
```

Take the output of that second command and add `/bin` to the end. That path needs to be in your PATH.

For Mac:
```bash
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
claude --version
```

---

### "xcrun: error: invalid active developer path" (Mac)

**What's happening:** Xcode Command Line Tools need to be installed or updated.

**Fix:**
```bash
xcode-select --install
```

Follow the popup prompt. Restart terminal after it finishes.

---

### WSL2 won't install / "Virtual Machine Platform feature not available" (Windows)

**What's happening:** Virtualization is disabled in your BIOS.

**Fix:** Search Google for your laptop model + "enable virtualization BIOS". Different manufacturers put this in different places. Common paths:
- Dell: BIOS > Virtualization Support > Enable
- Lenovo: BIOS > Security > Virtualization
- HP: BIOS > Advanced > Device Configurations > Virtualization Technology
- Surface: Held by Microsoft, usually enabled by default — check Windows Features instead

---

### Ubuntu keeps crashing in WSL2 (Windows)

**Fix:**
Open PowerShell as Administrator and run:
```powershell
wsl --update
wsl --shutdown
```

Then reopen Windows Terminal and select Ubuntu.

---

## Claude Code Issues

### Claude Code opens but immediately exits / "Authentication required"

**What's happening:** You need to log in with your Claude.ai account.

**Fix:**
```bash
claude
# It will prompt you to log in — follow the URL it provides
# After logging in, try again
```

Make sure your Claude.ai account is on **Claude Max 5x ($100/mo)** at minimum. Pro tier ($20/mo) technically has Claude Code access but rate limits will hit fast during a workshop day. Free tier won't work.

---

### "Claude Code requires a paid subscription"

**What's happening:** Your account isn't on a plan that includes Claude Code, or you're on Pro and have hit the rate limit.

**Fix:** Go to **claude.ai** in a browser > Settings > Plans > Upgrade to **Max 5x ($100/month)** at minimum. Max 20x ($200/month) is recommended for power users. Then restart Claude Code.

---

### Claude Code is extremely slow to respond

**What's happening:** Usually a network issue, or Claude's API is having a slow moment.

**Fix:**
1. Check **status.anthropic.com** — if there's an incident, wait for it to resolve
2. Try a fresh terminal session
3. Check your internet connection (Claude Code makes API calls for every response)

---

### "Permission denied" when running commands

**Mac Fix:**
Prefix the command with `sudo`:
```bash
sudo npm install -g @anthropic-ai/claude-code
```
(You'll be asked for your Mac password)

**Windows/WSL2 Fix:**
Same thing:
```bash
sudo apt install [package-name]
```
(You'll be asked for your Linux password)

---

### Claude Code says it doesn't have access to my files

**What's happening:** You're running Claude in a directory without the right permissions, or you haven't configured the filesystem MCP.

**Fix:**
1. Make sure you're running `claude` from inside your project directory: `cd ~/Documents/agent-native-os && claude`
2. Check that your CLAUDE.md is in that folder: `ls CLAUDE.md`
3. For broader file access, configure the filesystem MCP in your settings.json (see the template in `templates/settings/`)

---

## MCP Server Issues

### "MCP server failed to start"

**What's happening:** The package didn't fetch, there's a configuration error, or a dependency is missing.

**Fix:**
```bash
# Confirm the server is registered
claude mcp list

# If it is, remove and re-add to force a fresh install
claude mcp remove brave-search
claude mcp add brave-search
# (replace with your failing MCP name)

# Then restart Claude Code
claude
```

If it still fails, check the exact error with:
```bash
CLAUDE_DEBUG=1 claude
```
This shows verbose output including MCP startup errors.

---

### Gmail MCP won't authenticate

**What's happening:** The OAuth credentials file is wrong, missing, or the OAuth scopes aren't set up correctly.

**Fix:**
1. Check the credentials file exists: `ls ~/.claude/credentials/`
2. Verify the path in your settings.json matches exactly
3. Delete any cached auth tokens (look in `~/.config/` for Google-related folders)
4. Re-run the authentication flow: start `claude`, try to use Gmail, follow the browser prompt

---

### MCP is installed but Claude doesn't seem to use it

**What's happening:** Usually a JSON syntax error in settings.json, or the MCP name doesn't match.

**Fix:**
```bash
# Validate your settings.json
cat ~/.claude/settings.json | python3 -m json.tool

# If python3 isn't available:
node -e "JSON.parse(require('fs').readFileSync('$HOME/.claude/settings.json', 'utf8'))" && echo "Valid JSON" || echo "JSON syntax error"
```

If you see an error, find the line with the problem and fix it. Common issues: missing comma, unclosed bracket, extra comma at end of list.

---

### "op: command not found" when Claude tries to resolve secrets

**What's happening:** The 1Password CLI isn't installed or isn't in your PATH.

**Mac Fix:**
```bash
brew install 1password-cli
op --version
```

**Windows/WSL2 Fix:** Follow the CLI installation steps in `setup/windows/prerequisites.md`.

---

### 1Password CLI asks for password every time

**What's happening:** Your 1Password session isn't being cached properly.

**Mac Fix:**
Open 1Password app > Settings > Developer > Enable "Integrate with 1Password CLI". This allows the CLI to use your unlocked app session instead of asking for credentials separately.

---

## Obsidian Issues

### Claude can't find my Obsidian vault

**What's happening:** The path in your CLAUDE.md doesn't match where the vault actually is.

**Fix:**
```bash
# Find your vault — look in common locations
ls ~/Documents/
ls ~/
ls ~/Obsidian/

# On Windows, your Obsidian vault is on the Windows side:
ls /mnt/c/Users/YourWindowsName/Documents/
```

Once you find it, update the path in your CLAUDE.md exactly.

---

### Obsidian notes have broken formatting after Claude edits them

**What's happening:** Claude added or modified markdown in an unexpected way.

**Fix:** Open the file in a text editor (not just Obsidian) to see the raw markdown. Claude usually writes valid markdown, but occasionally it will indent things differently or use a heading level you didn't expect.

Set a rule in your CLAUDE.md: "When writing to Obsidian notes, use H2 (##) for sections, H3 (###) for subsections. Don't change existing heading structure."

---

## Git and GitHub Issues

### "Permission denied (publickey)" when pushing to GitHub

**What's happening:** Git is trying to use SSH authentication but you don't have an SSH key set up. Since we're using HTTPS, the fix is to make sure git uses HTTPS.

**Fix:**
```bash
# Use GitHub CLI to authenticate (HTTPS-based)
gh auth login
# Choose HTTPS, authenticate via browser

# Set git to use the GitHub CLI for credentials
gh auth setup-git
```

---

### "Your branch is behind origin"

**What's happening:** The remote repo has changes you don't have locally.

**Fix:**
```bash
git pull
```

If you have local changes that conflict:
```bash
git status  # See what's changed
git stash   # Temporarily set aside your changes
git pull    # Get the remote changes
git stash pop  # Bring your changes back
```

---

## Scheduled Task Issues

### Cron job isn't running (Mac/WSL2)

**Fix:**
1. Verify cron syntax at **crontab.guru** — paste your cron expression and confirm it does what you think
2. Check if cron is running: `ps aux | grep cron`
3. Check cron logs:
   - Mac: `grep CRON /var/log/system.log | tail -20`
   - WSL2: `/var/log/syslog | grep CRON`
4. Make sure the script is executable: `chmod +x ~/your-script.sh`
5. Use absolute paths in your script — cron doesn't inherit your shell's PATH

---

### Script runs manually but fails in cron

**What's happening:** Cron runs with a minimal environment — no PATH, no shell variables, no 1Password session.

**Fix:** At the top of your script, explicitly set everything:
```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/Users/yourname"

# For 1Password
eval $(op signin --raw 2>/dev/null)
```

---

## Still Stuck?

1. **Copy the full error message** — the whole thing, not just the last line
2. **Ask Claude**: Open a terminal, type `claude`, and paste the error: "I'm getting this error: [paste]. I was trying to [describe what you were doing]. How do I fix it?"
3. **Post in community Slack** with: your platform (Mac/Windows), which step you're on, and a screenshot of the error
4. **Check if it's a known issue** on the workshop support channel

We promise most issues have been seen before and have solutions. Don't spend more than 10 minutes stuck before asking — that's what the community is for.
