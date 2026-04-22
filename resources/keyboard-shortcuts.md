# Keyboard Shortcuts — Claude Code and Terminal

Quick reference for shortcuts you'll use constantly. Save this page.

---

## Claude Code CLI Shortcuts

| Action | Shortcut |
|--------|----------|
| Exit Claude Code | `/exit` or `Ctrl + C` |
| Clear screen | `Ctrl + L` |
| Cancel current response | `Ctrl + C` (once, while Claude is typing) |
| Go to beginning of line | `Ctrl + A` |
| Go to end of line | `Ctrl + E` |
| Delete to beginning of line | `Ctrl + U` |
| Search command history | `Ctrl + R` (then type to search) |
| Previous command | Up arrow |
| Next command | Down arrow |
| Run a slash command | Type `/commandname` and press Enter |

---

## Terminal Shortcuts (Mac)

| Action | Shortcut |
|--------|----------|
| New terminal window | `Cmd + N` (in Terminal app) |
| New terminal tab | `Cmd + T` |
| Close tab | `Cmd + W` |
| Clear screen | `Cmd + K` or `Ctrl + L` |
| Copy | `Cmd + C` |
| Paste | `Cmd + V` |
| Interrupt running process | `Ctrl + C` |
| Pause process (background) | `Ctrl + Z` |
| Go to beginning of line | `Ctrl + A` |
| Go to end of line | `Ctrl + E` |
| Tab completion | `Tab` |
| Search history | `Ctrl + R` |
| Previous command | Up arrow |
| Jump word left | `Option + Left arrow` |
| Jump word right | `Option + Right arrow` |
| Delete previous word | `Option + Delete` |

**Ghostty-specific:**
| Action | Shortcut |
|--------|----------|
| New window | `Cmd + N` |
| New tab | `Cmd + T` |
| Split pane horizontal | `Cmd + D` |
| Split pane vertical | `Cmd + Shift + D` |
| Navigate panes | `Cmd + Option + Arrow` |

---

## Terminal Shortcuts (Windows Terminal / WSL2)

| Action | Shortcut |
|--------|----------|
| New tab | `Ctrl + Shift + T` |
| New window | `Ctrl + Shift + N` |
| Close tab | `Ctrl + Shift + W` |
| Next tab | `Ctrl + Tab` |
| Previous tab | `Ctrl + Shift + Tab` |
| Open Ubuntu | `Ctrl + Shift + [Ubuntu profile number]` |
| Copy | `Ctrl + Shift + C` |
| Paste | `Ctrl + Shift + V` |
| Search | `Ctrl + Shift + F` |
| Clear screen | `Ctrl + L` |
| Interrupt process | `Ctrl + C` |
| Tab completion | `Tab` |
| Previous command | Up arrow |
| Search history | `Ctrl + R` |
| Go to beginning of line | `Ctrl + A` |
| Go to end of line | `Ctrl + E` |

---

## Claude Code Slash Commands (Built-In)

| Command | What It Does |
|---------|-------------|
| `/exit` | Exit Claude Code |
| `/clear` | Clear conversation context and start fresh |
| `/help` | Show available commands |
| `/cost` | Show approximate cost of this session |
| `/status` | Show current Claude Code status |
| `/continue` | Continue the most recent conversation |

**Your custom commands** (add yours here as you build them):

| Command | What It Does |
|---------|-------------|
| `/morning` | Daily briefing |
| `/weekly-review` | Weekly review |
| | |

---

## Useful Terminal One-Liners

```bash
# See last 20 commands you ran
history | tail -20

# Find a file by name
find ~ -name "settings.json" 2>/dev/null

# See what's using a lot of disk space
du -sh ~/Documents/* | sort -rh | head -10

# Check if a port is in use (useful for MCP server debugging)
lsof -i :3000

# Kill a process by name
pkill -f "claude"

# Watch a file update in real-time (good for watching log files)
tail -f ~/logs/morning-briefing.log
```

---

## VS Code Shortcuts (When Using the Extension)

| Action | Mac | Windows |
|--------|-----|---------|
| Command palette | `Cmd + Shift + P` | `Ctrl + Shift + P` |
| Open file | `Cmd + P` | `Ctrl + P` |
| Toggle terminal | `` Ctrl + ` `` | `` Ctrl + ` `` |
| Open Claude panel | Find "Claude" in sidebar | Find "Claude" in sidebar |
| Explain selection | Highlight text, then right-click > Claude | Same |
| New file | `Cmd + N` | `Ctrl + N` |
| Save file | `Cmd + S` | `Ctrl + S` |
| Find in files | `Cmd + Shift + F` | `Ctrl + Shift + F` |

---

## Obsidian Shortcuts

| Action | Mac | Windows |
|--------|-----|---------|
| Quick open (search files) | `Cmd + O` | `Ctrl + O` |
| Search all notes | `Cmd + Shift + F` | `Ctrl + Shift + F` |
| New note | `Cmd + N` | `Ctrl + N` |
| Toggle sidebar | `Cmd + B` | `Ctrl + B` |
| Graph view | `Cmd + G` | `Ctrl + G` |
| Command palette | `Cmd + P` | `Ctrl + P` |
| Bold | `Cmd + B` | `Ctrl + B` |
| Italic | `Cmd + I` | `Ctrl + I` |
| Insert link | `Cmd + K` | `Ctrl + K` |
| Toggle checkbox | `Cmd + L` | `Ctrl + L` |
| Daily note | `Cmd + P` > "Open today's daily note" | Same |

---

## Tip: Build Your Own Cheatsheet

Add a section to this file for shortcuts you discover that aren't listed here. The best cheatsheet is the one that reflects how *you* actually work.
