# Recommended Mac Apps

These aren't required for the workshop, but they'll make your life meaningfully better as you build your agent OS. All of them are either free or have free tiers.

---

## Terminals (Pick One)

Your terminal is where you talk to Claude Code. The built-in Mac Terminal works fine, but these are nicer.

### Ghostty (Recommended)
**Free | ghostty.org**

The fastest, most modern terminal available right now. Built by HashiCorp's founder, open source, and delightfully fast. This is what we use in the workshop.

Install: Download from ghostty.org or `brew install --cask ghostty`

### iTerm2
**Free | iterm2.com**

The longtime Mac developer favorite. Tons of features, highly customizable, excellent split-pane support. A solid choice if you want something battle-tested.

Install: `brew install --cask iterm2`

---

## Code & File Editors

### Visual Studio Code
**Free | code.visualstudio.com**

The most popular code editor in the world, and it has a Claude Code extension. Useful for seeing your files visually while Claude edits them. We'll use this briefly during the workshop.

Install: `brew install --cask visual-studio-code`

### Cursor
**Free tier + paid | cursor.com**

An AI-first code editor. If you want to go deeper into AI-assisted development after the workshop, Cursor is worth exploring. Not required for Day 1.

Install: `brew install --cask cursor`

---

## Knowledge Base

### Obsidian
**Free (with paid sync option) | obsidian.md**

A note-taking app that stores everything as plain text files on your computer. We use it as the foundation for your second brain — a searchable knowledge base that Claude can read and write. We'll set this up on Day 2.

Install: `brew install --cask obsidian` or download from obsidian.md

---

## Password and Secrets Management

### 1Password
**Paid (~$3/month) | 1password.com**

The gold standard for password management. More importantly for this workshop: it also stores API keys and secrets in a way that Claude Code can access securely. If you're not already using a password manager, start here.

Install: `brew install --cask 1password`

*Already using another password manager?* Bitwarden is a free alternative that also has a CLI. We'll show both options during the secrets module.

---

## Productivity

### Raycast
**Free (with paid Pro) | raycast.com**

An Alfred/Spotlight replacement that's become the power-user standard on Mac. Fast app launcher, clipboard history, window management, and — importantly — it has an AI mode that lets you trigger Claude from anywhere on your screen. Highly recommended.

Install: `brew install --cask raycast`

### CleanMyMac
**Paid | macpaw.com/cleanmymac**

Disk cleanup and system health. Optional, but good to have if your Mac is running slow or low on storage. Claude Code and its dependencies take up some space.

---

## Utilities

### Rectangle
**Free | rectangleapp.com**

Window snapping for Mac. Lets you move windows to halves and quadrants of your screen with keyboard shortcuts. Incredibly useful when you're working with a terminal on one side and a browser on the other.

Install: `brew install --cask rectangle`

### Warp
**Free tier | warp.dev**

An AI-native terminal that some people prefer over Ghostty. Has built-in AI command suggestions. Worth trying if the idea of AI right inside your terminal appeals to you.

Install: `brew install --cask warp`

---

## Setting Up Homebrew Quickly

If you want to install several of these at once, you can chain Homebrew commands:

```bash
# Install multiple apps in one command
brew install --cask ghostty obsidian visual-studio-code rectangle
```

---

## After the Workshop

Once you've got your agent OS running, you might also look at:

- **Arc Browser** — The browser built for people who live in tabs (arc.net)
- **Notion** — If you want your knowledge base to be collaborative and cloud-synced
- **n8n** — Workflow automation that works beautifully with Claude (we touch this in Guide 09)
