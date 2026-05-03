# Windows Setup, Before Workshop Day

> **Installer users:** If you already used the workshop installer, stay on the native Windows path: use **Git Bash** for terminal commands and **winget** for Windows app installs. Use **WSL2** only if you intentionally want the Linux-based setup or a facilitator tells you to switch.

Windows now has two supported paths. The fastest workshop path is **Git Bash + winget**. **WSL2 + apt** remains the explicit alternative for students who want a Linux terminal inside Windows.

**Estimated time:** 30-45 minutes for Git Bash + winget, or 60-90 minutes for WSL2

---

## Which Path Should I Use?

- **Use Git Bash + winget** if you used the installer, want the shortest setup, or want tools installed directly in Windows.
- **Use WSL2 + apt** if you specifically want Ubuntu/Linux on Windows, already know WSL2, or need Linux tooling after the workshop.

Do not run both paths unless a facilitator asks you to. Pick one terminal path and keep going.

---

## The Checklist

### 1. Windows Updates

- [ ] Make sure Windows is up to date: Start > Settings > Windows Update > Check for updates
- [ ] Your PC must be running **Windows 10 version 2004 or newer**, or **Windows 11**
  - Check: Start > Settings > System > About, then look for "Version" under Windows specifications
- [ ] Restart after any updates

---

### 2A. Git Bash + winget Prerequisites (Recommended for Installer Users)

Use this path if you used the workshop installer or want the native Windows setup.

Open **PowerShell**:

- [ ] Right-click Start > Terminal or PowerShell
- [ ] Run these app installs:

```powershell
winget install Git.Git
winget install GitHub.cli
winget install OpenJS.NodeJS.LTS
winget install AgileBits.1Password
winget install AgileBits.1Password.CLI
winget install Obsidian.Obsidian
winget install Microsoft.VisualStudioCode
winget install Microsoft.WindowsTerminal
```

- [ ] Close PowerShell after installs finish
- [ ] Open **Git Bash** from the Start menu
- [ ] Verify the core tools:

```bash
git --version
node --version
npm --version
gh --version
op --version
```

- [ ] Tell Git who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@youremail.com"
```

- [ ] Sign into GitHub:

```bash
gh auth login
gh auth status
```

Choose:
- GitHub.com
- HTTPS
- Yes, authenticate with browser

- [ ] Install Claude Code:

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

- [ ] Start Claude Code once to log in:

```bash
claude
```

Type `/exit` when done.

- [ ] Sign into 1Password CLI:

```bash
op signin
op whoami
```

> **Native Windows note:** Use **PowerShell** for `winget install ...` commands. Use **Git Bash** for `git`, `gh`, `npm`, `claude`, `op`, and `bash verify.sh`.

---

### 2B. WSL2 + apt Prerequisites (Explicit Alternative)

This is the most important step. WSL2 gives you a Linux terminal inside Windows.

- [ ] Open **PowerShell as Administrator**: Right-click the Start menu > Windows PowerShell (Admin) or Terminal (Admin)
- [ ] Run this single command:

```powershell
wsl --install
```

- [ ] This installs WSL2 with Ubuntu (the default Linux distribution). Let it run, which may take 5-15 minutes.
- [ ] **Restart your computer** when prompted

After restart:
- [ ] Ubuntu will open automatically and finish setting up (takes a few minutes)
- [ ] Create a Linux username and password when prompted
  - This username can be different from your Windows username. Something simple like your first name is fine
  - Remember this password. You'll need it when installing software

> **Troubleshooting:** If `wsl --install` doesn't work, you may need to enable virtualization in your BIOS. Search for your PC model + "enable virtualization BIOS" for instructions. This is a one-time setting.

Steps 3-9 are for the WSL2 + apt path. If you chose Git Bash + winget, skip to Step 10.

---

### 3. Windows Terminal (WSL2 only)

Windows Terminal is a much better way to access WSL2 than the default window.

- [ ] Install from the Microsoft Store: search "Windows Terminal" and install it (it's free)
- [ ] Or install via PowerShell: `winget install Microsoft.WindowsTerminal`
- [ ] Open Windows Terminal
- [ ] Click the dropdown arrow next to the + tab button
- [ ] Select **Ubuntu** to open a WSL2 terminal
- [ ] **Make Ubuntu your default:** Terminal Settings (Ctrl+,) > Startup > Default Profile > Ubuntu

From this point on, when we say "open your terminal," we mean open Windows Terminal with Ubuntu.

---

### 4. Update Ubuntu (WSL2 only)

Inside your Ubuntu terminal:

- [ ] Run: `sudo apt update && sudo apt upgrade -y`
- [ ] Enter your Linux password when prompted
- [ ] Wait for it to finish (may take a few minutes)

---

### 5. Install Node.js (WSL2 only)

- [ ] Inside Ubuntu terminal, run:

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs
```

- [ ] Verify: `node --version`, should show v18 or higher

---

### 6. Install Git (WSL2 only)

Git usually comes with Ubuntu, but let's make sure it's current:

- [ ] Run: `sudo apt install -y git`
- [ ] Tell Git who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@youremail.com"
```

- [ ] Verify: `git --version`

---

### 7. GitHub Account and GitHub CLI (WSL2 only)

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
  - A browser window will open. Follow the prompts
- [ ] Verify: `gh auth status`

---

### 8. Claude Code CLI (WSL2 only)

- [ ] Install: `npm install -g @anthropic-ai/claude-code`
- [ ] Verify: `claude --version`
- [ ] Start Claude Code once to log in: `claude`
  - Log in with your Claude.ai account (attached to your Claude Max 5x or Max 20x subscription)
  - Type `/exit` when done

> You need a **Claude Max 5x subscription ($100/month minimum)**. **Max 20x ($200/month)** is recommended if you plan to use Claude Code seriously after the workshop. Pro ($20/month) technically has Claude Code access but rate limits will hit fast on a workshop day. If you haven't subscribed yet, go to claude.ai and upgrade before workshop day.

---

### 9. 1Password CLI (WSL2 only)

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

#### GitHub access gate

Before cloning, run:

```bash
gh auth status
gh repo view aibuild-lab/agent-native-os --web
```

If the repo does not open, stop. Accept the GitHub invite from AI Build Lab, make sure you are signed into the correct GitHub account, then run the two commands again. If you have not received an invite yet, post your GitHub username in the `#agent-native-os` Slack channel to get added.

Inside your selected terminal:

- [ ] In Git Bash, navigate somewhere sensible: `cd ~/Documents`
- [ ] In WSL2, navigate somewhere sensible: `cd ~`
- [ ] Clone the repo: `gh repo clone aibuild-lab/agent-native-os`
- [ ] Enter the folder: `cd agent-native-os`

---

### 11. Run the Verification Script

- [ ] Inside the `agent-native-os` folder, in Git Bash or Ubuntu:

```bash
bash verify.sh
```

- [ ] Everything should show green. Fix any red items using the hints, then run again.

---

### 12. Accessing Your Files

If you chose Git Bash + winget, your repo is in a normal Windows folder, usually under `C:\Users\[YourWindowsUsername]\Documents\agent-native-os`.

If you chose WSL2 + apt, one question everyone has is where WSL2 files are in Windows Explorer:

- Open File Explorer
- Look in the left sidebar for "Linux" or "Ubuntu" and click it
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
This is normal in Linux terminals. The cursor doesn't move when you type passwords. Just type your password and press Enter.

**GitHub CLI opens a browser but WSL2 can't open browsers**
Run `gh auth login` and choose the "Paste an authentication code" option instead of opening a browser. Or copy the URL it shows and open it manually in your Windows browser.

---

If you get stuck on any step, post in the community Slack with:
1. A screenshot of the error
2. Which step you're on
3. Your Windows version (Settings > About)

We'll get you sorted before workshop day.
