# Recommended Windows Apps

> **Installer users:** If you already used the workshop installer, stay on the native Windows path: use **Git Bash** for terminal commands and **winget** for Windows app installs. Use **WSL2** only if you intentionally want the Linux-based setup or a facilitator tells you to switch.

These tools will make your agent OS experience better on Windows. All are either free or have generous free tiers.

---

## Terminals

### Windows Terminal (Required)
**Free | Microsoft Store**

You already installed this in the prerequisites. It's the best way to access WSL2 and PowerShell side by side (or, if on native Git Bash: Git Bash, PowerShell, and regular Windows tabs side by side). If you chose WSL2 and haven't set Ubuntu as your default profile yet, do that in Settings (Ctrl+,) > Startup > Default Profile.

### Warp
**Free tier | warp.dev**

An AI-native terminal with built-in AI suggestions. Warp now has a Windows version (still rolling out), so check warp.dev to see if it's available for your Windows version.

---

## Code & File Editors

### Visual Studio Code
**Free | code.visualstudio.com**

Essential for Windows. VS Code has excellent WSL2 integration, so you can open your Linux files in a graphical editor, run the terminal, and see everything side by side (or, if on native Git Bash: open your normal Windows project folder and use the built-in terminal profile for Git Bash).

Install from the website, then inside WSL2 you can open any folder with: `code .` (or, if on native Git Bash: run `code .` from the repo folder in Git Bash).

Install the **WSL extension** in VS Code for the best WSL2 experience (or, if on native Git Bash: skip the WSL extension unless you later add WSL2).

### Cursor
**Free tier + paid | cursor.com**

An AI-first editor worth exploring if you want to go deeper post-workshop.

---

## Knowledge Base

### Obsidian
**Free | obsidian.md**

Download the Windows installer from obsidian.md or run `winget install Obsidian.Obsidian`. Store your Obsidian vault in your Windows Documents folder, not in WSL2, so it syncs with Obsidian Sync if you use it (or, if on native Git Bash: use the same Windows Documents location). We'll set this up during Install Block Two.

---

## Password and Secrets Management

### 1Password
**Paid (~$3/month) | 1password.com**

Download the standard Windows installer from 1password.com. You also need the CLI inside WSL2 (or, if on native Git Bash: install it with `winget install AgileBits.1Password.CLI`). Together, they let Claude Code access your secrets securely.

### Bitwarden
**Free + paid | bitwarden.com**

A solid free alternative to 1Password. Has both a Windows app and a CLI that works in WSL2 (or, if on native Git Bash: install the CLI with `winget install Bitwarden.CLI`). If you're not ready to pay for 1Password, Bitwarden covers the basics.

---

## Productivity

### PowerToys
**Free | Microsoft**

A set of power-user utilities for Windows from Microsoft. Highlights:
- **FancyZones**: Snap windows to custom layouts (like two terminals side by side)
- **Run**: A fast app launcher (similar to Mac's Spotlight)
- **Keyboard Manager**: Remap keys

Install: `winget install Microsoft.PowerToys`

### Flow Launcher
**Free | flowlauncher.com**

A fast app launcher for Windows. Open any app or file with a keyboard shortcut, similar to Mac's Spotlight or Raycast. Highly recommended once you're working faster and want to skip the mouse.

---

## Utilities

### ShareX
**Free | getsharex.com**

Screenshots and screen recording on Windows. Excellent for documenting your setup or sharing errors when asking for help.

### AutoHotkey
**Free | autohotkey.com**

Windows automation scripting. Once you're comfortable with Claude Code, AutoHotkey can complement it for desktop-level automation. Advanced. Don't worry about it for workshop day.

---

## File Navigation

One thing Windows users often want to figure out early: where their project files live.

**Native Git Bash folder:**
Your repo is in a normal Windows folder, usually under `C:\Users\[YourWindowsUsername]\Documents\agent-native-os`.

**Open a Git Bash folder in Windows Explorer:**
```bash
explorer .
```

**Open a WSL2 folder in Windows Explorer:**
```bash
explorer.exe .
```

**Access Windows files from WSL2:**
Your C: drive is at `/mnt/c/`
Your Documents folder: `/mnt/c/Users/[YourWindowsUsername]/Documents/`

(or, if on native Git Bash: use Windows paths directly, such as `~/Documents` or `/c/Users/[YourWindowsUsername]/Documents/`.)

**Access WSL2 files from Windows:**
In File Explorer address bar, type: `\\wsl$\Ubuntu\home\[yourusername]\`

**Tip:** Keep your coding projects inside WSL2 (`~/projects/`) for performance if you chose WSL2 (or, if on native Git Bash: keep projects in `Documents` or another normal Windows folder). Keep your Obsidian vault and documents in Windows (`C:\Users\...`) for easy access from Windows apps.

---

## After the Workshop

As your setup grows, explore:

- **n8n Desktop**: Workflow automation you can run locally (n8n.io)
- **Docker Desktop**: For running services locally (more advanced, post-workshop)
- **WSL2 + GPU passthrough**: If you want to run local AI models (very advanced), or, if on native Git Bash: start with Windows-native Ollama or LM Studio before adding WSL2 GPU work
