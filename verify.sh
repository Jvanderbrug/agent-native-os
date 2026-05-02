#!/bin/bash
# Agent Native OS — Setup Verification Script
# Run before workshop day. Usage: bash verify.sh
# Windows users: run this inside WSL2 (Ubuntu). See setup/windows/prerequisites.md.

G='\033[0;32m'; R='\033[0;31m'; Y='\033[1;33m'; B='\033[0;34m'; BD='\033[1m'; X='\033[0m'
PASS=0; FAIL=0
pass() { echo -e "  ${G}✓${X} $1"; ((PASS++)); }
fail() { echo -e "  ${R}✗${X} $1\n    ${Y}→ Fix:${X} $2"; ((FAIL++)); }
section() { echo -e "\n${BD}--- $1 ---${X}"; }

echo -e "\n${BD}${B}============================================${X}"
echo -e "${BD}${B}  Agent Native OS — Setup Verification${X}"
echo -e "${BD}${B}============================================${X}"

# 1. Claude Code CLI (installed by the Claude desktop app)
section "Claude Code CLI"
if command -v claude &>/dev/null; then
  CLAUDE_VER=$(claude --version 2>/dev/null || echo "installed")
  pass "claude --version works ($CLAUDE_VER)"
else
  fail "Claude Code CLI not found on PATH" \
    "Install the Claude desktop app from claude.ai/download. The desktop app installs the 'claude' CLI for you. After install, open a fresh terminal and re-run this script."
fi

# 2. GitHub CLI (gh) authenticated
section "GitHub CLI"
if command -v gh &>/dev/null; then
  pass "gh installed ($(gh --version 2>/dev/null | head -1))"
  if gh auth status &>/dev/null; then
    GH_USER=$(gh api user --jq .login 2>/dev/null || echo "authenticated")
    pass "gh auth status OK (user: $GH_USER)"
  else
    fail "gh is installed but not authenticated" \
      "Run: gh auth login  (choose GitHub.com, HTTPS, sign in via browser)"
  fi
else
  fail "GitHub CLI (gh) not found" \
    "Mac: brew install gh  |  Windows/WSL: sudo apt install gh  |  Or: https://cli.github.com"
fi

# 3. Workshop repo cloned
section "Workshop Repo"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/README.md" ]] && [[ -d "$SCRIPT_DIR/guides" ]] && [[ -d "$SCRIPT_DIR/setup" ]]; then
  pass "Repo looks good (README.md, guides/, setup/ all present at $SCRIPT_DIR)"
else
  fail "Couldn't verify repo structure at $SCRIPT_DIR" \
    "Make sure you cloned the full repo and you're running this script from inside it. Try: cd ~/Documents/agent-native-os && bash verify.sh"
fi

# 4. CLAUDE.md exists and has at least 3 lines of real content
section "CLAUDE.md"
CLAUDE_MD=""
if [[ -f "$HOME/.claude/CLAUDE.md" ]]; then
  CLAUDE_MD="$HOME/.claude/CLAUDE.md"
elif [[ -f "$SCRIPT_DIR/CLAUDE.md" ]]; then
  CLAUDE_MD="$SCRIPT_DIR/CLAUDE.md"
fi

if [[ -n "$CLAUDE_MD" ]]; then
  # Count non-blank, non-comment lines
  CONTENT_LINES=$(grep -cv '^[[:space:]]*\(#\|$\)' "$CLAUDE_MD" 2>/dev/null || echo 0)
  if [[ "$CONTENT_LINES" -ge 3 ]]; then
    pass "CLAUDE.md found at $CLAUDE_MD ($CONTENT_LINES content lines)"
  else
    fail "CLAUDE.md exists at $CLAUDE_MD but has fewer than 3 lines of content ($CONTENT_LINES)" \
      "Open it and fill in at least: who you are, what you do, and how you like Claude to work with you. See guides/02-claude-md.md for the template."
  fi
else
  fail "No CLAUDE.md found at ~/.claude/CLAUDE.md or in this repo" \
    "Copy the workshop template: cp $SCRIPT_DIR/templates/CLAUDE.md.template ~/.claude/CLAUDE.md  (or fill in $SCRIPT_DIR/CLAUDE.md). See guides/02-claude-md.md."
fi

# Summary
echo -e "\n${BD}${B}============================================${X}"
echo -e "${BD}  Results${X}"
echo -e "${BD}${B}============================================${X}\n"
echo -e "  ${G}Passed:${X}   $PASS"
echo -e "  ${R}Failed:${X}   $FAIL\n"

if [[ $FAIL -eq 0 ]]; then
  echo -e "${G}${BD}You're all set for the workshop. See you Sunday.${X}"
else
  echo -e "${Y}${BD}A few things need attention before workshop day.${X}"
  echo -e "Work through the fixes above and run this script again."
  echo -e "If you're stuck, post in the community Slack or check setup/mac/prerequisites.md or setup/windows/prerequisites.md."
fi
echo ""
