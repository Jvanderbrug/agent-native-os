# Guide 06 — Obsidian: Your Second Brain

**Session time:** 11:30 AM – 12:30 PM (Day 2)

---

## Why Your Agent OS Needs a Brain

Claude Code can read your email, check your calendar, and run commands. But there's a whole category of knowledge it doesn't have access to: *your knowledge*.

- How you think about your industry
- Notes from past client meetings
- Your system for managing projects
- Lessons you've learned that you don't want to repeat
- Reference material you've collected over years

This is what your second brain stores. And Obsidian is the best tool for building one that Claude can actually read and use.

---

## What Is Obsidian?

Obsidian is a note-taking app with two properties that make it perfect for an agent OS:

1. **Everything is plain text files.** Your notes are `.md` files on your computer — not locked in some company's cloud database. They're yours, forever.

2. **Claude can read them.** Because they're plain text files in a folder, Claude Code can search through them, reference them, and even update them. Your knowledge base becomes accessible to your agent.

Contrast this with Notion, Google Docs, or Evernote — those are great apps, but they lock your data in cloud databases that Claude can't directly access (you'd need an MCP server, and even then it's limited).

Obsidian gives you something simpler and more powerful: a folder of text files that both you and Claude can work with directly.

---

## Setting Up Obsidian

### Install Obsidian

**Mac:**
```bash
brew install --cask obsidian
```
Or download from **obsidian.md**

**Windows:**
Download the Windows installer from obsidian.md. Install to your Windows side (not inside WSL2) — Obsidian is a desktop app.

### Create Your Vault

1. Open Obsidian
2. Choose "Create new vault"
3. Name it something like "My Second Brain" or your name
4. **Choose the location carefully:**
   - **Mac:** Put it in `~/Documents/` or `~/Obsidian/`
   - **Windows:** Put it in `C:\Users\[YourName]\Documents\Obsidian\` — NOT inside WSL2

This vault is a folder. Inside it, every note is a `.md` file.

### Set Up Basic Folders

Create these folders inside your vault (you can create them in Obsidian or in Finder/Explorer):

```
Your Vault/
├── Inbox/          ← Quick capture, process later
├── Areas/          ← Ongoing areas of responsibility
├── Projects/       ← Active projects with start + end
├── Resources/      ← Reference material
├── Archive/        ← Completed things
└── Daily Notes/    ← Daily log (optional but powerful)
```

This structure is based on the PARA method by Tiago Forte — one of the most widely used second-brain frameworks.

---

## Connecting Obsidian to Claude Code

Here's where it gets powerful. Since your vault is just a folder of text files, Claude can work with it directly.

### Point Claude to Your Vault

Add this to your `CLAUDE.md`:

```markdown
## My Knowledge Base

My Obsidian vault is located at:
[Mac]: /Users/[yourname]/Documents/My Second Brain/
[Windows]: /mnt/c/Users/[yourname]/Documents/Obsidian/My Second Brain/

Structure:
- Inbox/ — unprocessed captures
- Areas/ — ongoing responsibilities
- Projects/ — active projects
- Resources/ — reference material
- Archive/ — completed

When I ask about something that might be in my notes, search this vault first.
When I ask you to capture something, add it to Inbox/ as a new note.
```

### Test It

```bash
cd agent-native-os
claude
```

Ask:
```
> Check my Obsidian inbox and tell me what's there
```

If your vault path is correct in CLAUDE.md, Claude will navigate to your Inbox folder and list (or summarize) what's in it.

```
> Create a new note in my Obsidian Inbox called "Workshop Notes" and add my key takeaways from today
```

Claude will create a new `.md` file in your Inbox folder. Open Obsidian — you'll see it there.

---

## Practical Use Cases

Once your vault is connected, here's what becomes possible:

**Meeting notes:**
```
> I just got off a call with Jennifer at Cascade Health. She wants to expand our contract to cover their Austin office. Create a meeting note in my Projects folder for the Cascade Health account.
```

**Research capture:**
```
> I read an interesting article about async team communication. Save a note in Resources/ with the key ideas: [paste the ideas]
```

**Weekly review:**
```
> Look at everything in my Inbox and suggest how to organize each item into Areas, Projects, or Resources
```

**Project status:**
```
> Read my Projects/Website Redesign folder and give me a status summary
```

**Find something:**
```
> Do I have any notes about pricing strategy?
```

---

## The Obsidian Daily Note

One of the most powerful habits: open a Daily Note every morning and have Claude populate it.

In Obsidian settings, enable "Daily Notes" (under Core Plugins). Set the folder to `Daily Notes/` and a template path.

Create a template file at `Templates/Daily Note Template.md`:

```markdown
# {{date}}

## Today's Priorities
- [ ] 
- [ ] 
- [ ] 

## Scheduled
(from calendar)

## Notes

## End of Day

```

Then each morning, ask Claude:
```
> Pull my calendar for today and fill in the Scheduled section of today's daily note in Obsidian
```

Claude will look at your Google Calendar (via MCP) and write the entries into your daily note. You start every day already organized.

---

## Obsidian Plugins Worth Knowing

Obsidian has a plugin ecosystem. These are worth installing (in Obsidian: Settings > Community Plugins):

**Templater** — More powerful templates than the built-in one. Worth it if you want to automate note creation.

**Dataview** — Query your notes like a database. Show all notes tagged `#client` modified in the last 7 days, etc. Very powerful once you have a large vault.

**Calendar** — Visual calendar in the sidebar showing which days have daily notes.

**Omnisearch** — Better full-text search across your whole vault.

---

## A Note on Sync

Obsidian stores files locally. If you use multiple computers, you'll need a sync solution:

- **Obsidian Sync** (~$4/month) — The official solution, end-to-end encrypted
- **iCloud** (Mac only) — Free, works fine if you only use Macs
- **Dropbox / OneDrive / Google Drive** — Free options, work across platforms

For the workshop, local is fine. Think about sync when you're ready to use this daily.

---

## What You Just Built

- An Obsidian vault set up with the PARA structure
- Claude Code knows where your vault is and can read/write it
- The pattern for using natural language to capture, retrieve, and organize your knowledge

---

## Track Exercises

See `tracks/[your-track]/exercises.md` — Exercise Set 06.

---

*Next up: Guide 07 — Custom Commands*
