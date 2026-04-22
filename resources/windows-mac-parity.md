# Windows Platform Parity Reference
**AI Build Lab — Claude Code Workshop**
**Audience:** Non-technical operators | **Last updated:** 2026-04-22

This document maps every Mac-specific tool and concept in the curriculum to its Windows equivalent, flags gaps, and gives instructors a clear recommended action for each item. Use it as the authoritative reference when prepping Windows students before or during Day 1.

---

## Table of Contents

1. [Windows Prerequisites (Do Before Day 1)](#windows-prerequisites)
2. [Tool-by-Tool Parity Matrix](#tool-by-tool-parity-matrix)
3. [Things That Simply Don't Work on Windows Without WSL2](#things-that-dont-work-without-wsl2)
4. [Windows-First Recommendations](#windows-first-recommendations)
5. [Quick Reference: Key Path Translations](#quick-reference-key-path-translations)
6. [Instructor Notes](#instructor-notes)

---

## Windows Prerequisites

These are the steps a Windows student must complete **before Day 1** that a Mac student does not need to worry about. Budget 30–60 minutes. The curriculum assumes these are done.

### 1. Enable WSL2 (Windows Subsystem for Linux)

WSL2 gives Windows a real Linux kernel underneath. Without it, roughly half the CLI tools in this curriculum won't work at all. This is non-negotiable.

**Steps:**
1. Open PowerShell as Administrator (right-click Start → "Windows PowerShell (Admin)")
2. Run: `wsl --install`
3. Restart the computer when prompted
4. On reboot, a terminal window opens automatically to finish Ubuntu setup — create a username and password when asked (this is your Linux username, not your Windows login)
5. Confirm it worked: open PowerShell and run `wsl --status` — you should see "Default Version: 2"

**Minimum Windows version required:** Windows 10 version 2004 (Build 19041) or Windows 11. Run `winver` in the Start menu to check.

**Why this matters:** WSL2 is not just a compatibility layer — it's a full Linux environment. Everything in this curriculum that involves a terminal, `~/.config/`, `chmod`, `zsh`, or shell scripts runs inside WSL2, not in Windows itself.

### 2. Install Windows Terminal

The default Command Prompt and PowerShell windows are not suitable for this workshop. Windows Terminal is the modern replacement and supports WSL2 natively.

- Download from the Microsoft Store (search "Windows Terminal") or run: `winget install Microsoft.WindowsTerminal`
- After install, open Windows Terminal and set the default profile to "Ubuntu" (the WSL2 instance): Settings → Startup → Default profile → Ubuntu

### 3. Update Ubuntu inside WSL2

After WSL2 is set up, open Ubuntu in Windows Terminal and run:
```bash
sudo apt update && sudo apt upgrade -y
```

### 4. Install Node.js inside WSL2 (via nvm)

Do NOT install Node.js with the Windows installer — that installs it on the Windows side, not inside WSL2 where Claude Code lives.

Inside Ubuntu (WSL2):
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
# Close and reopen the terminal, then:
nvm install --lts
node --version   # should show v20.x or higher
```

### 5. Install Claude Code CLI inside WSL2

Once Node.js is installed inside WSL2:
```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

### 6. Install Git inside WSL2

```bash
sudo apt install git -y
git --version
```

Then configure identity:
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 7. Generate an SSH key inside WSL2

```bash
ssh-keygen -t ed25519 -C "you@example.com"
# Accept all defaults (press Enter three times)
cat ~/.ssh/id_ed25519.pub
# Copy the output and add it to GitHub → Settings → SSH Keys
```

### 8. Install GitHub CLI (gh) inside WSL2

```bash
sudo apt install gh -y
gh auth login
# Choose GitHub.com → HTTPS → paste a personal access token, or follow browser flow
```

### Summary Checklist for Windows Students

| Step | Done? |
|------|-------|
| Windows 10 v2004+ or Windows 11 confirmed | |
| WSL2 installed (`wsl --install`) | |
| Ubuntu set up (username + password created) | |
| Windows Terminal installed + default set to Ubuntu | |
| Ubuntu updated (`sudo apt update && upgrade`) | |
| Node.js installed via nvm inside WSL2 | |
| Claude Code CLI installed inside WSL2 | |
| Git installed and configured inside WSL2 | |
| SSH key generated inside WSL2 + added to GitHub | |
| GitHub CLI installed and authenticated | |

---

## Tool-by-Tool Parity Matrix

---

### Terminal (Ghostty / iTerm2 / Terminal.app)

**Mac approach:** Students use Ghostty (the workshop's recommended terminal), or fall back to iTerm2 or the built-in Terminal.app. All are native macOS applications.

**Windows equivalent:** Windows Terminal (free, from Microsoft Store). It supports multiple tabs, profiles, and custom fonts. Once WSL2 is configured, the Ubuntu profile inside Windows Terminal is functionally identical to Mac Terminal for everything this curriculum does.

**WSL2 note:** The terminal app itself runs on Windows. The shell sessions inside it run in Linux. This distinction only matters if a student tries to navigate to Windows files from the Linux shell — use `/mnt/c/Users/YourName/` to access Windows files from WSL2.

**Complexity rating:** Easy — Windows Terminal is polished and non-technical users adapt quickly.

**Recommended workshop approach:** Teach Mac first, note the Windows Terminal equivalent. Ghostty-specific features (appearance settings, split panes) have direct Windows Terminal equivalents in the Settings UI. No curriculum changes needed — just swap the name.

---

### Claude Code CLI (npm install -g @anthropic-ai/claude-code)

**Mac approach:** Install globally via npm in the native macOS terminal. Runs in zsh or bash. Config lives at `~/.claude/`.

**Windows equivalent:** Install inside WSL2 using npm (see Prerequisites). Claude Code is fully supported on Linux/WSL2. The config directory `~/.claude/` exists inside the WSL2 Ubuntu environment, not in the Windows file system.

**WSL2 note:** Claude Code must be installed inside WSL2, not on the Windows side. If a student installs Node.js via the Windows installer and then runs `npm install -g @anthropic-ai/claude-code` in PowerShell, it "works" but the resulting `claude` command won't have access to Linux tools (zsh, chmod, file permissions, etc.) that Claude Code relies on. Always install inside WSL2.

**Complexity rating:** Medium — the installation itself is easy; the "install it in the right place" instruction requires one extra clarification for Windows students.

**Recommended workshop approach:** Teach both. The command is identical once inside WSL2. Flag the "install inside WSL2" requirement prominently on a slide.

---

### Claude Desktop App

**Mac approach:** Download from claude.ai, install, launch. The new version includes local Claude Code integration built in. Config syncs with claude.ai account.

**Windows equivalent:** Claude Desktop is available for Windows — download the `.exe` installer from claude.ai. Full feature parity with Mac version as of 2025. The local Claude Code integration works on Windows as of the Claude Desktop 2025 release.

**WSL2 note:** Not applicable. Claude Desktop is a native Windows application and does not need WSL2.

**Complexity rating:** Easy — the Windows installer is a standard .exe, no CLI required.

**Recommended workshop approach:** Teach Mac way. The Windows experience is identical — just a different installer file. No curriculum changes needed.

---

### VS Code + Claude Code Extension

**Mac approach:** Install VS Code from code.visualstudio.com, install the Claude Code extension from the Extensions marketplace, authenticate.

**Windows equivalent:** VS Code for Windows is identical. Install the Claude Code extension the same way. The key difference: if students are working inside WSL2, they should also install the "WSL" extension (by Microsoft) in VS Code so the editor connects to the WSL2 filesystem instead of Windows. When VS Code opens a WSL2 folder, a green "WSL: Ubuntu" badge appears in the bottom-left corner confirming the connection.

**WSL2 note:** Install VS Code on Windows (not inside WSL2). Then inside a WSL2 terminal, navigate to your project folder and type `code .` — this opens VS Code on Windows but connected to the WSL2 filesystem. This is the correct workflow.

**Complexity rating:** Easy — the extension marketplace and UI are identical on both platforms.

**Recommended workshop approach:** Teach Mac way. Add one slide or callout box: "Windows students: also install the WSL extension and open projects with `code .` from the WSL2 terminal."

---

### Homebrew (Package Manager)

**Mac approach:** Install via the one-liner at brew.sh. Use `brew install <tool>` to add CLI tools. Homebrew installs to `/opt/homebrew/bin/` on Apple Silicon Macs.

**Windows equivalent (native Windows):** `winget` (Windows Package Manager) is the closest native equivalent. Pre-installed on Windows 11; available for Windows 10 via the App Installer. Syntax: `winget install <package-name>`. Does not install the same packages as Homebrew — it installs Windows applications and some CLI tools.

**Windows equivalent (inside WSL2):** `apt` (Advanced Package Tool) is the Ubuntu package manager inside WSL2. Use `sudo apt install <package>` for CLI tools that run in the Linux environment. For tools the curriculum installs via Homebrew (like `gh`, `jq`, `tree`), `apt` is the correct replacement inside WSL2.

**WSL2 note:** For the purposes of this curriculum, use `apt` inside WSL2 as the direct Homebrew replacement. The packages available differ slightly, but every tool taught in this workshop has an `apt` equivalent.

**Complexity rating:** Easy inside WSL2. Medium if students need to understand the Windows/WSL2 split.

**Recommended workshop approach:** Skip Homebrew for Windows students. Replace with `apt` inside WSL2 for CLI tools, and `winget` for Windows desktop apps. Provide a side-by-side cheat sheet: "Mac: `brew install X` → Windows/WSL2: `sudo apt install X`".

---

### 1Password CLI (op)

**Mac approach:** Install via Homebrew (`brew install 1password-cli`). Use `op` commands to retrieve secrets at runtime. Integrates with the 1Password desktop app for biometric unlock.

**Windows equivalent:** 1Password CLI is available for Windows. Download the `.zip` from 1password.com/downloads/command-line/, extract `op.exe`, and add it to PATH. Also available inside WSL2 via the Linux binary.

**WSL2 note:** For scripts that run inside WSL2, install the Linux version of `op` inside WSL2 (download the Linux binary from 1password.com). The Windows `op.exe` is not accessible from inside WSL2 by default. The 1Password desktop app on Windows handles biometric unlock, and the `op` CLI inside WSL2 can connect to it via a socket — but this requires configuring the 1Password app to allow connections from WSL2 (Settings → Developer → "Use the SSH agent" and "Integrate with 1Password CLI").

**Complexity rating:** Medium — the CLI itself is the same; the WSL2 bridge setup requires a few extra steps.

**Recommended workshop approach:** Teach both. Share a setup guide for the WSL2 ↔ 1Password bridge. If the workshop doesn't heavily rely on automated secret retrieval (i.e., students just paste API keys manually), this can be deferred to post-workshop setup.

---

### macOS Keychain (Security Store for API Keys/Tokens)

**Mac approach:** Use the `security` CLI command or Keychain Access app to store and retrieve secrets. API keys live in the keychain and are retrieved at runtime without appearing in shell config files.

**Windows equivalent:** Windows Credential Manager (built into Windows). Accessible via Control Panel → Credential Manager, or programmatically via the `cmdkey` CLI. For scripts inside WSL2, there is no built-in equivalent that works seamlessly — the most common approach is to store secrets in a `.env` file inside WSL2 with restricted permissions (`chmod 600`), or use the `pass` utility (a GPG-encrypted password store for Linux).

**WSL2 note:** The Windows Credential Manager is not accessible from inside WSL2 without a third-party bridge. For non-technical workshop students, the practical recommendation is: store API keys in a `.env` file inside WSL2 with `chmod 600`, and add that file to `.gitignore`. This is less secure than a proper keychain but far simpler for a workshop setting.

**Complexity rating:** Hard — there is no simple, cross-platform equivalent that works identically.

**Recommended workshop approach:** For Windows students in a workshop context, skip the keychain integration and teach the `.env` file approach with `chmod 600` as a reasonable stand-in. Flag this explicitly: "Mac students use Keychain for extra security; Windows students will use a protected .env file — both approaches keep your key out of git." Revisit proper Credential Manager integration as a post-workshop exercise for students who want to harden their setup.

---

### Tailscale (Mesh VPN)

**Mac approach:** Install Tailscale from the Mac App Store or tailscale.com. Native macOS app with menu bar icon.

**Windows equivalent:** Tailscale for Windows is fully supported. Download the installer from tailscale.com/download/windows. Native Windows app with system tray icon. Feature-complete parity with Mac.

**WSL2 note:** Tailscale on Windows automatically routes traffic for WSL2 connections — no separate installation needed inside WSL2. WSL2 instances can reach Tailscale IPs as long as the Windows Tailscale client is running.

**Complexity rating:** Easy — the Windows client is essentially identical to Mac.

**Recommended workshop approach:** Teach Mac way. The Windows experience is the same. No curriculum changes needed.

---

### Obsidian (Note-Taking)

**Mac approach:** Download from obsidian.md, install, open a vault.

**Windows equivalent:** Obsidian for Windows is fully supported. Download the `.exe` installer from obsidian.md. Feature-complete parity.

**WSL2 note:** Not applicable. Obsidian is a desktop app and runs natively on Windows.

**Complexity rating:** Easy — identical experience on both platforms.

**Recommended workshop approach:** Teach Mac way. No changes needed.

---

### n8n (Workflow Automation)

**Mac approach:** Run locally via `npm install -g n8n` and `n8n start`, or use n8n Cloud. Local installs use the macOS filesystem paths.

**Windows equivalent:** n8n Cloud is identical on any platform (browser-based). For local n8n, install inside WSL2 via npm — the experience is the same as Mac. Do not install n8n via the Windows npm (PowerShell) — the file path conventions break.

**WSL2 note:** Running n8n locally inside WSL2 works well. Access the n8n UI in a Windows browser at `http://localhost:5678` — WSL2 automatically forwards ports to Windows localhost.

**Complexity rating:** Easy for Cloud; Medium for local (WSL2 setup required first).

**Recommended workshop approach:** Use n8n Cloud for the workshop to eliminate the local install complexity. This is platform-agnostic and removes WSL2 from the equation entirely for n8n.

---

### Node.js / npm

**Mac approach:** Install via nvm (`curl -o- .../install.sh | bash`) or Homebrew. Lives at `/opt/homebrew/bin/node` or `~/.nvm/versions/node/...`.

**Windows equivalent:** Install via nvm inside WSL2 (see Prerequisites). Do not use the Windows Node.js installer from nodejs.org for anything that runs in WSL2 — the Windows and Linux versions don't share binaries.

**WSL2 note:** Node.js installed inside WSL2 is completely isolated from Node.js installed on Windows. This is almost always the right setup for this curriculum. The commands (`node`, `npm`, `npx`) are identical once inside WSL2.

**Complexity rating:** Easy inside WSL2. Medium if students install it in the wrong place.

**Recommended workshop approach:** Teach Mac way. The commands are identical inside WSL2. Provide one clear instruction: "Install Node via nvm inside the Ubuntu terminal, not via the Windows installer."

---

### Git + GitHub CLI (gh)

**Mac approach:** Git is pre-installed on Mac (via Xcode Command Line Tools). `gh` installed via Homebrew. Both run in the native terminal.

**Windows equivalent:** Install both inside WSL2: `sudo apt install git gh`. Authentication with `gh auth login` works identically. Alternatively, Git for Windows (gitforwindows.org) provides Git on the Windows side, but for this curriculum, the WSL2 versions are preferred.

**WSL2 note:** Git and `gh` inside WSL2 are the direct equivalents. If students use VS Code with the WSL extension, Git operations via the VS Code UI (Source Control panel) work correctly against the WSL2 filesystem.

**Complexity rating:** Easy inside WSL2.

**Recommended workshop approach:** Teach Mac way. Commands are identical inside WSL2. No curriculum changes needed beyond the initial install instruction.

---

### MacWhisper (Local Speech-to-Text)

**Mac approach:** Download MacWhisper from goodsnooze.gumroad.com. Native macOS app. Uses OpenAI's Whisper model locally. Produces transcripts from audio/video files or live microphone.

**Windows equivalent:** No direct Windows equivalent with the same polished UI. Options:
- **Whisper.cpp for Windows** — command-line only, requires compilation or pre-built binaries. Suitable for technical users, not non-technical operators.
- **OpenAI Whisper via Python inside WSL2** — install with `pip install openai-whisper` inside WSL2, run `whisper audiofile.mp3`. Functional but command-line only.
- **Faster-Whisper Desktop** (free, Windows GUI) — open-source, available at github.com/Const-me/Whisper. Closest UI equivalent to MacWhisper on Windows.
- **Whisper Transcription (Microsoft Store)** — unofficial Windows Whisper GUI app, paid, similar workflow to MacWhisper.

**WSL2 note:** Python Whisper can be run inside WSL2. For non-technical operators, the CLI experience is a meaningful friction increase compared to MacWhisper's drag-and-drop interface.

**Complexity rating:** Hard — no polished Windows equivalent with the same UX as MacWhisper.

**Recommended workshop approach:** Use the cloud alternative: the Whisper API via n8n or a simple Python script, which works identically on all platforms. For students who need local transcription, recommend Faster-Whisper Desktop as the closest Windows match. Flag this in workshop materials as "Mac students have an easier path here."

---

### Downie 4 (Video Downloader)

**Mac approach:** Downie 4 from software.charliemonroe.net — native macOS app, drag a URL in, get the video out. Simple GUI for non-technical users.

**Windows equivalent:**
- **yt-dlp** (open source CLI) — install inside WSL2: `sudo apt install yt-dlp`. Usage: `yt-dlp <URL>`. Feature-complete, cross-platform, but command-line only.
- **YT-DLP GUI** for Windows — several third-party frontends exist (e.g., "Videomass" or "yt-dlg"). Free but less polished than Downie.
- **4K Video Downloader** — paid Windows app (similar price to Downie), GUI-based, close UX match.

**WSL2 note:** `yt-dlp` inside WSL2 downloads files to the Linux filesystem. Students need to either work from there or move files to Windows with `cp /path/to/file /mnt/c/Users/YourName/Downloads/`.

**Complexity rating:** Medium — yt-dlp is easy to learn but the lack of a polished GUI is a step down for non-technical operators.

**Recommended workshop approach:** Teach `yt-dlp` inside WSL2 as the universal alternative (it also works on Mac). This is actually a curriculum improvement — teaching a cross-platform CLI tool instead of a Mac-only GUI. Alternatively, if the workshop just needs students to have video files, provide pre-downloaded files to eliminate platform dependency entirely.

---

### Transloader

**Mac approach:** Transloader (tailored.art/transloader) — Mac app for sending URLs or files to a remote Mac for download. Requires both sender and receiver to be on Apple platforms.

**Windows equivalent:** None. Transloader is Apple-ecosystem-only (uses iCloud for transport). The concept (remote download handoff) can be replicated with other tools, but there is no drop-in Windows equivalent.

**WSL2 note:** Not applicable.

**Complexity rating:** Hard — Apple-only by design.

**Recommended workshop approach:** Skip for Windows students. If the curriculum uses Transloader for a specific workflow, replace it with: (a) a shared cloud folder (Dropbox, Google Drive) where the instructor drops files, or (b) a direct download link the student fetches with `curl` or `wget` inside WSL2. Most Transloader use cases in a workshop context are about getting files to students, which has simpler cross-platform alternatives.

---

### Time Machine (Backup — Required Before YOLO Mode)

**Mac approach:** Enable Time Machine in System Settings, point it at an external drive or network share. Claude Code's YOLO/auto-approve mode requires a working backup as a safety prerequisite.

**Windows equivalent:**
- **File History** — built into Windows 10/11 (Settings → Update & Security → Backup → Add a drive). Continuously backs up files in your user folder. Closest equivalent to Time Machine.
- **Windows Backup** (Windows 11) — Settings → System → Storage → Backup. More comprehensive, can back up to OneDrive or external drive.
- **Macrium Reflect Free** — third-party, creates full system images. More robust than File History for full disaster recovery.

**WSL2 note:** File History and Windows Backup do NOT back up the WSL2 Linux filesystem by default. This is an important gap. To back up WSL2 data: manually export with `wsl --export Ubuntu backup.tar` from PowerShell, and back up the resulting .tar file. For workshop purposes, the YOLO prerequisite can be satisfied with File History on Windows + a periodic `wsl --export`.

**Complexity rating:** Medium — Windows has good backup tools, but the WSL2 gap requires an extra step that non-technical users may not know about.

**Recommended workshop approach:** Teach both. For Windows students: enable File History (easy) AND show the `wsl --export` command for WSL2 data. Explicitly note: "Your Claude Code config and projects live inside WSL2 — Windows Backup doesn't cover them unless you export."

---

### launchd (macOS Daemon System / Scheduled Tasks)

**Mac approach:** Use `launchd` with `.plist` files to schedule scripts. Plists live in `~/Library/LaunchAgents/`. Load with `launchctl load`. This is how the curriculum automates recurring Claude Code tasks.

**Windows equivalent (native Windows):** Task Scheduler — built into Windows, accessible via Start → "Task Scheduler". GUI-based, can run scripts on a schedule. PowerShell or batch scripts can also be scheduled here.

**Windows equivalent (inside WSL2):** `cron` — the standard Linux scheduler. Enable it in WSL2 with `sudo service cron start`. Add jobs with `crontab -e`. For persistent execution, WSL2 needs to be running (or auto-started via a Windows Task Scheduler task that launches WSL2 on login).

**WSL2 note:** WSL2 does not run in the background by default — it shuts down when no terminals are open. This means WSL2 cron jobs only run while WSL2 is active. Work around this by: (a) having Windows Task Scheduler trigger WSL2 commands (`wsl -e /path/to/script.sh`), or (b) keeping a WSL2 terminal open in the background.

**Complexity rating:** Hard — the Mac launchd system is persistent and automatic; replicating the same behavior on Windows requires combining Windows Task Scheduler and WSL2, which is non-obvious for non-technical users.

**Recommended workshop approach:** For Windows students, teach `cron` inside WSL2 for basic scheduling, and show how to trigger a WSL2 script from Windows Task Scheduler if persistence is needed. Alternatively, for workshop content that uses launchd for automation, migrate those automations to n8n (which is platform-agnostic) — this is a better long-term pattern anyway.

---

### afplay (macOS Audio Playback Command)

**Mac approach:** `afplay soundfile.mp3` in the terminal plays audio. Used in the curriculum for soundboard/voice feedback hooks.

**Windows equivalent (inside WSL2):** There is no direct equivalent that works inside WSL2 out of the box. Options:
- **PowerShell from WSL2:** `powershell.exe /c (New-Object Media.SoundPlayer 'C:\path\to\file.wav').PlaySync()` — works but clunky, only for .wav files, requires Windows path.
- **mpg123 inside WSL2:** `sudo apt install mpg123`, then `mpg123 file.mp3` — plays audio through the Windows audio system via WSL2 audio bridging (WSL2 supports PulseAudio/PipeWire on recent versions).
- **Windows `cmdmp3` or `vlc` called from WSL2** — possible but requires extra setup.

**WSL2 note:** WSL2 on Windows 11 has audio support built in (WSLg). On Windows 10, audio from WSL2 requires manual PulseAudio setup, which is non-trivial.

**Complexity rating:** Hard — not a clean equivalent; audio from WSL2 is unreliable across Windows versions.

**Recommended workshop approach:** Skip the `afplay`-based audio hooks for Windows students. The voice/soundboard feature is a bonus, not core to the curriculum. Document it as "Mac-only for now" and provide a no-op stub (a script that does nothing) so Windows students don't get errors.

---

### say (macOS TTS CLI Command)

**Mac approach:** `say "Hello world"` in the terminal speaks text aloud using macOS's built-in TTS engine. Used in voice feedback hooks.

**Windows equivalent (inside WSL2):**
- **PowerShell from WSL2:** `powershell.exe -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('Hello world')"` — works but verbose.
- **eSpeak inside WSL2:** `sudo apt install espeak`, then `espeak "Hello world"` — functional, robotic voice quality.
- **WSL2 → Windows TTS bridge script:** a short shell function can wrap the PowerShell call to mimic the `say` interface.

**WSL2 note:** WSL2 on Windows 11 can play audio, so eSpeak or the PowerShell bridge will produce audible output. Windows 10 WSL2 audio support is inconsistent.

**Complexity rating:** Medium — a PowerShell wrapper can closely replicate `say` on Windows 11.

**Recommended workshop approach:** Provide a drop-in `say` wrapper script for Windows students that calls the PowerShell TTS engine. Students don't need to know the internals — they just add the script to their PATH. Include this in the workshop repo as `say-windows.sh`. For Windows 10 students, flag that audio may not work and offer ElevenLabs API as the cloud fallback (which is platform-agnostic).

---

### zsh / ~/.zshrc (Default Shell Configuration)

**Mac approach:** zsh is the default shell since macOS Catalina (2019). Shell config lives in `~/.zshrc`. Students add environment variables, PATH customizations, and aliases here.

**Windows equivalent (inside WSL2):** Ubuntu in WSL2 uses bash by default. Students can switch to zsh: `sudo apt install zsh -y`, then `chsh -s $(which zsh)`. After reopening the terminal, zsh is active and `~/.zshrc` works identically to Mac.

**WSL2 note:** Inside WSL2 with zsh installed, the experience is essentially identical to Mac. All curriculum commands using `~/.zshrc` work without modification.

**Complexity rating:** Easy — switching to zsh is a one-time setup step.

**Recommended workshop approach:** In the Windows Prerequisites section, include the step to install zsh and set it as default. After that, the rest of the curriculum's zsh content is identical.

---

### FileVault (Mac Disk Encryption)

**Mac approach:** Enable FileVault in System Settings → Privacy & Security → FileVault. Required as a security baseline before storing API keys and enabling YOLO mode.

**Windows equivalent:** BitLocker — built into Windows 10/11 Pro and Enterprise. Enable via Control Panel → BitLocker Drive Encryption. On Windows 11 Home, Device Encryption is available as a simplified version (Settings → Privacy & Security → Device Encryption).

**WSL2 note:** If BitLocker is enabled on the Windows drive, the WSL2 filesystem (stored inside Windows) is also encrypted. No separate encryption step needed for WSL2.

**Complexity rating:** Easy — BitLocker is built-in and follows a similar enable-and-forget pattern as FileVault.

**Recommended workshop approach:** Teach both. Slide note: "Mac → FileVault, Windows → BitLocker or Device Encryption. Both accomplish the same goal: encrypting your drive so your API keys can't be read if your laptop is lost or stolen."

---

### iMessage Integration

**Mac approach:** Claude Code reads/sends iMessages via AppleScript or the `imessage` plugin. Requires a Mac with iMessage signed in. Used for notifications and interactive responses.

**Windows equivalent:** None. iMessage is Apple-only. There is no official or supported way to access iMessage from Windows.

**WSL2 note:** Not applicable. iMessage cannot be accessed from WSL2 or any non-Apple environment.

**Complexity rating:** Hard (impossible) — no Windows equivalent exists.

**Recommended workshop approach:** Skip for Windows students entirely. Replace any curriculum demonstrations of iMessage integration with Slack notifications or email — both are platform-agnostic. Flag this clearly: "iMessage integration is Mac-only. Windows students: use Slack for agent notifications instead."

---

### Screens 5 (Remote Desktop)

**Mac approach:** Screens 5 (Edovia) — Mac app for VNC/RDP remote desktop connections to other machines. Used to connect to remote servers or other machines in the fleet.

**Windows equivalent:**
- **Remote Desktop Connection (RDP)** — built into Windows, excellent for connecting to Windows servers. Start → "Remote Desktop Connection" or `mstsc` command.
- **Microsoft Remote Desktop** (free, Microsoft Store) — modern version of the above.
- For connecting to Mac or Linux machines: **RealVNC Viewer** (free), **TigerVNC**, or **MobaXterm** (free, includes SSH + VNC in one app).

**WSL2 note:** Not applicable. Remote desktop clients run natively on Windows.

**Complexity rating:** Easy — Windows RDP is actually more capable than Screens 5 for Windows-to-Windows connections; comparable for cross-platform use.

**Recommended workshop approach:** Teach both. For the specific use case (connecting to a remote Linux server), SSH inside WSL2 is usually better than a full remote desktop anyway. Flag: "Windows has built-in RDP which is excellent. For Linux server access, just use SSH."

---

### chmod / File Permissions Model

**Mac approach:** `chmod 600 ~/.cache/secrets.env` restricts a file to owner-read-only. Standard Unix permissions. Used throughout the curriculum to secure API key files.

**Windows equivalent (native Windows):** Windows uses Access Control Lists (ACLs) via `icacls` command. Conceptually similar but syntactically very different. Example equivalent: `icacls file.txt /inheritance:r /grant:r "username:R"`. Non-technical users find this confusing.

**Windows equivalent (inside WSL2):** `chmod` works identically inside WSL2. The Linux permission model is fully supported. `chmod 600 ~/.cache/secrets.env` runs without modification.

**WSL2 note:** Inside WSL2, use `chmod` exactly as taught on Mac. The permissions are enforced by the Linux kernel running in WSL2. This is one of the strongest arguments for WSL2 — Windows students can follow the same security practices without learning icacls.

**Complexity rating:** Easy inside WSL2. Hard on native Windows without WSL2.

**Recommended workshop approach:** Teach the Mac way. Inside WSL2, the commands are identical. No curriculum changes needed. Add a footnote: "These commands only work inside the WSL2/Ubuntu terminal, not in PowerShell or Command Prompt."

---

### ~/.config/ Path Conventions

**Mac approach:** Config files for CLI tools live in `~/.config/` (e.g., `~/.config/claude/`, `~/.config/op/`). This is the XDG Base Directory Specification standard, followed by most modern CLI tools.

**Windows equivalent (native Windows):** Windows uses `%APPDATA%\` (e.g., `C:\Users\YourName\AppData\Roaming\`) for app configs. CLI tools ported to Windows sometimes use this, sometimes use `%USERPROFILE%\.config\` to match Unix conventions.

**Windows equivalent (inside WSL2):** `~/.config/` inside WSL2 works identically to Mac. All CLI tools that follow XDG conventions store their config in the same relative paths. The absolute path is something like `/home/yourusername/.config/` inside the WSL2 environment.

**WSL2 note:** Inside WSL2, `~/.config/` is the correct path and works exactly like Mac. The Windows `%APPDATA%` path is irrelevant for tools running inside WSL2.

**Complexity rating:** Easy inside WSL2 — paths are identical.

**Recommended workshop approach:** Teach Mac way. Inside WSL2, paths are the same. Add one note: "These paths are for your Ubuntu terminal. They don't exist in Windows Explorer — they're inside your Linux environment."

---

### /opt/homebrew/bin vs Standard PATH

**Mac approach:** Apple Silicon Macs install Homebrew to `/opt/homebrew/bin/`, which may not be in PATH by default. The curriculum teaches students to add it explicitly in `~/.zshrc`: `export PATH="/opt/homebrew/bin:$PATH"`.

**Windows equivalent (inside WSL2):** Inside WSL2, packages installed via `apt` go to standard Linux paths (`/usr/bin/`, `/usr/local/bin/`) which are already in PATH. There is no `/opt/homebrew/` equivalent. The specific PATH manipulation taught for Mac is not needed inside WSL2.

**WSL2 note:** PATH management in WSL2 is simpler than on Mac — standard `apt`-installed tools are immediately available without PATH edits. Tools installed via `npm -g` go to `~/.nvm/versions/node/.../bin/` which nvm adds to PATH automatically.

**Complexity rating:** Easy — Windows students actually have a simpler PATH situation inside WSL2.

**Recommended workshop approach:** Explain the Mac PATH fix as a Mac-specific quirk. For Windows students: "Inside Ubuntu, this step isn't needed — installed tools are in PATH automatically."

---

### SSH Key Generation and Storage (~/.ssh/)

**Mac approach:** `ssh-keygen -t ed25519 -C "email"` in the terminal. Keys stored in `~/.ssh/`. SSH config in `~/.ssh/config`. macOS Keychain can store passphrases so they're entered once.

**Windows equivalent (inside WSL2):** Identical commands. `~/.ssh/` inside WSL2 is the correct location for keys used by tools running in WSL2. Use `chmod 600 ~/.ssh/id_ed25519` and `chmod 700 ~/.ssh/` exactly as on Mac.

**Windows equivalent (native Windows):** Windows 10/11 includes OpenSSH as an optional feature (Settings → Apps → Optional features → OpenSSH Client). Keys go in `C:\Users\YourName\.ssh\`. Works in PowerShell/Command Prompt. For VS Code SSH connections, the Windows SSH keys are used.

**WSL2 note:** WSL2 and Windows each have separate `~/.ssh/` directories. For tools running inside WSL2 (Claude Code, git, gh), use the WSL2 keys. For Windows-native tools (VS Code remote SSH), use the Windows keys. Students can copy the public key from WSL2 to Windows (`cp ~/.ssh/id_ed25519.pub /mnt/c/Users/YourName/.ssh/`) if they want to share keys between environments, but this is optional.

**Complexity rating:** Easy inside WSL2 — commands are identical.

**Recommended workshop approach:** Teach Mac way. Inside WSL2, commands are the same. Note: "Your SSH keys inside Ubuntu are separate from any Windows SSH keys. For everything we do in this workshop, use the Ubuntu terminal for key generation."

---

## Things That Don't Work on Windows Without WSL2

The following curriculum items **do not have a native Windows equivalent** and require WSL2 (or are simply impossible on Windows):

| Item | Situation |
|------|-----------|
| `chmod` / Unix file permissions | Requires WSL2; native Windows uses icacls (very different) |
| `~/.zshrc` / zsh shell | Requires WSL2; PowerShell uses different config files and syntax |
| `launchd` / persistent background daemons | No equivalent; WSL2 + Windows Task Scheduler is the workaround |
| `afplay` audio playback | No clean WSL2 equivalent; audio bridging unreliable on Windows 10 |
| `say` TTS command | Requires a PowerShell wrapper or eSpeak; not a one-liner |
| iMessage integration | Impossible on Windows; Apple-only |
| Transloader | Impossible on Windows; Apple-only |
| MacWhisper | No polished GUI equivalent; CLI alternatives exist via WSL2 |
| `/opt/homebrew/bin` PATH pattern | Mac-specific; not needed in WSL2 |
| macOS Keychain (`security` CLI) | Windows Credential Manager exists but is not accessible from WSL2 without a bridge |
| `ssh-add` with macOS Keychain integration | Works differently; WSL2 can use the Windows SSH agent with extra config |

**Bottom line:** Without WSL2, a Windows student cannot meaningfully participate in the CLI portions of this workshop. With WSL2 set up, approximately 80-85% of the curriculum is directly portable, and the remaining 15-20% has reasonable workarounds.

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
| **Git (inside WSL2)** | Identical to Mac. Git was originally built for Linux. |
| **BitLocker (disk encryption)** | Pre-installed on Pro/Enterprise. No extra cost. FileVault is also free, so this is a tie. |
| **Windows Terminal** | Tab management and profile system are arguably more configurable than macOS Terminal.app (though Ghostty is competitive). |
| **Task Scheduler (for automation)** | GUI-based scheduler is more approachable than launchd plists for non-technical users — though less powerful for complex schedules. |

---

## Quick Reference: Key Path Translations

| Mac Path | WSL2 Equivalent | Notes |
|----------|----------------|-------|
| `~/.zshrc` | `~/.zshrc` (inside Ubuntu) | Identical after installing zsh in WSL2 |
| `~/.config/` | `~/.config/` (inside Ubuntu) | Identical |
| `~/.ssh/` | `~/.ssh/` (inside Ubuntu) | Keep WSL2 keys here for CLI tools |
| `~/.claude/` | `~/.claude/` (inside Ubuntu) | Claude Code config; identical |
| `/opt/homebrew/bin/` | `/usr/bin/` or `/usr/local/bin/` | apt installs here; already in PATH |
| `~/Library/LaunchAgents/` | No equivalent | Use cron or Windows Task Scheduler |
| `/Applications/` | `C:\Program Files\` (Windows side) | Desktop apps only; not in WSL2 |
| Windows `C:\Users\YourName\` | `/mnt/c/Users/YourName/` | WSL2 mounts the Windows C: drive here |

---

## Instructor Notes

### Framing for Non-Technical Windows Students

Avoid explaining WSL2 as "a virtual machine" or "Linux inside Windows" in technical terms. Instead:

> "Windows has a feature called WSL2 that lets us run the same kind of terminal environment that Mac users have. Once it's set up (which takes about 20 minutes, and you only do it once), everything else in this workshop works the same way on your machine as it does on a Mac."

### Classroom Setup Strategy

- **Before Day 1:** Email Windows students the Prerequisites checklist from this document. Ask them to confirm WSL2 is installed and `claude --version` works inside Ubuntu.
- **Day 1 buffer:** Build 15-20 extra minutes into Day 1 for Windows students who hit setup issues. The most common: installed Node.js on Windows side instead of WSL2 side.
- **Pairing:** If possible, seat Windows students next to Mac students for the first session. Most issues can be resolved with "run that command inside the Ubuntu terminal, not PowerShell."

### The One Sentence to Memorize

Tell Windows students: **"Everything we do happens inside the Ubuntu terminal, not PowerShell, not Command Prompt."**

This resolves 90% of Windows confusion in this workshop.

### Mac-Only Features to Flag Explicitly in Materials

Put a Mac icon or a note in the curriculum materials next to:
- Any use of `afplay`
- Any use of `say`
- Any use of iMessage/Transloader
- Any use of launchd plists
- MacWhisper demonstrations
- macOS Keychain (`security` CLI)

These should either be replaced with cross-platform alternatives or clearly labeled "Mac only — Windows students, skip this step."

### Testing Your Windows Setup

Have Windows students run this quick validation sequence inside Ubuntu (WSL2) before the first session:

```bash
node --version       # should show v20.x or higher
npm --version        # should show v10.x or higher
claude --version     # should show Claude Code version
git --version        # should show git 2.x
gh --version         # should show gh 2.x
ssh-keygen -V        # should show OpenSSH version (if installed)
echo $SHELL          # should show /bin/zsh (after switching to zsh)
```

If all six pass, the student is ready for Day 1.

---

*This document covers the curriculum as of April 2026. Tool versions and Windows/WSL2 capabilities change frequently — verify against current documentation before each cohort.*
