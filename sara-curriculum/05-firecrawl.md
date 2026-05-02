# Component 5: Firecrawl (Web Scraping)

## What is Firecrawl?

Firecrawl is a tool that lets Claude read websites -- the full content of web pages, not just search results.

You might think Claude can already do this. And it can, sort of. Claude has a built-in tool called WebFetch that can read simple web pages. But most modern websites are built with JavaScript, and WebFetch can't handle those. It sees a blank page or broken content.

**Real example:** When we tried to read the AI Build Lab page on Notion using WebFetch, it came back blank. Notion uses JavaScript to build the page in your browser, so WebFetch never sees the content. Firecrawl renders the page like a real browser would, then hands Claude the full text.

| | Built-in WebFetch | Firecrawl |
|--|------------------|-----------|
| **Simple web pages** (basic HTML) | Works fine | Works fine |
| **Modern websites** (JavaScript-heavy) | Sees blank or broken content | Renders the full page |
| **Crawl multiple pages** | One page at a time, manually | Can crawl an entire website automatically |
| **Extract specific data** | No -- you get the whole page | Yes -- "get me all the prices" or "find the team page" |
| **Setup required** | None -- built in | API key + MCP configuration |

**The short version:** WebFetch is like reading a physical newspaper -- works great for simple text. Firecrawl is like having a browser that reads the page for you -- it handles everything modern websites throw at it.

---

## Before you start

Make sure you've completed:
- **Component 3 (Security + 1Password)** -- you need 1Password set up with the CLI working
- **Firecrawl account created** -- sign up at [firecrawl.dev](https://firecrawl.dev) and get your API key from the dashboard
- **API key stored in 1Password** -- saved as "Firecrawl-API" in your Workshop-Keys vault

If you did the pre-workshop setup, all of this is already done.

---

## Setting it up

This follows the same wrapper pattern you used for Exa in Component 4. If that felt confusing the first time, this one will feel familiar.

### Step 1: Create the wrapper script

Ask Claude:
> "Create a wrapper script for the Firecrawl MCP server that pulls my API key from 1Password. My key is stored in the Workshop-Keys vault as Firecrawl-API."

Claude will create a file at `~/.claude/firecrawl-wrapper.sh` that looks like this:

```bash
#!/bin/bash
export FIRECRAWL_API_KEY=$(op read "op://Workshop-Keys/Firecrawl-API/credential")
exec npx -y firecrawl-mcp "$@"
```

### Step 2: Make it executable

Ask Claude: "Make the Firecrawl wrapper script executable."

Or in terminal:
```
chmod +x ~/.claude/firecrawl-wrapper.sh
```

### Step 3: Add Firecrawl as an MCP server

Ask Claude: "Add Firecrawl as an MCP server using the wrapper script."

Or in terminal:
```
claude mcp add firecrawl -s user -- ~/.claude/firecrawl-wrapper.sh
```

### Step 4: Verify it's connected

In terminal:
```
claude mcp list
```

You should see:
```
firecrawl: ~/.claude/firecrawl-wrapper.sh - ✓ Connected
```

### Step 5: Restart Claude Code

Close and reopen Claude Code so it picks up the new MCP server.

### Step 6: Test it

Ask Claude:
> "Use Firecrawl to read the homepage of [a website you know well] and summarize what it says."

Pick a website you're familiar with so you can verify the summary is accurate. If Claude returns a good summary of the page's content, Firecrawl is working.

---

## What you can do with Firecrawl

Now that it's connected, here are practical things you can ask:

**Read a competitor's website:**
> "Use Firecrawl to read [competitor's website] and tell me what services they offer and how they position themselves."

**Research a company before a meeting:**
> "Use Firecrawl to read [company website] and give me a summary of who they are, what they do, and any recent news on their site."

**Extract specific information:**
> "Use Firecrawl to read [website] and pull out all the pricing information."

**Crawl multiple pages:**
> "Use Firecrawl to crawl [website] and summarize what the company does, their team, and their blog posts."

**Save research to your vault:**
> "Use Firecrawl to read [article URL] and save a summary to my research folder in Obsidian."

---

## Firecrawl vs. Exa vs. WebSearch: which does what

You now have three ways Claude can get information from the web. Here's how they fit together:

| Tool | What it does | When to use it |
|------|-------------|---------------|
| **WebSearch** | Searches the web like Google | Quick factual lookups, finding a specific URL |
| **Exa** | AI-powered search that finds quality content | Deep research, competitive intelligence, daily briefing sources |
| **Firecrawl** | Reads the full content of a specific webpage | When you have a URL and need to read what's on it |

Think of it as a workflow:
1. **Search** (Exa or WebSearch) finds the relevant pages
2. **Firecrawl** reads the pages in full detail
3. Claude summarizes and saves the results

For your daily briefing, this combination is powerful: Exa finds the best articles on your topics, Firecrawl reads the full content, and Claude distills it into your morning briefing.

> **Tip:** You don't usually need to specify which tool to use. If you give Claude a URL and ask it to read the page, it will try WebFetch first. If that comes back blank or broken, tell Claude: "Use Firecrawl to read that page instead." Over time, you can add a standing rule to your CLAUDE.md: "When fetching web pages, use Firecrawl instead of WebFetch."

---

## Common issues and fixes

| Problem | Fix |
|---------|-----|
| "Firecrawl isn't available" | Restart Claude Code (close and reopen) |
| "API key not configured" | Check 1Password: `op item get "Firecrawl-API" --vault="Workshop-Keys"` |
| Firecrawl shows `✗ Failed` in `claude mcp list` | Sign in to 1Password CLI: `op signin` |
| Results come back empty for a page | Some pages block automated access. Try a different URL to confirm Firecrawl itself is working. |
| Claude uses WebFetch instead of Firecrawl | Say "Use Firecrawl to..." explicitly, or add a rule to your CLAUDE.md |

---

## Quick reference

| Question | Answer |
|----------|--------|
| What is it? | A tool that reads the full content of web pages, including JavaScript-heavy sites |
| Why not just use WebFetch? | WebFetch can't read modern websites (JavaScript). Firecrawl can. |
| How much does it cost? | Free tier: 500 credits. Paid plans available for more. |
| Where's my API key? | In 1Password, in your Workshop-Keys vault, saved as "Firecrawl-API" |
| How do I know it's working? | `claude mcp list` should show `firecrawl: ✓ Connected` |
| Do I need it for the daily briefing? | It's a powerful addition -- lets the briefing read full articles, not just search results |

---

## Glossary (Component 5)

| Term | What it means |
|------|---------------|
| **Firecrawl** | A tool that reads web pages like a real browser. It can handle modern JavaScript-heavy websites that simpler tools can't. |
| **Web scraping** | The process of automatically reading and extracting information from websites. Firecrawl is a web scraping tool. |
| **JavaScript** | A programming language that most modern websites use to build their pages dynamically. When a site "loads" after you open it, that's JavaScript running. WebFetch can't see content built by JavaScript; Firecrawl can. |
| **Render** | The process of building a web page so it looks the way you'd see it in a browser. Firecrawl "renders" pages, which means it runs the JavaScript and sees the final result -- just like your browser does. |
| **Crawl** | Reading multiple pages from a website automatically. Instead of giving Claude one URL at a time, Firecrawl can follow links and read an entire site. |
| **WebFetch** | Claude Code's built-in tool for reading web pages. Works for simple pages but fails on most modern websites. |
| **Wrapper script** | Same pattern as Component 4 -- a small script that pulls your API key from 1Password before starting Firecrawl. |

---

*Status: DRAFT v1 -- based on Sara's teaching prep and alignment docs*
