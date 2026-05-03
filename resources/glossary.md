# Glossary - Plain English Definitions

Every term used in this workshop, explained without jargon.

If you hear a term in the workshop that's not here, write it down and ask. We'll add it.

---

## A

**Agent**
An AI system that can take actions - not just answer questions. An agent can read files, call APIs, send emails, and complete multi-step tasks. Claude Code is an agent when it's doing things, not just talking.

**Agent OS (Agent Operating System)**
The combination of tools, configurations, and connections that let you work with AI agents effectively. Your CLAUDE.md + MCP servers + custom commands + Obsidian vault = your agent OS.

**API (Application Programming Interface)**
A way for software to talk to other software. When Claude uses your Gmail, it's using Gmail's API. APIs usually require an "API key" to prove who's asking.

**API Key**
A long string of letters and numbers (like a password) that proves your identity to a service. Keep these private - they give access to your accounts. Example: `sk-xxxxxxxxxxxxxxxx`.

**Anthropic**
The company that makes Claude. Founded in 2021, focuses on AI safety.

**Autonomy Level**
A setting in your CLAUDE.md that controls how independently Claude acts. Safe Mode = asks before doing anything. Autopilot = acts unless something seems risky.

---

## B

**Bash**
A language for writing terminal commands and scripts. When you type commands in the terminal, you're often writing Bash. Shell scripts (`.sh` files) are usually Bash programs.

**Blueprint**
In this workshop: a pre-built, documented workflow you can deploy without building from scratch. See `blueprints/README.md`.

---

## C

**CLI (Command Line Interface)**
Another term for the terminal - the text-based interface for interacting with your computer. Claude Code CLI = Claude Code running in the terminal.

**Claude**
The AI assistant made by Anthropic. Claude Code is the version that can take actions on your computer. Claude.ai is the web chat interface.

**Claude Code**
The agentic version of Claude that runs in your terminal and can read/write files, run commands, and connect to external services via MCP servers.

**Claude Max**
The paid subscription tier required to use Claude Code comfortably. Comes in two flavors: **Max 5x ($100/month)** is the workshop minimum, and **Max 20x ($200/month)** is recommended for power users. Pro ($20/month) technically has Claude Code access too, but rate limits hit fast on a workshop day.

**CLAUDE.md**
A markdown file that gives Claude persistent context about who you are. Automatically read at the start of every session. The foundation of your agent OS.

**Context**
The information Claude knows going into a conversation. Your CLAUDE.md is context. Files you share are context. The conversation history is context.

**Cron**
A Unix/Mac/Linux scheduler for running commands on a schedule. `crontab -e` edits your schedule. Common syntax: `30 7 * * 1-5` means "7:30 AM, Monday through Friday."

---

## D

**Directory**
The technical term for a folder. "Navigate to a directory" = go into a folder.

**dotfiles**
Configuration files on Unix/Mac systems that start with a `.` (dot). They're hidden by default. `.zshrc`, `.claude/settings.json`, `.gitconfig` are all dotfiles.

---

## E

**Environment Variable**
A named value stored in your terminal session. `BRAVE_API_KEY=mykey123` sets an environment variable called `BRAVE_API_KEY`. Programs can read these values without them being hardcoded.

**ExecutionPolicy**
A PowerShell security setting that controls whether scripts are allowed to run. If a Windows install command is blocked, set `RemoteSigned` for your current user instead of weakening policy for the whole machine.

---

## G

**Git**
Version control software - tracks changes to files over time. Think of it like Track Changes in Word, but for any file, forever. GitHub is a website for storing git repositories.

**Git Bash**
The Bash terminal that comes with Git for Windows. It gives Windows users familiar Unix-style commands without installing WSL2. Native Windows Claude Code may use Git Bash to run shell commands.

**GitHub**
A website for storing and sharing code repositories (folders tracked by git). You have a free account. We use it to store your workshop files.

**GitHub CLI (gh)**
A command-line tool for interacting with GitHub. `gh auth login`, `gh repo clone`, `gh pr create` etc.

**GUI (Graphical User Interface)**
The visual, clickable interface for a program. The Claude Desktop App has a GUI. The Claude Code CLI does not - it's text only.

---

## H

**Headless**
Running a program without a visible interface. "Headless mode" for Claude Code = running a command without entering the interactive session. Example: `claude -p "Summarize this file"`.

**Homebrew**
The package manager for Mac - the easiest way to install developer tools. `brew install` is how you install things.

**Hook**
A function or command that runs automatically when a specific event happens. Claude Code hooks can run when a session starts, ends, or when a tool is called.

---

## J

**JSON**
JavaScript Object Notation - a text format for structured data. Your `settings.json` file is JSON. It uses `{curly braces}`, `"quotes"`, `[brackets]`, and commas. Very picky about syntax - one missing comma breaks the whole thing.

---

## K

**Keychain**
Mac's built-in password and credential storage. More secure than a text file because it's encrypted and locked to your Mac account.

---

## L

**Launchd**
Mac's built-in system for scheduling tasks (more powerful than cron, but more complex). For simple scheduled tasks in this workshop, we use cron instead.

---

## M

**Markdown**
A simple text format where special characters create formatting. `**bold**` becomes **bold**, `# Heading` becomes a heading. CLAUDE.md is written in markdown. Obsidian displays markdown beautifully.

**MCP (Model Context Protocol)**
An open standard that lets Claude connect to external tools and services. An MCP server is a small program that bridges Claude to Gmail, Notion, Slack, etc.

**MCP Server**
A program that runs on your computer and gives Claude access to a specific external service. Once configured in `settings.json`, Claude can use it like a built-in capability.

---

## N

**n8n**
A workflow automation platform (like Zapier, but self-hostable and more powerful). Can trigger Claude Code workflows based on events like new emails, form submissions, or webhooks.

**Node.js**
A JavaScript runtime - the engine that runs JavaScript code outside of a browser. Required for Claude Code and many MCP servers. Installed with `brew install node` (Mac) or `sudo apt install nodejs` (WSL2).

**npm**
Node Package Manager - the tool for installing JavaScript packages. `npm install -g` installs a package globally (available everywhere on your system).

---

## O

**OAuth**
A secure way to let one application access another without sharing your password. When you click "Sign in with Google," that's OAuth. Many MCP server connections use OAuth.

**Obsidian**
A note-taking app that stores notes as plain text markdown files. Used in this workshop as your knowledge base / second brain.

**op**
The 1Password command-line tool. `op read`, `op signin`, `op whoami`.

**op:// reference**
A URL format that tells the 1Password CLI where to find a secret. Example: `op://Personal/Gmail Credentials/credential`. Safer than storing secrets as plain text.

---

## P

**PARA**
A knowledge organization system: Projects, Areas, Resources, Archive. A way to structure your Obsidian vault developed by productivity author Tiago Forte.

**PATH**
A list of folders your computer looks in when you type a command. If `claude` isn't found, it means the folder containing Claude isn't in your PATH.

**Permissions**
Controls over what Claude Code is allowed to do without asking. Configured in `settings.json`. Safe by default - Claude asks before most actions.

**Prompt**
1. In the terminal: the `$` or `%` symbol where you type commands.
2. In AI: the text you send to Claude to get a response.

---

## R

**Repository (repo)**
A folder tracked by git. When you "clone a repo," you're downloading a git-tracked folder to your computer.

**Root**
The top-level directory of your computer (`/` on Mac/Linux, `C:\` on Windows). Your home folder is one level down.

---

## S

**Safe Mode**
An autonomy level for Claude Code where it asks for confirmation before taking any action. Recommended for beginners and for new workflows.

**Session**
A single Claude Code run - from when you type `claude` to when you type `/exit`. Each session starts with your CLAUDE.md context.

**settings.json**
The main configuration file for Claude Code. Lives at `~/.claude/settings.json`. Controls MCP servers, permissions, and hooks.

**Shell**
The program that interprets terminal commands. On Mac: zsh (the default). On WSL2/Linux: bash. `.zshrc` and `.bashrc` are the configuration files for each.

**Slash Command**
A command triggered by typing `/name`. Built-in examples: `/exit`, `/help`. Your custom commands become slash commands.

**SSH**
Secure Shell - a way to securely connect to another computer's terminal over a network. Used for connecting to servers remotely.

**sudo**
"Super user do" - runs a command with administrator privileges. Used when normal user permissions aren't sufficient. Will ask for your password.

---

## T

**Terminal**
The text-based interface for interacting with your computer. Also called: command line, shell, console, CLI.

**Token (AI)**
The unit of text that AI models process. Roughly 3/4 of a word. Claude Max gives you a large token budget per month.

**Token (auth)**
A credential string used to prove identity to a service. Like an API key but often temporary.

---

## V

**Vault**
In Obsidian: the folder containing all your notes. In 1Password: the secure container holding your credentials.

**Version Control**
Tracking changes to files over time so you can see history, revert changes, and collaborate. Git is the version control system we use.

---

## W

**WSL2 (Windows Subsystem for Linux 2)**
A Linux environment that runs inside Windows. Gives Windows users a real Unix-like terminal. Required for Claude Code on Windows.

**winget**
Windows Package Manager. A command-line installer built into modern Windows. Example: `winget install --id Git.Git -e`.

**winpty**
A Git Bash helper that gives some Windows command-line programs a usable interactive terminal. If `claude` hangs or input behaves strangely in Git Bash, `winpty claude` may fix it.

---

## Z

**zsh**
The default shell on modern Macs. Similar to bash. Configuration file: `~/.zshrc`.

---

*Missing a term? Add it here or ask in the community Slack.*
