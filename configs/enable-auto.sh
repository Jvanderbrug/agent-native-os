#!/bin/bash
# Enable Auto Mode (Level 2: Trusted Crew)
# Auto mode supersedes the older YOLO scripts. Claude auto-accepts file
# edits and most low-risk commands, but still gates destructive operations.
# Requires Time Machine to be active as a safety net.

set -e

SETTINGS_DST="$HOME/.claude/settings.json"

echo "=== Auto Mode Setup (Level 2: Trusted Crew) ==="
echo ""

# Hard gate: Time Machine must be configured. No backup, no auto mode.
TM_DEST=$(tmutil destinationinfo 2>/dev/null | grep "Name" || echo "")

if [ -z "$TM_DEST" ]; then
    echo "WARNING: Time Machine is not configured!"
    echo ""
    echo "Tyler's rule: No Time Machine, no Auto mode. Period."
    echo ""
    echo "To set up Time Machine:"
    echo "  1. Open System Settings > General > Time Machine"
    echo "  2. Add a backup destination (external drive or NAS)"
    echo "  3. Run a backup"
    echo "  4. Come back and run this script again"
    echo ""
    exit 1
fi

echo "Time Machine: VERIFIED"
echo "  Destination: $TM_DEST"
echo ""

# Backup existing settings
mkdir -p "$(dirname "$SETTINGS_DST")"
if [ -f "$SETTINGS_DST" ]; then
    BACKUP="$SETTINGS_DST.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$SETTINGS_DST" "$BACKUP"
    echo "Backed up existing settings to: $BACKUP"
fi

# Patch settings.json to set permissions.defaultMode = "acceptEdits"
# (the "auto mode" — auto-accept file edits, still gate destructive commands).
# Preserves any other settings (env, MCP configs, existing allow lists).
if [ -f "$SETTINGS_DST" ]; then
    python3 -c "
import json
with open('$SETTINGS_DST') as f:
    settings = json.load(f)
if 'permissions' not in settings:
    settings['permissions'] = {}
settings['permissions']['defaultMode'] = 'acceptEdits'
with open('$SETTINGS_DST', 'w') as f:
    json.dump(settings, f, indent=2)
"
else
    echo '{"permissions":{"defaultMode":"acceptEdits"}}' | python3 -m json.tool > "$SETTINGS_DST"
fi

echo ""
echo "Auto mode ENABLED (Level 2: Trusted Crew)"
echo ""
echo "What changes:"
echo "  - Claude auto-accepts file edits without prompting"
echo "  - Most low-risk shell commands run without prompting"
echo "  - Destructive commands (rm, sudo, git push) still require approval"
echo ""
echo "To go back to safe mode: ./configs/enable-safe.sh"
echo "Or use the /safe slash command in Claude Code"
