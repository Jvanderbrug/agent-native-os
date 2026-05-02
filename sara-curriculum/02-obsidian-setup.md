# Component 2: Your Second Brain (Obsidian)

## What is Obsidian?

Obsidian is a free note-taking app that stores everything as simple text files in a folder on your computer. Unlike Notion or Google Docs where your notes live on the internet, Obsidian notes are just files on your machine.

Why does that matter? Because Claude Code can read files on your computer. If your notes are in Obsidian, Claude can read them, search them, and add to them -- without needing to log into anything or connect to the internet.

The workshop calls this your **"second brain"** -- a place where your knowledge accumulates over time, and Claude can tap into it whenever you have a conversation.

---

## Why Obsidian instead of Notion or Google Docs?

This is the #1 question people ask. The answer comes down to one thing: **where do the files live?**

| Tool | Where your notes live | Can Claude read them directly? |
|------|----------------------|-------------------------------|
| **Google Docs** | On Google's servers (the cloud) | Not yet -- but we'll set up connections (MCPs) later today that can change this |
| **Notion** | On Notion's servers (the cloud) | Not yet -- same as above, MCPs can connect Claude to cloud tools |
| **Obsidian** | In a folder on your computer | Yes -- they're just files, Claude reads them like any other file |

It's not that Obsidian is a better note-taking app. It's that Obsidian stores files locally, and Claude Code works with local files. That's the match.

> **Tip:** You don't have to choose one or the other. Many people keep using Notion or Google Docs for collaboration and shared work, and use Obsidian as their personal knowledge base that Claude can access. They serve different purposes.

---

## What is a "vault"?

In Obsidian, a **vault** is just a folder on your computer. That's it. Obsidian calls it a vault, but it's literally a regular folder with text files inside it.

When you "create a vault," you're just telling Obsidian: "This is the folder where I want to keep my notes." Obsidian then watches that folder and shows you the contents in a nice interface.

> **Tip:** You don't need Obsidian open for Claude to read your notes. The notes are just files in a folder. Claude reads the folder directly. Obsidian is just a nice way for YOU to view and organize them.

---

## Setting it up (step by step)

### Step 1: Install Obsidian

Ask Claude: "Install Obsidian on my computer."

Or do it yourself: go to [obsidian.md](https://obsidian.md) and download the app. It's free.

### Step 2: Create your vault folder

Ask Claude: "Create a folder called second-brain in my Documents folder for my Obsidian vault."

Or create it yourself in Finder: go to Documents, right-click, New Folder, name it `second-brain`.

### Step 3: Open the vault in Obsidian

1. Open Obsidian
2. Click **"Open folder as vault"**
3. Navigate to **Documents > second-brain**
4. Click Open

You should see an empty Obsidian window. That's your blank second brain.

### Step 4: Add some starter folders

Ask Claude: "Create folders in my second-brain vault for daily briefings, research, meeting notes, projects, and ideas."

Or create them yourself in Obsidian by right-clicking in the sidebar.

Your vault now has a basic structure:

| Folder | What goes here |
|--------|---------------|
| **daily-briefings** | Where your overnight agent saves its research (set up later in the workshop) |
| **research** | Articles, findings, things you're learning |
| **meeting-notes** | Notes from calls and meetings |
| **projects** | Notes organized by project |
| **ideas** | A place to capture random thoughts |

This structure is just a starting point. Rename, reorganize, or add folders anytime.

---

## How content gets into your vault

This is the practical question: great, I have an empty vault -- **how does stuff actually end up in it?**

### Ways content flows in

**1. You ask Claude to save something.**
The simplest way. After a meeting or a work session, tell Claude what to save:
> "Save a note in my meeting-notes folder about today's call with the client. We discussed the timeline for the website redesign and agreed on a June 1 launch date."

Claude creates a file in the right folder with your content, formatted and ready.

**2. Automated agents save their output.**
Later in the workshop, you'll set up things like a daily briefing that runs overnight. The briefing results get saved to your `daily-briefings` folder automatically. You wake up and the notes are there.

**3. You drag and drop.**
If you have a file on your computer -- like a downloaded transcript or a PDF -- you can drag it into the Obsidian window or into the vault folder in Finder.

**4. You copy and paste.**
Open a new note in Obsidian (click the new note icon or press Cmd+N), paste in whatever you want to save.

### What about content in other apps?

Right now, Claude can only read what's on your computer. It doesn't have access to Zoom, Fathom, Notion, Gmail, or other apps -- **yet.**

Later today, we'll set up connections called **MCPs** that give Claude access to tools like Gmail, your calendar, web search, and more. And we'll set up **scheduled automations** that let Claude pull information from these sources and save it to your vault automatically -- even while you sleep.

But for now, before those connections are set up, if you have something like a meeting transcript in Zoom or Fathom, the flow is:
1. **Download** the transcript from Zoom/Fathom to your computer
2. **Tell Claude** to read it and save it to your vault
3. Claude reads the downloaded file, cleans it up, and saves it as a note

This is temporary. By the end of the workshop, much of this will be automated.

> **Tip:** Get in the habit of downloading transcripts and important documents to a consistent folder on your computer (like Downloads or a dedicated "inbox" folder). Then you can tell Claude: "Check my Downloads folder for any new transcripts and save them to my meeting-notes vault." One command, and it's filed.

---

## The big picture: container first, pipes later

Think of it this way:

- **Obsidian** = the container where knowledge lives
- **MCPs** (later components) = the pipes that connect Claude to your apps and data
- **Cron jobs** (later components) = the schedule that makes it all run automatically

Right now, we've built the container. In the next components, we'll connect the pipes and set up the schedule. By the end of the workshop, content will flow into your vault automatically -- briefings, research, summaries -- without you lifting a finger.

---

## Quick reference

| Question | Answer |
|----------|--------|
| What is it? | A note-taking app that stores files locally on your computer |
| Why not Notion/Google Docs? | Those store files in the cloud. Claude can read local files directly. |
| What's a vault? | Just a folder on your computer that Obsidian watches |
| Where does it live? | Wherever you created it (we used Documents/second-brain) |
| Does Obsidian need to be open? | No. The notes are files. Claude reads the folder, not the app. |
| How do notes get in? | Ask Claude, drag and drop, copy/paste, or automated agents save them |
| Is it free? | Yes |
| Can I still use Notion? | Absolutely. Obsidian is for your personal knowledge base that Claude accesses. Notion is for collaboration. |

---

## Glossary (Component 2)

| Term | What it means |
|------|---------------|
| **Obsidian** | A free note-taking app that stores notes as plain text files in a folder on your computer. Unlike cloud apps, the files are local -- which means Claude Code can read them directly. |
| **Vault** | What Obsidian calls a folder of notes. It's just a regular folder on your computer. Obsidian watches it and displays the contents in a nice interface. |
| **Second brain** | A personal knowledge base that grows over time. Your Obsidian vault is your second brain -- Claude can read it, add to it, and reference it in conversations. |
| **Local files** | Files that live on your computer (not on the internet). Obsidian stores notes as local files. Claude Code can read local files directly without needing to log into anything. |
| **Cloud / Cloud storage** | Files stored on someone else's servers, accessed through the internet. Notion, Google Docs, and Dropbox are cloud storage. Claude can't access these directly yet -- but MCPs (set up later in the workshop) bridge that gap. |
| **MCP (preview)** | A way to connect Claude to external services. We'll cover this in Components 3-6. For now, just know that MCPs are how we'll eventually connect Claude to Gmail, web search, and other tools. |

---

*Status: DRAFT v1 -- based on Sara's experience going through setup as a student*
