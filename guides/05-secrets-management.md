# Guide 05, Secrets Management

**When we cover this:** Install Block Three: Connect Data Sources + First Fleet Run (2:15 PM CDT, 3:15 PM EDT). Secrets management is part of wiring tools in safely. See the README for the full agenda.

---

## The Problem We're Solving

When you connect Claude to external tools, you need API keys, little strings of text that prove to Gmail or Notion or Slack that you're authorized to use their APIs.

The bad way to handle these: paste them directly into config files as plain text. The problem is those files can end up on GitHub, be read by other programs, or just sit there waiting to be found.

**We need a better system.** And we have one.

---

## The Concept: Never Store Secrets As Plain Text

The goal is simple: API keys should never live in a file you might accidentally share. They should live in a **secure vault** and only be fetched when actually needed.

This is what 1Password is for.

Here's the pattern we use:
1. Store your API key in 1Password (your vault)
2. In your Claude Code config, reference the key as `op://YourVault/YourItem/field` instead of the actual key
3. When Claude Code starts, it fetches the real value from 1Password automatically
4. The actual key never sits in a plain text file

---

## Mac: Using 1Password + Keychain

### Step 1: Store Your First Secret in 1Password

1. Open 1Password
2. Create a new item: click the + button
3. Choose "API Credential" (or just "Secure Note")
4. Name it clearly, e.g., "Brave Search API Key"
5. Add a field called "credential" and paste your API key there
6. Save

### Step 2: Find the op:// Reference

In 1Password, right-click any field and look for "Copy Secret Reference." This gives you an `op://` path like:

```
op://Personal/Brave Search API Key/credential
```

This is what you put in your config file instead of the actual key.

### Step 3: Update Your settings.json

Before:
```json
"env": {
  "BRAVE_API_KEY": "BSA_xxxxxxxxxxxxxxxxxxxxxxxx"
}
```

After:
```json
"env": {
  "BRAVE_API_KEY": "op://Personal/Brave Search API Key/credential"
}
```

### Step 4: Make Sure the CLI is Linked to 1Password App

```bash
# This should show your account email
op whoami

# If it's not working, open 1Password app:
# Settings > Developer > Enable "Integrate with 1Password CLI"
```

Now when Claude Code starts, it automatically resolves any `op://` references by talking to your 1Password app. The real API key is fetched in memory but never written to disk.

### Mac Keychain (Advanced)

For extra security, you can also store the 1Password service account token itself in the Mac Keychain (your system's secure credential storage). This is covered in the Architect track exercises. Don't worry about it during the live workshop.

---

## Windows: Using 1Password + Windows Credential Manager

### Step 1: Store Your First Secret in 1Password

Same as Mac. Open 1Password, create an API Credential item, add your key to a field called "credential."

### Step 2: Install 1Password CLI in Your Windows Terminal

You have two supported paths. Use the one that matches the terminal where you run Claude Code.

**Option A: Git Bash with native Windows `op.exe`**

Install the native 1Password CLI:

```bash
winget install --id AgileBits.1Password.CLI -e
```

Then verify from Git Bash:

```bash
op.exe --version
op.exe whoami
```

If `op` is on your PATH, `op whoami` may also work. `op.exe whoami` is the explicit native Windows check.

**Option B: WSL2/Ubuntu with Linux `op`**

You should have done this in prerequisites. Verify:

```bash
op --version
op whoami
```

Both paths work the same for Claude Code. The native Windows `op.exe` installed by `winget` and the WSL2 `op` installed inside Ubuntu both resolve the same `op://` secret references.

### Step 3: Use op:// References

Same as Mac. Replace plain API keys with `op://` references in your settings.json. The reference format is identical on Mac, Git Bash, and WSL2:

```json
"env": {
  "BRAVE_API_KEY": "op://Personal/Brave Search API Key/credential"
}
```

### Step 4: Sign In When Prompted

The first time you start a session, 1Password CLI may ask you to authenticate (fingerprint on Mac, PIN or password on Windows). After that, it caches your session for a period of time.

---

## The .env Pattern (Intermediate)

For situations where you have multiple secrets that many tools need, a common pattern is a `.env` file that loads all secrets into environment variables:

Create `~/.claude-secrets.env`:
```bash
export BRAVE_API_KEY="op://Personal/Brave Search API Key/credential"
export NOTION_TOKEN="op://Personal/Notion API Token/credential"
export OPENAI_API_KEY="op://Personal/OpenAI API Key/credential"
```

Then in your shell config (`.zshrc` on Mac, `.bashrc` on WSL2, or `.bashrc` / `.bash_profile` in Git Bash):
```bash
# Load Claude secrets
if [ -f ~/.claude-secrets.env ]; then
  source ~/.claude-secrets.env
fi
```

Now every terminal session automatically has these environment variables available, and they're all pulling from 1Password, never stored as plain text.

---

## What NOT to Do

**Don't put API keys in:**
- Your `CLAUDE.md` (it's version controlled)
- Any file you might push to GitHub
- A note in Notion or Google Drive (cloud-synced)
- Your chat history (screenshots, etc.)

**Signs you've done this wrong:**
- Your settings.json has a long random string that starts with `sk-` or `BSA-` or similar
- You've pasted an API key into a git commit
- You have a file called `secrets.txt` anywhere on your computer

If any of those apply, rotate the exposed key immediately (log into the service and generate a new one). The old one should be considered compromised.

### Free / open-source alternatives

If 1Password is a hard no for cost or other reasons, there are free alternatives that follow the same `op://`-style reference pattern. The workshop teaches 1Password as the default, but these are supported:

- **Bitwarden** ([bitwarden.com](https://bitwarden.com)): free tier with personal vault. Has a CLI (`bw`) similar to `op`.
- **Infisical** ([infisical.com](https://infisical.com)): open-source, self-hostable. Good for team-scale post-class.

Both fit the "secrets in encrypted store, agents read by reference" pattern. If you go this route, use the `.env` with `chmod 600` path during the workshop and migrate to your manager of choice after.

---

## Rotating a Key

When you need to change an API key (because it's expired, compromised, or you just want to):

1. Generate a new key in the service (Gmail, Notion, etc.)
2. Update the item in 1Password with the new key
3. Restart Claude Code. It fetches fresh from 1Password on each session

Since your config file uses `op://` references (not the key itself), you only update 1Password. Your config file doesn't change.

---

## Managing Multiple Services

As you add more MCPs, you'll accumulate more API keys. Keep them organized in 1Password:

- Create a folder called "Claude MCP Keys" or similar
- Put all workshop-related API credentials in it
- Name each item clearly: "Gmail OAuth Credentials", "Notion Integration Token", etc.

When someone (or Claude) asks "what API keys do you have?", you can answer clearly without exposing the actual values.

---

## A Word on Trust

You're giving Claude access to real accounts: your Gmail, your calendar, your files. This deserves a moment of thought.

Claude Code is running locally on your machine. It's not sending your emails to a third-party server. It's using the same credentials *you* use when you log into Gmail, just doing it programmatically.

The risk model is similar to: "If someone else sat at my computer with my browser logged in, what could they do?" The answer is: a lot. That's why we:

1. Store credentials in 1Password, not plain text
2. Keep your Claude Code autonomy level at Safe Mode initially
3. Review what Claude is about to do before it does it

The safety comes from the system, not from blind trust.

---

## What You Just Built

- API keys stored in 1Password, not in config files
- op:// references in your settings.json for any MCPs you've connected
- An understanding of the right pattern for adding future secrets

---

## Track Exercises

See `tracks/[your-track]/exercises.md`, Exercise Set 05.

---

*That wraps the secrets block. Coming up: Obsidian, custom commands, connecting your world, and putting it all together.*
