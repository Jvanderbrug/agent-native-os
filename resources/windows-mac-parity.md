# Windows Platform Parity Reference
**AI Build Lab - Claude Code Workshop**
**Audience:** Non-technical operators | **Last updated:** 2026-05-03

This document maps every Mac-specific tool and concept in the curriculum to its Windows equivalent, flags gaps, and gives instructors a clear recommended action for each item. Use it as the authoritative reference when prepping Windows students before or during workshop day.

> **Windows path reality check:** If your students used the AI Build Lab installer, they are on native Git Bash + winget. WSL2 is the alternative path. This doc shows both. Do not tell installer students that WSL2 is required for the core workshop unless a specific activity below says WSL2-only.

---

## Table of Contents

1. [Windows Prerequisites (Do Before Workshop Day)](#windows-prerequisites)
2. [Tool-by-Tool Parity Matrix](#tool-by-tool-parity-matrix)
3. [Windows Mode Decision Guide: Git Bash and WSL2](#windows-mode-decision-guide-git-bash-and-wsl2)
4. [Windows-First Recommendations](#windows-first-recommendations)
5. [Quick Reference: Key Path Translations](#quick-reference-key-path-translations)
6. [Instructor Notes](#instructor-notes)

---

## Windows Prerequisites

These are the steps a Windows student must complete **before workshop day** that a Mac student does not need to worry about. Budget 30 to 60 minutes. The curriculum supports two Windows modes:

| Mode | Who uses it | Terminal students open | Package manager | What to tell instructors |
|------|-------------|------------------------|-----------------|--------------------------|
| Native Git Bash + winget | Students who used the AI Build Lab installer | Git Bash | `winget` for apps and CLIs | This is the default workshop path. It covers Git, GitHub CLI, Node, Claude Code, SSH, `ssh-agent`, `chmod`, `~`, dotfiles, and most shell scripts. |
| WSL2 + Ubuntu | Students or instructors who need a fuller Linux environment | Ubuntu in Windows Terminal | `apt` and `npm` inside Ubuntu | This remains supported and is useful for Linux-heavy demos, but it is not required for the core installer path. |

### 1. Choose the Windows mode first

If the student followed the AI Build Lab installer, stay on the native path:

```powershell
winget install --id Git.Git --source winget --accept-package-agreements --accept-source-agreements
winget install --id OpenJS.NodeJS.LTS --source winget --accept-package-agreements --accept-source-agreements
winget install --id GitHub.cli --source winget --accept-package-agreements --accept-source-agreements
```

Then have the student open **Git Bash**, not PowerShell or Command Prompt, for workshop terminal work.

Use WSL2 when the student already has it, wants it, or needs a specific Linux-only tool. Do not force WSL2 just to make `chmod`, `ssh`, `ssh-agent`, `~/.zshrc`, Git, GitHub CLI, Node, or Claude Code work.

### 2. Native Git Bash + winget setup

This is the path created by the AI Build Lab installer. It uses Windows-native tools plus Git Bash for Unix-style shell behavior.

**Steps:**
1. Confirm Windows 10 version 2004+ or Windows 11 with `winver`
2. Confirm `winget` works in PowerShell: `Get-Command winget`
3. Install Git, Node.js LTS, and GitHub CLI with `winget`
4. Set `CLAUDE_CODE_GIT_BASH_PATH` to `C:\Program Files\Git\bin\bash.exe`
5. Install Claude Code with Anthropic's Windows installer
6. Add `%USERPROFILE%\.local\bin` to the User PATH
7. Open Git Bash and verify:

```bash
git --version
node --version
npm --version
gh --version
winpty claude --version
ssh -V
ssh-agent -s
chmod --version
```

**Why this matters:** Git Bash provides a Unix-style `HOME`, `~`, `~/.ssh/`, `~/.config/`, shell scripts, OpenSSH, `ssh-agent`, and common GNU/MSYS utilities. It is enough for most workshop flows. Its permission model sits on top of Windows ACLs, so `chmod` works for curriculum commands and Git/SSH expectations, but Windows ACLs still matter for deep hardening.

### 3. Alternative: Enable WSL2 (Windows Subsystem for Linux)

WSL2 gives Windows a real Linux kernel underneath. It is the best match for Linux-first CLI demos and remains the cleanest fallback when a native Windows tool behaves differently.

**Steps:**
1. Open PowerShell as Administrator (right-click Start -> "Windows PowerShell (Admin)")
2. Run: `wsl --install`
3. Restart the computer when prompted
4. On reboot, a terminal window opens automatically to finish Ubuntu setup - create a username and password when asked (this is your Linux username, not your Windows login)
5. Confirm it worked: open PowerShell and run `wsl --status` - you should see "Default Version: 2"

**Minimum Windows version required:** Windows 10 version 2004 (Build 19041) or Windows 11. Run `winver` in the Start menu to check.

**Why this matters:** WSL2 is not just a compatibility layer. It is a full Linux environment. Use it when you need Linux package behavior, Linux file permissions, or exact parity with Mac/Linux shell examples. It is not mandatory for the native Git Bash installer path.

### 4. Install Windows Terminal

The default Command Prompt window is not suitable for this workshop. Windows Terminal is the modern replacement and supports PowerShell and WSL2 profiles. Git Bash can run in its own window or be added as a Windows Terminal profile.

- Download from the Microsoft Store (search "Windows Terminal") or run: `winget install Microsoft.WindowsTerminal`
- For Git Bash students, open Git Bash directly from the Start menu, or add Git Bash as a Windows Terminal profile
- For WSL2 students, set the default profile to "Ubuntu" (the WSL2 instance): Settings -> Startup -> Default profile -> Ubuntu

### 5. Update Ubuntu inside WSL2

After WSL2 is set up, open Ubuntu in Windows Terminal and run:
```bash
sudo apt update && sudo apt upgrade -y
```

### 6. Install Node.js

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Install Windows Node.js LTS with `winget install --id OpenJS.NodeJS.LTS --source winget --accept-package-agreements --accept-source-agreements`. Git Bash can run `node`, `npm`, and `npx` from that install. | Install Node.js inside WSL2 via `nvm`. Do not rely on the Windows Node.js installer for commands running inside Ubuntu. |

Inside Ubuntu (WSL2):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# Close and reopen the terminal, then:
nvm install --lts
node --version   # should show v20.x or higher
```

### 7. Install Claude Code CLI

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Use Anthropic's Windows installer. It installs `claude.exe` under `%USERPROFILE%\.local\bin`. Add that directory to the User PATH and run Claude from Git Bash with `winpty claude` if plain `claude` has an interactive terminal error. | Install with npm inside Ubuntu. Claude Code then runs in the Linux environment and uses Linux paths. |

Once Node.js is installed inside WSL2:
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### 8. Install Git

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Git for Windows is installed by the AI Build Lab installer with `winget`. It includes Git Bash, OpenSSH, `ssh-agent`, `chmod`, and the Unix-style commands used in most workshop steps. | Install Git inside Ubuntu with `apt`. This gives Linux Git against the WSL2 filesystem. |

Inside Ubuntu (WSL2):
```bash
sudo apt install git -y
git --version
```

Then configure identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 9. Generate an SSH key

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Run these commands in Git Bash. Keys live at `~/.ssh/`, which maps to `C:\Users\YourName\.ssh\`. `ssh`, `ssh-keygen`, `ssh-agent`, `ssh-add`, and `chmod` work in Git Bash. | Run the same commands inside Ubuntu. Keys live in the WSL2 Linux home directory and are separate from Windows keys. |

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# Accept all defaults (press Enter three times)
cat ~/.ssh/id_ed25519.pub
# Copy the output and add it to GitHub -> Settings -> SSH Keys
```

### 10. Install GitHub CLI (gh)

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Installed by the AI Build Lab installer with `winget install --id GitHub.cli`. Run `gh auth login` from Git Bash. | Install with `sudo apt install gh -y` inside Ubuntu. Run `gh auth login` there. |

```bash
sudo apt install gh -y
gh auth login
# Choose GitHub.com -> HTTPS -> paste a personal access token, or follow browser flow
```

### Summary Checklist for Windows Students

| Step | Done? |
|------|-------|
| Windows 10 v2004+ or Windows 11 confirmed | |
| Windows mode chosen: Git Bash installer path or WSL2 alternative | |
| Git Bash path: `winget`, Git, Node.js, GitHub CLI, Claude Code installed | |
| Git Bash path: `CLAUDE_CODE_GIT_BASH_PATH` and `%USERPROFILE%\.local\bin` PATH configured | |
| Git Bash path: Git Bash opens and `git`, `node`, `gh`, `ssh`, `ssh-agent`, `chmod`, and `winpty claude` verify | |
| WSL2 path, if used: WSL2 installed (`wsl --install`) | |
| WSL2 path, if used: Ubuntu set up and updated | |
| WSL2 path, if used: Node.js, Claude Code, Git, SSH, and GitHub CLI installed inside Ubuntu | |

---

## Tool-by-Tool Parity Matrix

---

### Terminal (Ghostty / iTerm2 / Terminal.app)

**Mac approach:** Students use Ghostty (the workshop's recommended terminal), or fall back to iTerm2 or the built-in Terminal.app. All are native macOS applications.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Git Bash is the installer-default workshop terminal. It ships with Git for Windows and gives students a `$` prompt, `~`, `~/.ssh/`, `chmod`, OpenSSH, `ssh-agent`, and common Unix-style commands. | Windows Terminal with the Ubuntu profile is the WSL2 terminal. Once WSL2 is configured, it is functionally identical to a Linux terminal for the curriculum. |

**Mode note:** Git Bash works against the Windows home folder (`C:\Users\YourName`) with Unix-style path syntax (`/c/Users/YourName`). WSL2 works against the Ubuntu home folder and uses `/mnt/c/Users/YourName/` to reach Windows files.

**Complexity rating:** Easy for Git Bash. Easy to medium for WSL2, depending on whether Ubuntu is already set up.

**Recommended workshop approach:** Tell installer students to open Git Bash. Tell WSL2 students to open Ubuntu in Windows Terminal. Ghostty-specific features (appearance settings, split panes) have direct Windows Terminal equivalents in the Settings UI.

---

### Claude Code CLI (npm install -g @anthropic-ai/claude-code)

**Mac approach:** Install globally via npm in the native macOS terminal. Runs in zsh or bash. Config lives at `~/.claude/`.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| The AI Build Lab installer uses Anthropic's Windows native installer. Claude runs from Git Bash; use `winpty claude` if Git Bash reports an interactive stdin issue. The Windows home folder contains `~/.claude/` and related config. | Install inside WSL2 using npm. Claude Code is fully supported on Linux/WSL2. The config directory `~/.claude/` exists inside the WSL2 Ubuntu environment. |

**Mode note:** Do not install the wrong copy for the mode you are teaching. Native Git Bash students should use the Windows Claude installer plus Git Bash. WSL2 students should install Node and Claude inside Ubuntu.

**Complexity rating:** Medium. The installation itself is easy; the "which Windows mode am I in?" instruction requires one extra clarification.

**Recommended workshop approach:** Teach both. For the installer cohort, make Git Bash the default and keep `winpty claude` in the Windows sign-in instructions. For WSL2, use the npm install inside Ubuntu.

---

### Claude Desktop App

**Mac approach:** Download from claude.ai, install, launch. The new version includes local Claude Code integration built in. Config syncs with claude.ai account.

**Windows equivalent:** Claude Desktop is available for Windows - download the `.exe` installer from claude.ai. Full feature parity with Mac version as of 2025. The local Claude Code integration works on Windows as of the Claude Desktop 2025 release.

**WSL2 note:** Not applicable. Claude Desktop is a native Windows application and does not need WSL2.

**Complexity rating:** Easy - the Windows installer is a standard .exe, no CLI required.

**Recommended workshop approach:** Teach Mac way. The Windows experience is identical - just a different installer file. No curriculum changes needed.

---

### VS Code + Claude Code Extension

**Mac approach:** Install VS Code from code.visualstudio.com, install the Claude Code extension from the Extensions marketplace, authenticate.

**Windows equivalent:** VS Code for Windows is identical. Install the Claude Code extension the same way. Git Bash students can open a normal Windows project folder in VS Code. If students are working inside WSL2, they should also install the "WSL" extension (by Microsoft) in VS Code so the editor connects to the WSL2 filesystem instead of Windows. When VS Code opens a WSL2 folder, a green "WSL: Ubuntu" badge appears in the bottom-left corner confirming the connection.

**Mode note:** Install VS Code on Windows. Git Bash students can run `code .` from Git Bash. WSL2 students can run `code .` from Ubuntu to open VS Code connected to the WSL2 filesystem.

**Complexity rating:** Easy - the extension marketplace and UI are identical on both platforms.

**Recommended workshop approach:** Teach Mac way. Add one slide or callout box: "Git Bash students: open projects normally or with `code .` from Git Bash. WSL2 students: install the WSL extension and open projects with `code .` from Ubuntu."

---

### Homebrew (Package Manager)

**Mac approach:** Install via the one-liner at brew.sh. Use `brew install <tool>` to add CLI tools. Homebrew installs to `/opt/homebrew/bin/` on Apple Silicon Macs.

**Windows equivalent (native Git Bash + winget):** `winget` (Windows Package Manager) is the installer-default equivalent. Pre-installed on Windows 11; available for Windows 10 via the App Installer. Syntax: `winget install <package-name>`. It installs Windows applications and many CLI tools, including Git, Node.js, and GitHub CLI. Git Bash then exposes those tools in a Unix-style terminal.

**Windows equivalent (inside WSL2):** `apt` (Advanced Package Tool) is the Ubuntu package manager inside WSL2. Use `sudo apt install <package>` for CLI tools that run in the Linux environment. For tools the curriculum installs via Homebrew (like `gh`, `jq`, `tree`), `apt` is the correct replacement inside WSL2.

**Mode note:** Use `winget` for native Git Bash students and `apt` for WSL2 students. Do not mix the two without explaining which environment owns the installed binary.

**Complexity rating:** Easy in Git Bash for installer-managed tools. Easy inside WSL2. Medium if students need to understand both modes at once.

**Recommended workshop approach:** Skip Homebrew for Windows students. Use `winget` on the installer path and `apt` inside WSL2. Provide a side-by-side cheat sheet: "Mac: `brew install X`; Git Bash path: `winget install X` when a Windows package exists; WSL2 path: `sudo apt install X`."

---

### 1Password CLI (op)

**Mac approach:** Install via Homebrew (`brew install 1password-cli`). Use `op` commands to retrieve secrets at runtime. Integrates with the 1Password desktop app for biometric unlock.

**Windows equivalent:** 1Password CLI is available for Windows. Download the `.zip` from 1password.com/downloads/command-line/, extract `op.exe`, and add it to PATH. Git Bash can run `op.exe` if it is on the Windows PATH. The CLI is also available inside WSL2 via the Linux binary.

**WSL2 note:** For scripts that run inside WSL2, install the Linux version of `op` inside WSL2 (download the Linux binary from 1password.com). The Windows `op.exe` is not accessible from inside WSL2 by default. The 1Password desktop app on Windows handles biometric unlock, and the `op` CLI inside WSL2 can connect to it via a socket - but this requires configuring the 1Password app to allow connections from WSL2 (Settings -> Developer -> "Use the SSH agent" and "Integrate with 1Password CLI").

**Git Bash note:** For the native path, prefer the Windows `op.exe` and Git Bash. That avoids the WSL2 bridge unless the student is already on WSL2.

**Complexity rating:** Medium. The CLI itself is the same; the WSL2 bridge setup requires a few extra steps.

**Recommended workshop approach:** Teach both. Share a setup guide for the WSL2 <-> 1Password bridge. If the workshop doesn't heavily rely on automated secret retrieval (i.e., students just paste API keys manually), this can be deferred to post-workshop setup.

---

### macOS Keychain (Security Store for API Keys/Tokens)

**Mac approach:** Use the `security` CLI command or Keychain Access app to store and retrieve secrets. API keys live in the keychain and are retrieved at runtime without appearing in shell config files.

**Windows equivalent:** Windows Credential Manager (built into Windows). Accessible via Control Panel -> Credential Manager, or programmatically via the `cmdkey` CLI. For workshop scripts, the simplest cross-mode approach is a `.env` file in the active project or home folder with restrictive permissions, plus `.gitignore`. Git Bash can run `chmod 600 .env`; WSL2 can run the same command with Linux kernel enforcement. For deeper hardening on native Windows, use Credential Manager or `icacls`.

**WSL2 note:** The Windows Credential Manager is not accessible from inside WSL2 without a third-party bridge. For non-technical workshop students, the practical recommendation is: store API keys in a `.env` file inside WSL2 with `chmod 600`, and add that file to `.gitignore`. This is less secure than a proper keychain but far simpler for a workshop setting.

**Git Bash note:** Native Git Bash does not block the `.env` pattern. It supports `~`, dotfiles, and `chmod` well enough for the workshop. Just remember that Windows ACLs are still the underlying permission system.

**Complexity rating:** Hard. There is no simple, cross-platform equivalent that works identically.

**Recommended workshop approach:** For Windows students in a workshop context, skip the keychain integration and teach the `.env` file approach with `chmod 600` as a reasonable stand-in. Flag this explicitly: "Mac students use Keychain for extra security; Windows students will use a protected `.env` file and `.gitignore`; both approaches keep your key out of git." Revisit proper Credential Manager integration as a post-workshop exercise for students who want to harden their setup.

---

### Tailscale (Mesh VPN)

**Mac approach:** Install Tailscale from the Mac App Store or tailscale.com. Native macOS app with menu bar icon.

**Windows equivalent:** Tailscale for Windows is fully supported. Download the installer from tailscale.com/download/windows. Native Windows app with system tray icon. Feature-complete parity with Mac.

**WSL2 note:** Tailscale on Windows automatically routes traffic for WSL2 connections - no separate installation needed inside WSL2. WSL2 instances can reach Tailscale IPs as long as the Windows Tailscale client is running.

**Complexity rating:** Easy - the Windows client is essentially identical to Mac.

**Recommended workshop approach:** Teach Mac way. The Windows experience is the same. No curriculum changes needed.

---

### Obsidian (Note-Taking)

**Mac approach:** Download from obsidian.md, install, open a vault.

**Windows equivalent:** Obsidian for Windows is fully supported. Download the `.exe` installer from obsidian.md. Feature-complete parity.

**WSL2 note:** Not applicable. Obsidian is a desktop app and runs natively on Windows.

**Complexity rating:** Easy - identical experience on both platforms.

**Recommended workshop approach:** Teach Mac way. No changes needed.

---

### n8n (Workflow Automation)

**Mac approach:** Run locally via `npm install -g n8n` and `n8n start`, or use n8n Cloud. Local installs use the macOS filesystem paths.

**Windows equivalent:** n8n Cloud is identical on any platform (browser-based). For local n8n, there are two workable modes:

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Use the Windows Node.js LTS install and run n8n from Git Bash or PowerShell. This is acceptable for workshop experimentation if paths stay in the Windows home/project folder. | Install inside WSL2 via npm when you want Mac/Linux-like paths and scripts. The experience is the same as Mac once inside Ubuntu. |

**WSL2 note:** Running n8n locally inside WSL2 works well. Access the n8n UI in a Windows browser at `http://localhost:5678` - WSL2 automatically forwards ports to Windows localhost.

**Complexity rating:** Easy for Cloud; Medium for local because students must keep the terminal mode and file paths consistent.

**Recommended workshop approach:** Use n8n Cloud for the workshop to eliminate the local install complexity. This is platform-agnostic and removes WSL2 from the equation entirely for n8n.

---

### Node.js / npm

**Mac approach:** Install via nvm (`curl -o- .../install.sh | bash`) or Homebrew. Lives at `/opt/homebrew/bin/node` or `~/.nvm/versions/node/...`.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Install Windows Node.js LTS with `winget`. Git Bash can run `node`, `npm`, and `npx` from that install. This is the AI Build Lab installer path. | Install via `nvm` inside WSL2. Do not use the Windows Node.js installer for commands that run inside Ubuntu. |

**Mode note:** Node.js installed inside WSL2 is isolated from Node.js installed on Windows. Pick one mode for the student and verify commands inside that mode's terminal.

**Complexity rating:** Easy in Git Bash when installed by winget. Easy inside WSL2. Medium if students install it in one mode and run commands in the other.

**Recommended workshop approach:** For installer students, use winget Node and Git Bash. For WSL2 students, use nvm inside Ubuntu.

---

### Git + GitHub CLI (gh)

**Mac approach:** Git is pre-installed on Mac (via Xcode Command Line Tools). `gh` installed via Homebrew. Both run in the native terminal.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Install Git for Windows and GitHub CLI with winget. Run `git`, `ssh`, `ssh-agent`, and `gh auth login` in Git Bash. This is the installer-default path. | Install both inside WSL2: `sudo apt install git gh`. Authentication with `gh auth login` works identically inside Ubuntu. |

**WSL2 note:** If students use VS Code with the WSL extension, Git operations via the VS Code UI (Source Control panel) work correctly against the WSL2 filesystem.

**Complexity rating:** Easy in Git Bash. Easy inside WSL2.

**Recommended workshop approach:** Teach the same Git and `gh` commands, but name the terminal first: Git Bash for installer students, Ubuntu for WSL2 students.

---

### MacWhisper (Local Speech-to-Text)

**Mac approach:** Download MacWhisper from goodsnooze.gumroad.com. Native macOS app. Uses OpenAI's Whisper model locally. Produces transcripts from audio/video files or live microphone.

**Windows equivalent:** No direct Windows equivalent with the same polished UI. Options:
- **Whisper.cpp for Windows** - command-line only, requires compilation or pre-built binaries. Suitable for technical users, not non-technical operators.
- **OpenAI Whisper via Python inside WSL2** - install with `pip install openai-whisper` inside WSL2, run `whisper audiofile.mp3`. Functional but command-line only.
- **Faster-Whisper Desktop** (free, Windows GUI) - open-source, available at github.com/Const-me/Whisper. Closest UI equivalent to MacWhisper on Windows.
- **Whisper Transcription (Microsoft Store)** - unofficial Windows Whisper GUI app, paid, similar workflow to MacWhisper.

**WSL2 note:** Python Whisper can be run inside WSL2. For non-technical operators, the CLI experience is a meaningful friction increase compared to MacWhisper's drag-and-drop interface.

**Complexity rating:** Hard - no polished Windows equivalent with the same UX as MacWhisper.

**Recommended workshop approach:** Use the cloud alternative: the Whisper API via n8n or a simple Python script, which works identically on all platforms. For students who need local transcription, recommend Faster-Whisper Desktop as the closest Windows match. Flag this in workshop materials as "Mac students have an easier path here."

---

### Downie 4 (Video Downloader)

**Mac approach:** Downie 4 from software.charliemonroe.net - native macOS app, drag a URL in, get the video out. Simple GUI for non-technical users.

**Windows equivalent:**
- **yt-dlp** (open source CLI) - install with `winget install yt-dlp.yt-dlp` for Git Bash students or `sudo apt install yt-dlp` inside WSL2. Usage: `yt-dlp <URL>`. Feature-complete, cross-platform, but command-line only.
- **YT-DLP GUI** for Windows - several third-party frontends exist (e.g., "Videomass" or "yt-dlg"). Free but less polished than Downie.
- **4K Video Downloader** - paid Windows app (similar price to Downie), GUI-based, close UX match.

**Mode note:** `yt-dlp` in Git Bash downloads to the Windows project folder. `yt-dlp` inside WSL2 downloads to the Linux filesystem. WSL2 students need to either work from there or move files to Windows with `cp /path/to/file /mnt/c/Users/YourName/Downloads/`.

**Complexity rating:** Medium - yt-dlp is easy to learn but the lack of a polished GUI is a step down for non-technical operators.

**Recommended workshop approach:** Teach `yt-dlp` as the universal alternative: Git Bash for installer students, Ubuntu for WSL2 students, and Mac Terminal for Mac students. This is actually a curriculum improvement because it teaches a cross-platform CLI tool instead of a Mac-only GUI. Alternatively, if the workshop just needs students to have video files, provide pre-downloaded files to eliminate platform dependency entirely.

---

### Transloader

**Mac approach:** Transloader (tailored.art/transloader) - Mac app for sending URLs or files to a remote Mac for download. Requires both sender and receiver to be on Apple platforms.

**Windows equivalent:** None. Transloader is Apple-ecosystem-only (uses iCloud for transport). The concept (remote download handoff) can be replicated with other tools, but there is no drop-in Windows equivalent.

**WSL2 note:** Not applicable.

**Complexity rating:** Hard - Apple-only by design.

**Recommended workshop approach:** Skip for Windows students. If the curriculum uses Transloader for a specific workflow, replace it with: (a) a shared cloud folder (Dropbox, Google Drive) where the instructor drops files, or (b) a direct download link the student fetches with `curl` or `wget` from Git Bash or WSL2. Most Transloader use cases in a workshop context are about getting files to students, which has simpler cross-platform alternatives.

---

### Time Machine (Backup - Required Before YOLO Mode)

**Mac approach:** Enable Time Machine in System Settings, point it at an external drive or network share. Claude Code's YOLO/auto-approve mode requires a working backup as a safety prerequisite.

**Windows equivalent:**
- **File History** - built into Windows 10/11 (Settings -> Update & Security -> Backup -> Add a drive). Continuously backs up files in your user folder. Closest equivalent to Time Machine.
- **Windows Backup** (Windows 11) - Settings -> System -> Storage -> Backup. More comprehensive, can back up to OneDrive or external drive.
- **Macrium Reflect Free** - third-party, creates full system images. More robust than File History for full disaster recovery.

**WSL2 note:** File History and Windows Backup do NOT back up the WSL2 Linux filesystem by default. This is an important gap. To back up WSL2 data: manually export with `wsl --export Ubuntu backup.tar` from PowerShell, and back up the resulting .tar file. For workshop purposes, the YOLO prerequisite can be satisfied with File History on Windows + a periodic `wsl --export`.

**Complexity rating:** Medium - Windows has good backup tools, but the WSL2 gap requires an extra step that non-technical users may not know about.

**Recommended workshop approach:** Teach both. For Git Bash students: enable File History or Windows Backup for the Windows user folder where their projects and config live. For WSL2 students: enable File History and show the `wsl --export` command for WSL2 data. Explicitly note: "If your Claude Code config and projects live inside WSL2, Windows Backup doesn't cover them unless you export."

---

### launchd (macOS Daemon System / Scheduled Tasks)

**Mac approach:** Use `launchd` with `.plist` files to schedule scripts. Plists live in `~/Library/LaunchAgents/`. Load with `launchctl load`. This is how the curriculum automates recurring Claude Code tasks.

**Windows equivalent (native Windows):** Task Scheduler - built into Windows, accessible via Start -> "Task Scheduler". GUI-based, can run scripts on a schedule. PowerShell or batch scripts can also be scheduled here.

**Windows equivalent (inside WSL2):** `cron` - the standard Linux scheduler. Enable it in WSL2 with `sudo service cron start`. Add jobs with `crontab -e`. For persistent execution, WSL2 needs to be running (or auto-started via a Windows Task Scheduler task that launches WSL2 on login).

**WSL2 note:** WSL2 does not run in the background by default - it shuts down when no terminals are open. This means WSL2 cron jobs only run while WSL2 is active. Work around this by: (a) having Windows Task Scheduler trigger WSL2 commands (`wsl -e /path/to/script.sh`), or (b) keeping a WSL2 terminal open in the background.

**Complexity rating:** Hard - the Mac launchd system is persistent and automatic; replicating the same behavior on Windows requires combining Windows Task Scheduler and WSL2, which is non-obvious for non-technical users.

**Recommended workshop approach:** For Git Bash students, use Windows Task Scheduler to run Git Bash scripts or PowerShell wrappers. For WSL2 students, teach `cron` inside WSL2 for basic scheduling, and show how to trigger a WSL2 script from Windows Task Scheduler if persistence is needed. Alternatively, for workshop content that uses launchd for automation, migrate those automations to n8n, which is platform-agnostic.

---

### afplay (macOS Audio Playback Command)

**Mac approach:** `afplay soundfile.mp3` in the terminal plays audio. Used in the curriculum for soundboard/voice feedback hooks.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| No direct `afplay`. Call a Windows media player, a PowerShell wrapper, VLC, or skip the hook. Git Bash can launch Windows executables. | No direct `afplay` out of the box. Options include `powershell.exe /c (New-Object Media.SoundPlayer 'C:\path\to\file.wav').PlaySync()`, `mpg123`, or Windows `cmdmp3`/`vlc` called from WSL2. |

**WSL2 note:** WSL2 on Windows 11 has audio support built in (WSLg). On Windows 10, audio from WSL2 requires manual PulseAudio setup, which is non-trivial.

**Complexity rating:** Hard - not a clean equivalent; audio from WSL2 is unreliable across Windows versions.

**Recommended workshop approach:** Skip the `afplay`-based audio hooks for Windows students. The voice/soundboard feature is a bonus, not core to the curriculum. Document it as "Mac-only for now" and provide a no-op stub (a script that does nothing) so Windows students don't get errors.

---

### say (macOS TTS CLI Command)

**Mac approach:** `say "Hello world"` in the terminal speaks text aloud using macOS's built-in TTS engine. Used in voice feedback hooks.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Use a Git Bash shell function that calls PowerShell's `System.Speech` synthesizer. | Use the same PowerShell bridge, install `espeak`, or add a wrapper script that mimics the `say` interface. |

**WSL2 note:** WSL2 on Windows 11 can play audio, so eSpeak or the PowerShell bridge will produce audible output. Windows 10 WSL2 audio support is inconsistent.

**Complexity rating:** Medium - a PowerShell wrapper can closely replicate `say` on Windows 11.

**Recommended workshop approach:** Provide a drop-in `say` wrapper script for Windows students that calls the PowerShell TTS engine. Students don't need to know the internals - they just add the script to their PATH. Include this in the workshop repo as `say-windows.sh`. For Windows 10 students, flag that audio may not work and offer ElevenLabs API as the cloud fallback (which is platform-agnostic).

---

### zsh / ~/.zshrc (Default Shell Configuration)

**Mac approach:** zsh is the default shell since macOS Catalina (2019). Shell config lives in `~/.zshrc`. Students add environment variables, PATH customizations, and aliases here.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Git Bash uses bash by default, so `~/.bashrc` is the startup file for aliases and PATH changes. The `~/.zshrc` path itself still works as a normal file under the Windows home directory, and simple curriculum checks that read/write it are not blocked. For commands meant to load automatically in Git Bash, mirror simple exports and aliases into `~/.bashrc`. | Ubuntu in WSL2 uses bash by default. Students can switch to zsh: `sudo apt install zsh -y`, then `chsh -s $(which zsh)`. After reopening the terminal, zsh is active and `~/.zshrc` works identically to Mac. |

**Mode note:** Do not say `~/.zshrc` is impossible without WSL2. The file path works in Git Bash. The only difference is whether the current shell automatically sources it.

**Complexity rating:** Easy for simple dotfile edits in Git Bash. Easy in WSL2 after switching to zsh.

**Recommended workshop approach:** For Git Bash students, use `~/.bashrc` for live shell behavior and mention `~/.zshrc` only when the curriculum is teaching the Mac file. For WSL2 students who want exact Mac parity, install zsh and use `~/.zshrc`.

---

### FileVault (Mac Disk Encryption)

**Mac approach:** Enable FileVault in System Settings -> Privacy & Security -> FileVault. Required as a security baseline before storing API keys and enabling YOLO mode.

**Windows equivalent:** BitLocker - built into Windows 10/11 Pro and Enterprise. Enable via Control Panel -> BitLocker Drive Encryption. On Windows 11 Home, Device Encryption is available as a simplified version (Settings -> Privacy & Security -> Device Encryption).

**WSL2 note:** If BitLocker is enabled on the Windows drive, the WSL2 filesystem (stored inside Windows) is also encrypted. No separate encryption step needed for WSL2.

**Complexity rating:** Easy - BitLocker is built-in and follows a similar enable-and-forget pattern as FileVault.

**Recommended workshop approach:** Teach both. Slide note: "Mac -> FileVault, Windows -> BitLocker or Device Encryption. Both accomplish the same goal: encrypting your drive so your API keys can't be read if your laptop is lost or stolen."

---

### iMessage Integration

**Mac approach:** Claude Code reads/sends iMessages via AppleScript or the `imessage` plugin. Requires a Mac with iMessage signed in. Used for notifications and interactive responses.

**Windows equivalent:** None. iMessage is Apple-only. There is no official or supported way to access iMessage from Windows.

**WSL2 note:** Not applicable. iMessage cannot be accessed from WSL2 or any non-Apple environment.

**Complexity rating:** Hard (impossible) - no Windows equivalent exists.

**Recommended workshop approach:** Skip for Windows students entirely. Replace any curriculum demonstrations of iMessage integration with Slack notifications or email - both are platform-agnostic. Flag this clearly: "iMessage integration is Mac-only. Windows students: use Slack for agent notifications instead."

---

### Screens 5 (Remote Desktop)

**Mac approach:** Screens 5 (Edovia) - Mac app for VNC/RDP remote desktop connections to other machines. Used to connect to remote servers or other machines in the fleet.

**Windows equivalent:**
- **Remote Desktop Connection (RDP)** - built into Windows, excellent for connecting to Windows servers. Start -> "Remote Desktop Connection" or `mstsc` command.
- **Microsoft Remote Desktop** (free, Microsoft Store) - modern version of the above.
- For connecting to Mac or Linux machines: **RealVNC Viewer** (free), **TigerVNC**, or **MobaXterm** (free, includes SSH + VNC in one app).

**WSL2 note:** Not applicable. Remote desktop clients run natively on Windows.

**Complexity rating:** Easy - Windows RDP is actually more capable than Screens 5 for Windows-to-Windows connections; comparable for cross-platform use.

**Recommended workshop approach:** Teach both. For the specific use case (connecting to a remote Linux server), SSH from Git Bash or WSL2 is usually better than a full remote desktop anyway. Flag: "Windows has built-in RDP which is excellent. For Linux server access, just use SSH from your chosen workshop terminal."

---

### chmod / File Permissions Model

**Mac approach:** `chmod 600 ~/.cache/secrets.env` restricts a file to owner-read-only. Standard Unix permissions. Used throughout the curriculum to secure API key files.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Git Bash includes `chmod`. `chmod 600 ~/.cache/secrets.env` runs without modification and is sufficient for the workshop's Git/SSH/script expectations. Windows ACLs remain the underlying enforcement layer, so use `icacls` for strict Windows-native hardening. | `chmod` works identically inside WSL2. The Linux permission model is fully supported. `chmod 600 ~/.cache/secrets.env` runs without modification. |

**Mode note:** Do not mark `chmod` as WSL2-only. It works in Git Bash for the curriculum. WSL2 is still the stronger Linux-permission match.

**Complexity rating:** Easy in Git Bash for workshop use. Easy inside WSL2. Hard in PowerShell if you require exact ACL control with `icacls`.

**Recommended workshop approach:** Teach the Mac command, then name the terminal: Git Bash or Ubuntu. Add a footnote: "Do not run this in PowerShell or Command Prompt unless you are intentionally using Windows ACL tools."

---

### ~/.config/ Path Conventions

**Mac approach:** Config files for CLI tools live in `~/.config/` (e.g., `~/.config/claude/`, `~/.config/op/`). This is the XDG Base Directory Specification standard, followed by most modern CLI tools.

**Windows equivalent (native Git Bash + winget):** Git Bash uses the Windows user profile as `HOME`, so `~/.config/` resolves to `C:\Users\YourName\.config\`. Many CLI tools also use `%APPDATA%\`, so check the specific tool, but the Unix-style `~/.config/` path works in Git Bash.

**Windows equivalent (inside WSL2):** `~/.config/` inside WSL2 works identically to Mac. All CLI tools that follow XDG conventions store their config in the same relative paths. The absolute path is something like `/home/yourusername/.config/` inside the WSL2 environment.

**Mode note:** Git Bash and WSL2 both support `~/.config/`, but they are different physical folders. Keep the student's project and tool config in the same mode they are using.

**Complexity rating:** Easy in Git Bash. Easy inside WSL2.

**Recommended workshop approach:** Teach Mac way and add one note: "On Windows, `~/.config/` works in Git Bash and in Ubuntu, but those are separate homes."

---

### /opt/homebrew/bin vs Standard PATH

**Mac approach:** Apple Silicon Macs install Homebrew to `/opt/homebrew/bin/`, which may not be in PATH by default. The curriculum teaches students to add it explicitly in `~/.zshrc`: `export PATH="/opt/homebrew/bin:$PATH"`.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| There is no `/opt/homebrew/`. Windows tools installed by winget live in Windows paths and are usually added to the User or System PATH. Claude Code may require adding `%USERPROFILE%\.local\bin`. Git Bash reads the Windows PATH and presents it in Unix-style form. | Packages installed via `apt` go to standard Linux paths (`/usr/bin/`, `/usr/local/bin/`) that are already in PATH. Tools installed via `npm -g` under `nvm` are added by nvm. |

**Complexity rating:** Easy in both modes once the student knows which PATH is being edited.

**Recommended workshop approach:** Explain the Mac PATH fix as a Mac-specific quirk. For Git Bash students, focus on `%USERPROFILE%\.local\bin` for Claude Code. For WSL2 students, this step usually is not needed after `apt` or `nvm`.

---

### SSH Key Generation and Storage (~/.ssh/)

**Mac approach:** `ssh-keygen -t ed25519 -C "email"` in the terminal. Keys stored in `~/.ssh/`. SSH config in `~/.ssh/config`. macOS Keychain can store passphrases so they're entered once.

**Windows equivalents:**

| Native Git Bash + winget | WSL2 + Ubuntu |
|--------------------------|---------------|
| Git for Windows includes OpenSSH. Run `ssh-keygen`, `ssh-agent`, `ssh-add`, `ssh`, and `chmod` in Git Bash. Keys live in `~/.ssh/`, which maps to `C:\Users\YourName\.ssh\`. | Identical commands. `~/.ssh/` inside WSL2 is the correct location for keys used by tools running in WSL2. Use `chmod 600 ~/.ssh/id_ed25519` and `chmod 700 ~/.ssh/` exactly as on Mac. |

**Mode note:** WSL2 and Windows/Git Bash each have separate `~/.ssh/` directories. For tools running in Git Bash, use the Git Bash keys. For tools running inside WSL2, use the WSL2 keys. Students can copy public keys between environments if needed, but they do not need WSL2 for SSH.

**Complexity rating:** Easy in Git Bash. Easy inside WSL2.

**Recommended workshop approach:** Teach Mac way, then name the terminal: Git Bash for installer students, Ubuntu for WSL2 students.

---

## Windows Mode Decision Guide: Git Bash and WSL2

The old framing was too strict. These are the 11 instructor claims that were previously treated as WSL2-only, with the corrected Git Bash reality beside the WSL2 path.

| Curriculum item | Native Git Bash + winget reality | WSL2 + Ubuntu reality | Instructor call |
|-----------------|----------------------------------|-----------------------|-----------------|
| `chmod` / Unix file permissions | Works in Git Bash for workshop commands, Git, and SSH expectations. Windows ACLs still exist underneath. | Works with real Linux permission enforcement. | Do not require WSL2 just for `chmod`. Use WSL2 for Linux-permission purists or advanced hardening. |
| `~/.zshrc` / shell config | `~` and dotfiles work. Git Bash auto-loads `~/.bashrc`, not `~/.zshrc`; simple exports can be mirrored. | Install zsh and `~/.zshrc` behaves like Mac. | Teach Git Bash students `~/.bashrc` for live behavior; keep WSL2 as exact zsh parity. |
| `launchd` / persistent background daemons | Use Windows Task Scheduler for native scheduled work. | Use cron inside WSL2, usually launched or kept alive by Task Scheduler. | WSL2 is not required for scheduling, but neither mode is identical to launchd. |
| `afplay` audio playback | No direct `afplay`; call Windows media tools or skip the audio hook. | Possible via WSLg/audio bridge or calling PowerShell, but inconsistent. | Treat as optional or Mac-only unless you provide a wrapper. |
| `say` TTS command | Works through a PowerShell TTS wrapper called from Git Bash. | Works through PowerShell wrapper or eSpeak. | Provide a wrapper if TTS matters; otherwise skip. |
| iMessage integration | Impossible on Windows. | Impossible on Windows. | Mac-only. Use Slack or email for Windows. |
| Transloader | Impossible on Windows. | Impossible on Windows. | Apple-only. Use cloud folder, direct URL, `curl`, or `wget`. |
| MacWhisper | No identical native app. Use Windows GUI alternatives or cloud/API transcription. | CLI Whisper options exist inside WSL2. | Do not block workshop. Offer cloud/API or a Windows GUI alternative. |
| `/opt/homebrew/bin` PATH pattern | Mac-specific. Git Bash uses Windows PATH plus Unix-style path presentation. Claude may need `%USERPROFILE%\.local\bin`. | Mac-specific. `apt` and `nvm` handle most PATH needs. | Explain this as a Mac quirk, not a Windows blocker. |
| macOS Keychain (`security` CLI) | Not available. Use `.env` + `.gitignore`, Windows Credential Manager, 1Password CLI, or `icacls` for stricter Windows ACLs. | Not available. Use `.env` + `.gitignore`, 1Password bridge, or Linux secret tooling. | Teach `.env` for workshop speed; harden later. |
| `ssh-add` with macOS Keychain integration | `ssh-agent` and `ssh-add` work in Git Bash. The macOS Keychain flags do not. | `ssh-agent` and `ssh-add` work in Ubuntu. macOS Keychain flags do not. | Do not require WSL2 for SSH or `ssh-agent`; only change the keychain-specific part. |

**Bottom line:** Native Git Bash + winget is a valid workshop path and covers roughly 80% of the curriculum, including `chmod`, `~`, dotfiles, SSH, `ssh-agent`, Git, GitHub CLI, Node, npm, and Claude Code. WSL2 remains the alternative path when instructors want exact Linux behavior or a tool specifically needs Ubuntu.

---

## Windows-First Recommendations

These tools are either better on Windows than Mac, or are equal and have no friction difference:

| Tool | Windows Advantage |
|------|-------------------|
| **Remote Desktop (RDP)** | Built-in, more capable than Screens 5 for Windows-to-Windows connections. No extra app needed. |
| **VS Code** | Excellent WSL2 integration. The "WSL" extension is a first-party Microsoft product, deeply integrated. |
| **Tailscale** | Full feature parity. Windows client is mature and stable. |
| **n8n Cloud** | Browser-based, identical on all platforms. No advantage to either. |
| **Obsidian** | Full feature parity. Windows version is equally polished. |
| **Claude Desktop App** | Full feature parity. Windows `.exe` installer is straightforward. |
| **Git Bash + Git for Windows** | Installer-default path. Git, SSH, `ssh-agent`, `chmod`, and common shell commands work in the native Windows home folder. |
| **Git inside WSL2** | Identical to Linux and close to Mac. Useful for Linux-heavy demos. |
| **BitLocker (disk encryption)** | Pre-installed on Pro/Enterprise. No extra cost. FileVault is also free, so this is a tie. |
| **Windows Terminal** | Tab management and profile system are arguably more configurable than macOS Terminal.app (though Ghostty is competitive). |
| **Task Scheduler (for automation)** | GUI-based scheduler is more approachable than launchd plists for non-technical users - though less powerful for complex schedules. |

---

## Quick Reference: Key Path Translations

| Mac Path | Native Git Bash + winget | WSL2 + Ubuntu | Notes |
|----------|--------------------------|---------------|-------|
| `~/.zshrc` | File path works under `C:\Users\YourName`; Git Bash auto-loads `~/.bashrc` for shell startup | `~/.zshrc` inside Ubuntu after installing zsh | For Git Bash, mirror simple exports into `~/.bashrc` when they need to load automatically. |
| `~/.bashrc` | `C:\Users\YourName\.bashrc` | `/home/yourusername/.bashrc` | Best live shell config target for Git Bash students. |
| `~/.config/` | `C:\Users\YourName\.config\` | `/home/yourusername/.config/` | Works in both modes, but these are separate homes. |
| `~/.ssh/` | `C:\Users\YourName\.ssh\` | `/home/yourusername/.ssh/` | Keep keys in the mode where Git/Claude runs. |
| `~/.claude/` | Usually under `C:\Users\YourName\.claude\` for Windows Claude | `/home/yourusername/.claude/` | Do not assume config syncs between modes. |
| `/opt/homebrew/bin/` | No equivalent; use Windows PATH and `%USERPROFILE%\.local\bin` for Claude | `/usr/bin/` or `/usr/local/bin/` | Mac-specific Homebrew path. |
| `~/Library/LaunchAgents/` | Task Scheduler | cron plus Task Scheduler to keep WSL2 alive | Neither mode is identical to launchd. |
| `/Applications/` | `C:\Program Files\` or `%LOCALAPPDATA%` | Not applicable for Linux packages | Desktop apps live on the Windows side. |
| Windows `C:\Users\YourName\` | `/c/Users/YourName/` | `/mnt/c/Users/YourName/` | Git Bash and WSL2 use different mount syntax. |

---

## Instructor Notes

### Framing for Non-Technical Windows Students

Start by identifying their path:

> "If you used the AI Build Lab installer, open Git Bash. That is the normal Windows path for today. WSL2 is another option for people who want a fuller Linux setup, but you do not need it for the core workshop."

If a student is using WSL2, avoid explaining it as "a virtual machine" in technical terms. Instead:

> "Windows has a feature called WSL2 that lets us run a Linux-style terminal. Once it's set up, many commands work the same way they do on a Mac."

### Classroom Setup Strategy

- **Before workshop day:** Email Windows students the Prerequisites checklist from this document. Ask installer students to confirm Git Bash opens and `git`, `node`, `gh`, `ssh`, `ssh-agent`, `chmod`, and `winpty claude` work. Ask WSL2 students to confirm `claude --version` works inside Ubuntu.
- **Workshop day buffer:** Build 15-20 extra minutes into the morning for Windows students who hit setup issues. The most common failure is mode mismatch: installing a tool in one Windows mode, then running commands in the other.
- **Pairing:** If possible, seat Windows students next to Mac students for the first session. Most issues can be resolved with "run that command inside Git Bash" for installer students or "run that command inside Ubuntu" for WSL2 students.

### The One Sentence to Memorize

Tell installer-path Windows students: **"Everything we do happens inside Git Bash, not PowerShell, not Command Prompt."**

Tell WSL2-path Windows students: **"Everything we do happens inside Ubuntu, not PowerShell, not Command Prompt."**

This resolves 90% of Windows confusion in this workshop.

### Mac-Only Features to Flag Explicitly in Materials

Put a Mac icon or a note in the curriculum materials next to:
- Any use of `afplay`
- Any use of `say`
- Any use of iMessage/Transloader
- Any use of launchd plists
- MacWhisper demonstrations
- macOS Keychain (`security` CLI)

These should either be replaced with cross-platform alternatives or clearly labeled "Mac only - Windows students, skip this step."

### Testing Your Windows Setup

Have native Git Bash students run this quick validation sequence inside Git Bash before the first session:

```bash
git --version
node --version
npm --version
gh --version
ssh -V
ssh-agent -s
chmod --version
winpty claude --version
```

If all pass, the student is ready for the installer-default Windows path.

Have WSL2 students run this quick validation sequence inside Ubuntu before the first session:

```bash
node --version       # should show v20.x or higher
npm --version        # should show v10.x or higher
claude --version     # should show Claude Code version
git --version        # should show git 2.x
gh --version         # should show gh 2.x
ssh -V               # should show OpenSSH version
echo $SHELL          # should show /bin/zsh (after switching to zsh)
```

If all seven pass, the student is ready for the WSL2 path.

---

*This document covers the curriculum as of April 2026. Tool versions and Windows/WSL2 capabilities change frequently - verify against current documentation before each cohort.*
