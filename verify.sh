#!/bin/bash

# ============================================================
# Agent Native OS — Setup Verification Script
# ============================================================
# Run this before Day 1 to confirm your machine is ready.
# Usage: bash verify.sh
#
# Windows users: Run this inside WSL2 (Ubuntu terminal).
# If you haven't set up WSL2 yet, see setup/windows/prerequisites.md
# ============================================================

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

PASS=0
FAIL=0
WARN=0

print_header() {
  echo ""
  echo -e "${BOLD}${BLUE}============================================${RESET}"
  echo -e "${BOLD}${BLUE}  Agent Native OS — Setup Verification${RESET}"
  echo -e "${BOLD}${BLUE}============================================${RESET}"
  echo ""
}

print_section() {
  echo ""
  echo -e "${BOLD}--- $1 ---${RESET}"
}

check_pass() {
  echo -e "  ${GREEN}✓${RESET} $1"
  ((PASS++))
}

check_fail() {
  echo -e "  ${RED}✗${RESET} $1"
  echo -e "    ${YELLOW}→ Fix:${RESET} $2"
  ((FAIL++))
}

check_warn() {
  echo -e "  ${YELLOW}⚠${RESET} $1"
  echo -e "    ${YELLOW}→ Note:${RESET} $2"
  ((WARN++))
}

print_header

# ============================================================
# 1. Operating System Detection
# ============================================================
print_section "System Info"

OS_TYPE=$(uname -s)
if [[ "$OS_TYPE" == "Darwin" ]]; then
  OS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
  check_pass "macOS detected (version $OS_VERSION)"
  IS_MAC=true
elif [[ "$OS_TYPE" == "Linux" ]]; then
  # Could be WSL2 on Windows
  if grep -qi microsoft /proc/version 2>/dev/null; then
    check_pass "Windows + WSL2 detected — great, this is the right place to run this script"
    IS_WINDOWS_WSL=true
  else
    check_pass "Linux detected"
  fi
  IS_MAC=false
else
  check_warn "Could not detect OS type (got: $OS_TYPE)" "This script is designed for Mac and WSL2 on Windows"
fi

# ============================================================
# 2. Node.js
# ============================================================
print_section "Node.js"

if command -v node &>/dev/null; then
  NODE_VERSION=$(node --version 2>/dev/null)
  NODE_MAJOR=$(echo "$NODE_VERSION" | sed 's/v//' | cut -d. -f1)
  if [[ "$NODE_MAJOR" -ge 18 ]]; then
    check_pass "Node.js installed ($NODE_VERSION)"
  else
    check_fail "Node.js is installed but version is too old ($NODE_VERSION — need v18 or newer)" \
      "Install the latest LTS from https://nodejs.org — or run: brew install node (Mac)"
  fi
else
  check_fail "Node.js not found" \
    "Mac: brew install node  |  Windows/WSL: sudo apt install nodejs npm  |  Or: https://nodejs.org"
fi

# ============================================================
# 3. Git
# ============================================================
print_section "Git"

if command -v git &>/dev/null; then
  GIT_VERSION=$(git --version 2>/dev/null)
  check_pass "Git installed ($GIT_VERSION)"

  # Check if git is configured
  GIT_NAME=$(git config --global user.name 2>/dev/null)
  GIT_EMAIL=$(git config --global user.email 2>/dev/null)

  if [[ -n "$GIT_NAME" && -n "$GIT_EMAIL" ]]; then
    check_pass "Git configured as: $GIT_NAME <$GIT_EMAIL>"
  else
    check_fail "Git is installed but not configured (no name/email set)" \
      "Run: git config --global user.name \"Your Name\" && git config --global user.email \"you@example.com\""
  fi
else
  check_fail "Git not found" \
    "Mac: brew install git  |  Windows/WSL: sudo apt install git  |  Or: https://git-scm.com"
fi

# ============================================================
# 4. GitHub CLI (gh)
# ============================================================
print_section "GitHub CLI"

if command -v gh &>/dev/null; then
  GH_VERSION=$(gh --version 2>/dev/null | head -1)
  check_pass "GitHub CLI installed ($GH_VERSION)"

  # Check authentication
  if gh auth status &>/dev/null 2>&1; then
    GH_USER=$(gh api user --jq .login 2>/dev/null || echo "authenticated")
    check_pass "GitHub CLI authenticated (user: $GH_USER)"
  else
    check_fail "GitHub CLI is installed but not authenticated" \
      "Run: gh auth login  (choose GitHub.com, HTTPS, and sign in via browser)"
  fi
else
  check_fail "GitHub CLI (gh) not found" \
    "Mac: brew install gh  |  Windows/WSL: sudo apt install gh  |  Or: https://cli.github.com"
fi

# ============================================================
# 5. Claude Code CLI
# ============================================================
print_section "Claude Code CLI"

if command -v claude &>/dev/null; then
  CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "installed")
  check_pass "Claude Code CLI installed ($CLAUDE_VERSION)"

  # Check if logged in (claude whoami or similar)
  # Claude Code doesn't have a simple whoami, but we can check for config
  if [[ -f "$HOME/.claude/settings.json" ]] || [[ -d "$HOME/.claude" ]]; then
    check_pass "Claude Code config directory found (~/.claude)"
  else
    check_warn "Claude Code CLI installed but no config found yet" \
      "You may need to run 'claude' once and log in. That's normal — we'll do this on Day 1."
  fi
else
  check_fail "Claude Code CLI not found" \
    "Run: npm install -g @anthropic-ai/claude-code  (requires Node.js to be installed first)"
fi

# ============================================================
# 6. 1Password CLI
# ============================================================
print_section "1Password CLI (op)"

if command -v op &>/dev/null; then
  OP_VERSION=$(op --version 2>/dev/null || echo "installed")
  check_pass "1Password CLI installed (v$OP_VERSION)"

  # Check if signed in
  if op whoami &>/dev/null 2>&1; then
    OP_USER=$(op whoami 2>/dev/null | grep -i email | awk '{print $2}' || echo "signed in")
    check_pass "1Password CLI signed in"
  else
    check_warn "1Password CLI installed but not signed in" \
      "Run: op signin  (you'll need your 1Password account credentials)"
  fi
else
  check_warn "1Password CLI (op) not installed" \
    "Optional but recommended. Mac: brew install 1password-cli  |  https://developer.1password.com/docs/cli/get-started"
fi

# ============================================================
# 7. Homebrew (Mac only)
# ============================================================
if [[ "$IS_MAC" == "true" ]]; then
  print_section "Homebrew (Mac Package Manager)"

  if command -v brew &>/dev/null; then
    BREW_VERSION=$(brew --version 2>/dev/null | head -1)
    check_pass "Homebrew installed ($BREW_VERSION)"
  else
    check_fail "Homebrew not found" \
      "Install from https://brew.sh — paste this in Terminal: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
  fi
fi

# ============================================================
# 8. Verify this repo is cloned properly
# ============================================================
print_section "Workshop Repo"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -f "$SCRIPT_DIR/CLAUDE.md" ]] && [[ -d "$SCRIPT_DIR/guides" ]]; then
  check_pass "Workshop repo looks good (found CLAUDE.md and guides/)"
else
  check_warn "Couldn't verify repo structure" \
    "Make sure you cloned the full repo and are running this script from inside it"
fi

# ============================================================
# Summary
# ============================================================
echo ""
echo -e "${BOLD}${BLUE}============================================${RESET}"
echo -e "${BOLD}  Results${RESET}"
echo -e "${BOLD}${BLUE}============================================${RESET}"
echo ""
echo -e "  ${GREEN}Passed:${RESET}   $PASS"
echo -e "  ${YELLOW}Warnings:${RESET} $WARN"
echo -e "  ${RED}Failed:${RESET}   $FAIL"
echo ""

if [[ $FAIL -eq 0 ]]; then
  echo -e "${GREEN}${BOLD}You're all set for Day 1! See you Saturday.${RESET}"
elif [[ $FAIL -le 2 ]]; then
  echo -e "${YELLOW}${BOLD}Almost there — fix the items above and run this again.${RESET}"
  echo -e "${YELLOW}If you get stuck, post in the community Slack and someone will help.${RESET}"
else
  echo -e "${RED}${BOLD}A few things need attention before Day 1.${RESET}"
  echo -e "Work through the fixes above, then run this script again."
  echo -e "If you're stuck, see setup/mac/prerequisites.md or setup/windows/prerequisites.md"
  echo -e "or post in the community Slack — we're happy to help before the weekend."
fi

echo ""
