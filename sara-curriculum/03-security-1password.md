# Component 3: Security and Secrets (1Password)

## Why this comes first

In the next few components, you're going to connect Claude Code to external services -- web search, email, calendar, and more. Every one of these connections requires an **API key** (a password-like code that gives Claude permission to use the service on your behalf).

Before we start connecting things, you need to know how to handle these keys safely. This component sets up the system you'll use for every connection from here on out.

---

## What is an API key?

An API key is like a hotel key card. It proves you're authorized to access a specific service. When Claude Code connects to Exa (web search) or Gmail or any other tool, it shows the API key to prove it has your permission.

**Why they matter:**
- Anyone with your API key can use the service as if they're you
- Some services charge by usage -- if someone gets your key, they could run up your bill
- Unlike a password, you can't hide an API key behind two-factor authentication

So we treat API keys like we treat car keys: we know where they are, we don't leave them lying around, and we don't hand them to strangers.

---

## What is 1Password?

1Password is a secure vault for storing passwords, API keys, and other secrets. Think of it as a safe that lives on your computer and in the cloud. You put your keys in the safe, and when Claude needs one, it opens the safe, grabs the key, uses it, and puts it back.

**Why not just paste the key into the chat?**
- Conversations can be logged, saved, or shared
- If you paste a key into the chat, it's now sitting in your conversation history
- 1Password keeps the key out of the conversation entirely

**Why not just save it in a file?**
- Files can accidentally get committed to git and shared publicly
- Files can be scattered across your computer with no organization
- 1Password is one place for everything, with encryption and access control

---

## Setting it up

### Step 1: Create your 1Password account

If you don't already have one:
1. Go to [1password.com](https://1password.com) and create a free personal account
2. Download and install the 1Password desktop app
3. Sign in

### Step 2: Install the 1Password CLI

The CLI (command-line interface) is what lets Claude pull keys from 1Password without you having to open the app, find the key, and copy-paste it.

Ask Claude: "Install the 1Password CLI on my computer."

Or install it yourself:
```
brew install 1password-cli
```

### Step 3: Connect the CLI to your account

Ask Claude: "Connect my 1Password CLI to my account."

Or do it yourself:
```
op signin
```

Follow the prompts to sign in. When it's done, verify it works:
```
op whoami
```

You should see your name and account info.

### Step 4: Create a vault for your API keys

A vault is like a folder inside your safe. We'll create one specifically for workshop keys.

Ask Claude: "Create a 1Password vault called Workshop-Keys."

Or do it yourself:
```
op vault create "Workshop-Keys"
```

---

## How to store an API key

When you sign up for a service like Exa (web search) or Firecrawl (web scraping), you'll get an API key from their website. Here's what to do with it:

**Step 1:** Copy the key from the service's website

**Step 2:** Store it in 1Password. Ask Claude:
> "Store this API key in my Workshop-Keys vault as Exa-API."

Or use the terminal:
```
op item create --category="API Credential" --title="Exa-API" --vault="Workshop-Keys" "credential=YOUR-KEY-HERE"
```

**Step 3:** Close the tab where the key was displayed. You don't need it anymore -- it's in 1Password now.

> **Important:** Never paste an API key directly into the Claude Code chat. Save it in 1Password first, THEN tell Claude to pull it from there. The key goes from your clipboard to 1Password to Claude's configuration -- it never appears in your conversation.

---

## How Claude uses your keys (the wrapper pattern)

This is the part that matters for the workshop. When we connect Claude to a service like Exa, we need Claude to be able to read the API key. But we don't want the key sitting in a config file on your computer.

The solution is a **wrapper script** -- a tiny file that:
1. Pulls the key from 1Password
2. Hands it to the tool
3. The key only exists in memory while the tool is running

Here's what it looks like in practice:

**The wrapper script** (a file on your computer):
```bash
#!/bin/bash
export EXA_API_KEY=$(op read "op://Workshop-Keys/Exa-API/credential")
exec npx -y exa-mcp-server "$@"
```

**What each line does:**
- Line 1: Says "this is a shell script"
- Line 2: Pulls the key from 1Password and stores it temporarily in memory
- Line 3: Starts the Exa tool with the key available

You don't need to write these scripts yourself -- Claude will create them for you. But it helps to know what's happening under the hood.

**The key point:** Your config file just says "run this script." The script pulls the key from 1Password on the fly. No key stored in any file. If someone looked at your config, they'd see a path to a script, not a secret.

---

## The security model in plain English

Here's the full picture of how your keys are protected:

| Layer | What it does | Analogy |
|-------|-------------|---------|
| **1Password** | Stores and encrypts your keys | The safe where you keep your car keys |
| **Wrapper script** | Pulls key from 1Password when needed, keeps it in memory only | A valet who gets your keys from the safe, drives the car, and returns them |
| **Gitignore** | Prevents config files from being shared | A "do not copy" stamp on sensitive documents |
| **Conversation hygiene** | Keys never appear in chat | Not reading your credit card number out loud in public |

**What you're protected from:**
- Keys appearing in your conversation history
- Keys getting committed to git and shared publicly
- Keys sitting in plain text files on your computer
- Losing track of which keys you have and where they are

**What's normal and expected:**
- The key briefly exists in memory when the tool starts -- that's how computers work
- 1Password itself stores an encrypted copy of the key -- that's the point of a password manager

---

## Checking your setup

After setting up 1Password, verify everything:

| Check | How to verify | What you should see |
|-------|--------------|-------------------|
| 1Password CLI works | Type `op whoami` in terminal | Your name and account info |
| Vault exists | Type `op vault list` | "Workshop-Keys" in the list |
| Keys are stored | Type `op item list --vault="Workshop-Keys"` | Your API key items listed |

---

## Quick reference

| Question | Answer |
|----------|--------|
| What is 1Password? | A secure vault for storing API keys and passwords |
| Why do I need it? | Every external tool connection requires an API key. 1Password keeps them safe. |
| Can I skip this? | No -- the next components all depend on having API keys stored securely |
| Is it free? | Yes, 1Password has a free personal tier |
| Does Claude access 1Password directly? | Yes, through the CLI -- it pulls keys when needed |
| Where do my keys end up? | Only in 1Password and briefly in memory. Not in config files, not in chat. |
| How do I add a new key later? | Same process: copy from the service's website, store in 1Password, create a wrapper script |

---

## Glossary (Component 3)

| Term | What it means |
|------|---------------|
| **API key** | A password-like code that gives Claude Code permission to use an external service. Like a hotel key card -- it proves you're authorized. |
| **1Password** | A secure app for storing passwords and API keys. Your encrypted vault. |
| **1Password CLI** | A way to access 1Password from the terminal (where Claude Code runs) instead of opening the app. This is how Claude pulls keys automatically. |
| **Vault** | A folder inside 1Password for organizing your secrets. We created "Workshop-Keys" for this workshop. |
| **Wrapper script** | A tiny file that pulls an API key from 1Password and hands it to a tool. Keeps the key out of config files. |
| **`op read`** | The 1Password CLI command that reads a specific secret from your vault. |
| **`op://`** | The address format for secrets in 1Password. Like a URL but for your vault. Example: `op://Workshop-Keys/Exa-API/credential` |
| **Environment variable** | A temporary value stored in your computer's memory (not a file). The wrapper script puts your API key in an environment variable so the tool can use it, then it disappears when the tool stops. |
| **Gitignore** | A file that tells git "don't track or share these files." Used to prevent config files (which might reference secrets) from being shared. |

---

*Status: DRAFT v1 -- based on Sara's experience setting up 1Password and the Exa wrapper pattern*
