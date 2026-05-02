# Component 4: Exa MCP (AI-Powered Web Search)

## What is Exa?

Exa is a search engine designed for AI. While Google finds web pages that match your keywords, Exa finds content that's actually *about* what you're looking for -- and filters out the noise.

You might be thinking: "Claude can already search the web. Why do I need another search tool?"

Good question. Here's the difference:

| | Built-in WebSearch | Exa |
|--|-------------------|-----|
| **How it searches** | Like Google -- matches keywords | Understands meaning -- finds content that's *about* your topic |
| **Quality of results** | Everything -- ads, listicles, SEO-optimized fluff | High-quality content -- research, real articles, expert sources |
| **Content returned** | Links and titles (you have to open each page separately) | Can return the full text of articles directly |
| **Best for** | Quick lookups, fact-checking | Deep research, competitive intelligence, overnight briefings |
| **Setup required** | None -- already built in | API key + MCP configuration (this guide) |

**The short version:** Built-in search is like Googling. Exa is like a research assistant who already filtered out the junk and only shows you the good stuff. For your daily briefing (which runs overnight with no one reviewing results), quality matters a lot.

> **Tip:** You don't have to choose one or the other. Claude uses both. Built-in search is great for quick lookups during a conversation. Exa is better for the deep research tasks that run autonomously.

---

## Before you start

Make sure you've completed:
- **Component 3 (Security + 1Password)** -- you need 1Password set up with the CLI working
- **Exa account created** -- sign up at [exa.ai](https://exa.ai) and get your API key from the dashboard
- **API key stored in 1Password** -- saved as "Exa-API" in your Workshop-Keys vault

If you did the pre-workshop setup, all of this is already done.

---

## Setting it up

### Step 1: Create the wrapper script

Remember the wrapper pattern from Component 3? We're using it here. The wrapper script pulls your Exa API key from 1Password every time the tool starts.

Ask Claude:
> "Create a wrapper script for the Exa MCP server that pulls my API key from 1Password. My key is stored in the Workshop-Keys vault as Exa-API."

Claude will create a file at `~/.claude/exa-wrapper.sh` that looks like this:

```bash
#!/bin/bash
export EXA_API_KEY=$(op read "op://Workshop-Keys/Exa-API/credential")
exec npx -y exa-mcp-server "$@"
```

### Step 2: Make the script executable

Ask Claude: "Make the exa wrapper script executable."

Or in terminal:
```
chmod +x ~/.claude/exa-wrapper.sh
```

### Step 3: Add Exa as an MCP server

Ask Claude: "Add Exa as an MCP server using the wrapper script."

Or in terminal:
```
claude mcp add exa -s user -- ~/.claude/exa-wrapper.sh
```

**What `-s user` means:** This installs Exa at the "user" level, which means it's available in every project, not just the current one.

### Step 4: Verify it's connected

In terminal:
```
claude mcp list
```

You should see:
```
exa: ~/.claude/exa-wrapper.sh - ✓ Connected
```

If you see `✗ Failed to connect`, check:
- Is 1Password CLI signed in? (`op whoami`)
- Is the API key stored correctly? (`op item get "Exa-API" --vault="Workshop-Keys"`)
- Is the script executable? (`ls -la ~/.claude/exa-wrapper.sh` -- should show `rwx`)

### Step 5: Restart Claude Code

Close and reopen Claude Code so it picks up the new MCP server. In VS Code, close the Claude Code panel (click the X on the tab) and reopen it (Cmd+Shift+P → "Claude Code: Open").

### Step 6: Test it

Ask Claude:
> "Use Exa to search for the latest trends in AI consulting and give me the top 3 findings."

If Exa is working, Claude will use the Exa tool (you'll see it in the response) and return high-quality results. If Claude says "Exa isn't available" or uses WebSearch instead, restart Claude Code and try again.

---

## What you can do with Exa

Now that it's connected, here are things you can ask Claude that use Exa:

**Research a topic:**
> "Use Exa to find the most authoritative articles about [your industry topic] published in the last month."

**Monitor competitors:**
> "Use Exa to search for recent news about [competitor name] and summarize what they've been doing."

**Find expert content:**
> "Use Exa to find research papers or expert analysis on [topic you're studying]."

**Prepare for a meeting:**
> "Use Exa to research [person's name] and [their company]. I have a meeting with them tomorrow."

**Build your daily briefing (later in the workshop):**
Exa will be one of the main data sources for your overnight intelligence briefing. You'll configure which topics, competitors, and industries to track, and Exa will find the best content automatically.

---

## Exa vs. WebSearch: when to use which

You don't need to tell Claude which search tool to use most of the time -- it will choose. But if you want to be specific:

| Situation | Use |
|-----------|-----|
| Quick factual question ("What's the capital of France?") | WebSearch |
| Deep research on a topic | Exa |
| Finding a specific website or URL | WebSearch |
| Competitive intelligence | Exa |
| Current news headlines | WebSearch |
| Finding quality articles for your daily briefing | Exa |
| Checking if something is true | WebSearch |
| Understanding trends in your industry | Exa |

> **Tip:** If you want Claude to specifically use Exa, just say "Use Exa to..." at the start of your request.

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| "Exa isn't available in this session" | Restart Claude Code (close and reopen the panel) |
| "API key not configured" | Check 1Password: `op item get "Exa-API" --vault="Workshop-Keys"` |
| Exa shows `✗ Failed` in `claude mcp list` | Sign in to 1Password CLI: `op signin` |
| Results seem the same as regular search | Try a more research-oriented query. Exa shines on topics, not quick lookups. |

---

## Quick reference

| Question | Answer |
|----------|--------|
| What is it? | An AI-powered search engine that finds high-quality content |
| Why not just use built-in search? | Exa filters out junk and returns better sources -- critical for autonomous briefings |
| How much does it cost? | Free tier: 1,000 searches/month. Paid: starts at $5/month for more. |
| Where's my API key? | In 1Password, in your Workshop-Keys vault, saved as "Exa-API" |
| How do I know it's working? | `claude mcp list` should show `exa: ✓ Connected` |
| Do I always have to say "Use Exa"? | No -- Claude will choose the right search tool automatically |

---

## Glossary (Component 4)

| Term | What it means |
|------|---------------|
| **Exa** | An AI-powered search engine designed for research and deep information retrieval. Unlike Google, it understands the meaning of your query, not just the keywords. |
| **MCP (Model Context Protocol)** | The system that connects Claude Code to external tools and services. Exa connects through MCP so Claude can search the web using it. |
| **MCP server** | A specific tool connection. "Adding an MCP server" means connecting a new tool to Claude Code. Each tool (Exa, Gmail, Calendar, etc.) is its own MCP server. |
| **Wrapper script** | The small script that pulls your API key from 1Password and starts the Exa tool. This is what keeps your key out of config files. |
| **`claude mcp list`** | A terminal command that shows all your connected MCP servers and whether they're working. |
| **`claude mcp add`** | A terminal command that connects a new MCP server to Claude Code. |
| **`-s user`** | A flag that means "install this for my whole account" (not just this project). |
| **WebSearch** | Claude Code's built-in web search. Works without any setup. Good for quick lookups but not as powerful as Exa for research. |

---

*Status: DRAFT v1 -- based on Sara's experience setting up Exa as a student, including the 1Password wrapper pattern*
