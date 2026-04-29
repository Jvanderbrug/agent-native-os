# Windows Setup, Before Workshop Day

Windows takes a few more steps than Mac, but don't let that intimidate you. The key is WSL2 — a lightweight Linux environment that runs inside Windows. Once that's set up, everything else works exactly like the Mac instructions.

**Estimated time:** 60–90 minutes (most of it is installing WSL2 and letting things download)

---

## Why WSL2?

Claude Code and many developer tools are designed for Unix-based systems (Mac and Linux). WSL2 (Windows Subsystem for Linux) gives you a real Linux terminal running inside Windows. You get the best of both worlds: your Windows apps, plus a proper development environment.

You'll do all your Claude Code work inside WSL2. Your Windows files are still accessible, and everything runs side by side.

---

## The Checklist

### 1. Windows Updates

- [ ] Make sure Windows is up to date: Start > Settings > Windows Update > Check for updates
- [ ] Your PC must be running **Windows 10 version 2004 or newer**, or **Windows 11**
  - Check: Start > Settings > System > About — look for "Version" under Windows specifications
- [ ] Restart after any updates

---

### 2. Install WSL2 (Windows Subsystem for Linux)

This is the most important step. WSL2 gives you a Linux terminal inside Windows.

- [ ] Open **PowerShell as Administrator**: Right-click the Start menu > Windows PowerShell (Admin) or Terminal (Admin)
- [ ] Run this single command:

```powershell
wsl --install
```

- [ ] This installs WSL2 with Ubuntu (the default Linux distribution). Let it run — it may take 5–15 minutes.
- [ ] **Restart your computer** when prompted

After restart:
- [ ] Ubuntu will open automatically and finish setting up (takes a few minutes)
- [ ] Create a Linux username and password when prompted
  - This username can be different from your Windows username — something simple like your first name is fine
  - Remember this password — you'll need it when installing software

> **Troubleshooting:** If `wsl --install` doesn't work, you may need to enable virtualization in your BIOS. Search for your PC model + "enable virtualization BIOS" for instructions. This is a one-time setting.

---

### 3. Windows Terminal

Windows Terminal is a much better way to access WSL2 than the default window.

- [ ] Install from the Microsoft Store: search "Windows Terminal" and install it (it's free)
- [ ] Or install via PowerShell: `winget install Microsoft.WindowsTerminal`
- [ ] Open Windows Terminal
- [ ] Click the dropdown arrow next to the + tab button
- [ ] Select **Ubuntu** to open a WSL2 terminal
- [ ] **Make Ubuntu your default:** Terminal Settings (Ctrl+,) > Startup > Default Profile > Ubuntu

From this point on, when we say "open your terminal," we mean open Windows Terminal with Ubuntu.

---

### 4. Update Ubuntu

Inside your Ubuntu terminal:

- [ ] Run: `sudo apt update && sudo apt upgrade -y`
- [ ] Enter your Linux password when prompted
- [ ] Wait for it to finish (may take a few minutes)

---

### 5. Install Node.js

- [ ] Inside Ubuntu terminal, run:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

- [ ] Verify: `node --version` — should show v18 or higher

---

### 6. Install Git

Git usually comes with Ubuntu, but let's make sure it's current:

- [ ] Run: `sudo apt install -y git`
- [ ] Tell Git who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@youremail.com"
```

- [ ] Verify: `git --version`

---

### 7. GitHub Account and GitHub CLI

- [ ] Create a free GitHub account at **github.com** (skip if you already have one)
- [ ] Install GitHub CLI inside Ubuntu:

```bash
type -p curl >/dev/null || sudo apt install curl -y
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh -y
```

- [ ] Sign in: `gh auth login`
  - Choose: GitHub.com
  - Choose: HTTPS
  - Choose: Yes (authenticate with browser)
  - A browser window will open — follow the prompts
- [ ] Verify: `gh auth status`

---

### 8. Claude Code CLI

- [ ] Install: `npm install -g @anthropic-ai/claude-code`
- [ ] Verify: `claude --version`
- [ ] Start Claude Code once to log in: `claude`
  - Log in with your Claude.ai account (attached to your Claude Max 5x or Max 20x subscription)
  - Type `/exit` when done

> You need a **Claude Max 5x subscription ($100/month minimum)**. **Max 20x ($200/month)** is recommended if you plan to use Claude Code seriously after the workshop. Pro ($20/month) technically has Claude Code access but rate limits will hit fast on a workshop day. If you haven't subscribed yet, go to claude.ai and upgrade before workshop day.

---

### 9. 1Password CLI

- [ ] Install 1Password app for Windows from **1password.com** (standard Windows installer)
- [ ] Create or sign into your 1Password account
- [ ] Install 1Password CLI inside Ubuntu:

```bash
curl -sS https://downloads.1password.com/linux/keys/1password.asc | sudo gpg --dearmor --output /usr/share/keyrings/1password-archive-keyring.gpg
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/1password-archive-keyring.gpg] https://downloads.1password.com/linux/debian/amd64 stable main' | sudo tee /etc/apt/sources.list.d/1password.list
sudo apt update && sudo apt install 1password-cli
```

- [ ] Sign in: `op signin`
- [ ] Verify: `op whoami`

> **Note:** 1Password for Windows and 1Password CLI inside WSL2 are separate installs. You need both. The CLI is what lets Claude Code access your secrets.

---

### 10. Clone This Repo

Inside your Ubuntu terminal:

- [ ] Navigate somewhere sensible: `cd ~`
- [ ] Clone the repo: `gh repo clone 8Dvibes/agent-native-os`
- [ ] Enter the folder: `cd agent-native-os`

---

### 11. Run the Verification Script

- [ ] Inside the `agent-native-os` folder:

```bash
bash verify.sh
```

- [ ] Everything should show green. Fix any red items using the hints, then run again.

---

### 12. Accessing Your Files

One question everyone has: where are my WSL2 files in Windows Explorer?

- Open File Explorer
- Look in the left sidebar for "Linux" or "Ubuntu" — click it
- Your home folder is at: `\\wsl$\Ubuntu\home\[yourusername]\`
- You can drag this to your Quick Access bar

You can also access your Windows files from inside WSL2 at `/mnt/c/` (for your C: drive).

---

## Common Pre-Workshop Issues on Windows

**WSL2 won't install: "Virtual Machine Platform feature not available"**
You need to enable virtualization in your BIOS. Search for your laptop/PC model + "enable virtualization BIOS" and follow the manufacturer's instructions.

**Ubuntu won't start after installation**
Open PowerShell as Admin and run: `wsl --update`

**"command not found" for tools you just installed**
Close your terminal completely and reopen it. Some installs require a fresh shell session.

**Can't type my password when running sudo**
This is normal in Linux terminals — the cursor doesn't move when you type passwords. Just type your password and press Enter.

**GitHub CLI opens a browser but WSL2 can't open browsers**
Run `gh auth login` and choose the "Paste an authentication code" option instead of opening a browser. Or copy the URL it shows and open it manually in your Windows browser.

---

If you get stuck on any step, post in the community Slack with:
1. A screenshot of the error
2. Which step you're on
3. Your Windows version (Settings > About)

We'll get you sorted before workshop day.
