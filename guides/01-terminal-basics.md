# Guide 01 - Terminal Basics

**When we cover this:** Welcome + Architecture / Lesson + Demo: Claude Code Is Not a Chatbot (10:00 to 10:45 AM CDT, 11:00 to 11:45 AM EDT). See the agenda in the README for the full day.
**Track adjustments:** Beginners go slower here. Builders and Architects can move faster.

> **Installer-flow students:** If your installer put you on native Windows Git Bash instead of WSL2/Ubuntu, use the Git Bash notes in each Windows section below. You should see a `$` prompt and can run the same basic commands from there.

---

## What Is a Terminal?

Here's the most important reframe of the whole day:

**A terminal is just a text-based chat with your computer.**

That's it. Instead of clicking buttons and icons, you type instructions and the computer responds with text. There's nothing magical or mysterious about it. If you can type a search into Google, you can use a terminal.

For decades, terminals were the only way to control a computer. Then we got graphical interfaces (icons, windows, mice), and most people stopped using them. But developers kept using terminals because they're actually *faster* for many things, especially the kind of things we're doing in this workshop.

And here's the thing: **Claude Code lives in the terminal.** To use it at its full power, you need to be comfortable in this environment.

By the end of this session, you will be. Promise.

---

## How to Open Your Terminal

### Mac
**Option 1:** Press `Cmd + Space`, type "Terminal", press Enter.
**Option 2:** Open Spotlight (the magnifying glass in your menu bar), type "Terminal".
**Option 3:** Applications > Utilities > Terminal.

If you installed Ghostty (recommended): Press `Cmd + Space`, type "Ghostty", press Enter. Same thing, just a nicer terminal.

### Windows
#### Windows Terminal with WSL2/Ubuntu
Open **Windows Terminal** (you installed this in prerequisites). Click the dropdown arrow next to the + tab button and choose **Ubuntu**. That's your WSL2 terminal.

If Ubuntu is your default profile: just open Windows Terminal and you're there.

#### Native Windows with Git Bash
Open **Git Bash** from the Start menu. Press the Windows key, type "Git Bash", and press Enter.

Use this path if the installer flow told you to use Git Bash or if Claude Code was installed on the Windows side. Git Bash gives you Bash-style commands without opening Ubuntu.

---

## Your First Look Around

When your terminal opens, you'll see something like this:

**Mac:**
```
tyfisk@MacBook-Pro ~ %
```

**Windows/WSL2:**
```
tyfisk@LAPTOP-ABC123:~$
```

**Windows/Git Bash:**
```
tyfisk@LAPTOP-ABC123 MINGW64 ~
$
```

This is called the **prompt**. It's the terminal telling you: "Ready. What do you want to do?"

The parts of it:
- Your **username** (the part before the @)
- Your **machine name** (after the @)
- Your current **location** (the `~` means your home folder)
- A **symbol** (% on Mac, $ on Linux/WSL2/Git Bash) means "ready"

You type after this prompt and press Enter to run a command. The terminal responds. That's the whole interaction pattern.

In Git Bash, `MINGW64` tells you that Git's Bash environment is active on Windows. It is not a folder. Type your command after the `$` prompt.

---

## Windows Paths: WSL2 vs. Git Bash

Both WSL2 and Git Bash let you type Unix-style commands, but they point at Windows files differently.

### Windows Terminal with WSL2/Ubuntu

WSL2 is a small Linux environment inside Windows. Your Linux home folder looks like this:

```bash
/home/yourname
```

Your Windows `C:` drive is mounted under `/mnt/c`:

```bash
cd /mnt/c/Users/WindowsName/Documents
```

Tools installed inside WSL2 are separate from tools installed on the Windows side. If a command works in Ubuntu but not in PowerShell or Git Bash, it is probably installed only inside WSL2.

### Native Windows with Git Bash

Git Bash starts in your Windows home folder using Bash-style paths:

```bash
/c/Users/WindowsName
```

A Windows path like this:

```text
C:\Users\WindowsName\Documents\agent-native-os
```

becomes this in Git Bash:

```bash
/c/Users/WindowsName/Documents/agent-native-os
```

`PATH` is the list of folders your terminal searches when you type a command. Git Bash uses your Windows PATH plus Git's own folders. If `claude` says `command not found`, Claude Code may be installed only inside WSL2, or it may be installed on Windows but not visible on Git Bash's PATH.

Use these checks:

```bash
pwd             # shows where you are
which claude    # shows where Git Bash finds claude, if it can
echo $PATH      # shows the folders Git Bash searches
```

---

## The 8 Commands You'll Actually Use

You don't need to memorize hundreds of commands. You'll use maybe 8 regularly. Here they are.

---

### `pwd` - Where am I?

**What it does:** Prints your current location (the folder you're "in")
**When to use it:** Whenever you're confused about where you are

```bash
pwd
```

Output:
```
/Users/tyfisk
```

This is your "current directory." Think of it like the open folder in File Explorer or Finder.

---

### `ls` - What's here?

**What it does:** Lists the files and folders in your current location
**When to use it:** Whenever you want to see what's in the current folder

```bash
ls
```

Output:
```
Desktop    Documents    Downloads    GitHub    Pictures
```

**Useful variations:**
```bash
ls -la          # Shows hidden files and more detail
ls Documents    # Lists what's inside the Documents folder
```

---

### `cd` - Go somewhere

**What it does:** Changes your current directory (like double-clicking a folder)
**When to use it:** To navigate into a project folder before working on it

```bash
cd Documents
```

Now you're inside Documents. Run `pwd` to confirm.

```bash
cd agent-native-os
```

Now you're inside the workshop folder.

**Going back up:**
```bash
cd ..
```
One `..` goes up one level (like clicking the back button in Finder).

**Going home:**
```bash
cd ~
```
`~` always means your home folder. No matter where you are, `cd ~` gets you home.

**Going somewhere in one shot:**
```bash
cd ~/Documents/agent-native-os
```

---

### `mkdir` - Make a new folder

**What it does:** Creates a new directory (folder)
**When to use it:** When Claude tells you to create a project structure

```bash
mkdir my-new-project
```

Or make nested folders all at once with `-p`:
```bash
mkdir -p projects/client-work/notes
```

---

### `cat` - Read a file

**What it does:** Prints the contents of a file to the terminal
**When to use it:** Quick look at what's in a file without opening an app

```bash
cat CLAUDE.md
```

This dumps the whole file to your screen. Good for small files.

---

### `cp` - Copy a file

**What it does:** Copies a file from one location to another
**When to use it:** Duplicating files, making backups

```bash
cp CLAUDE.md CLAUDE.md.backup
```

---

### `mv` - Move or rename a file

**What it does:** Moves a file, or renames it (same command, different use)
**When to use it:** Reorganizing, renaming

```bash
mv old-name.md new-name.md         # Rename
mv file.txt ~/Documents/file.txt   # Move
```

---

### `clear` - Clean up

**What it does:** Clears all the text from the terminal screen
**When to use it:** When it's gotten cluttered and you want a fresh view

```bash
clear
```

Or the shortcut: `Ctrl + L` (works on both Mac and Windows)

---

## Tab Completion - Your Best Friend

You will love this.

When you're typing a command, press **Tab** and the terminal will try to complete it for you. If you type `cd Docu` and press Tab, it becomes `cd Documents/` automatically.

If there are multiple matches, press Tab twice to see all options.

This saves hundreds of keystrokes per day and prevents typos. Use it constantly.

---

## Command History

You don't have to retype commands you've already run. Press the **Up arrow** key to cycle through your previous commands. Press Enter to run one again, or edit it first.

---

## Reading Error Messages

When something goes wrong, the terminal tells you. The messages can look intimidating at first, but they almost always contain the key information:

```
bash: cd: myproject: No such file or directory
```

Translation: "You tried to go to a folder called 'myproject' but it doesn't exist." Usually means a typo, or you're in the wrong parent folder.

```
Permission denied
```

Translation: "You don't have access to do that." On Mac or WSL2, you might need to put `sudo` in front of the command. It means "run as administrator" and it'll ask for your password. In Git Bash, reopen Git Bash as Administrator only if an installer explicitly tells you to.

**Rule of thumb:** Copy the exact error message and ask Claude. Ninety percent of the time Claude will tell you exactly what's wrong and how to fix it.

---

## Hands-On: Try These Now

Open your terminal and work through these in order:

```bash
# 1. Where are you?
pwd

# 2. What's here?
ls

# 3. Go to your Documents folder
cd ~/Documents

# 4. Confirm you're there
pwd

# 5. List what's in Documents
ls

# 6. Go into the workshop repo (adjust path if needed)
cd agent-native-os

# 7. List the workshop files
ls

# 8. Read the README
cat README.md

# 9. Go back home
cd ~

# 10. Celebrate: you're a terminal user now
echo "I did it"
```

---

## Mac vs. Windows: Side-by-Side Reference

| Task | Mac Terminal | Windows (WSL2/Ubuntu) | Windows (Git Bash) |
|------|-------------|------------------------|--------------------|
| Open terminal | Cmd + Space, type "Terminal" | Open Windows Terminal, select Ubuntu | Start menu, type "Git Bash" |
| Home folder location | `/Users/yourname` | `/home/yourname` | `/c/Users/WindowsName` |
| List files | `ls` | `ls` (same) | `ls` (same) |
| Change directory | `cd foldername` | `cd foldername` (same) | `cd foldername` (same) |
| Clear screen | `clear` or Ctrl+L | `clear` or Ctrl+L (same) | `clear` or Ctrl+L (same) |
| Run as admin | `sudo command` | `sudo command` | Reopen Git Bash as Administrator only when required |
| See Windows files | n/a | `cd /mnt/c/Users/WindowsName/` | `cd /c/Users/WindowsName/` |
| Find where a command lives | `which claude` | `which claude` | `which claude` |
| Open folder in Finder/Explorer | `open .` | `explorer.exe .` | `explorer.exe .` |

---

## What You Just Learned

- A terminal is a text-based interface for your computer: not scary, just different
- The 8 commands you'll use most: `pwd`, `ls`, `cd`, `mkdir`, `cat`, `cp`, `mv`, `clear`
- Tab completion saves time and prevents typos
- WSL2 and Git Bash both use Bash-style commands, but their paths and installed tools can differ
- Error messages are information, not failures. Read them and ask Claude

---

## Track Exercises

See `tracks/[your-track]/exercises.md` - Exercise Set 01.

---

*Next up: Guide 02 - The Three Ways to Use Claude*
