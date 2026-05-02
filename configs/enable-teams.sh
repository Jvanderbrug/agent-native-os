#!/bin/bash
# Enable Claude Code Agent Teams feature
# Adds the experimental teams env var to your settings.json

set -e

SETTINGS="$HOME/.claude/settings.json"

echo "=== Agent Teams Setup ==="
echo ""

# Create settings dir if needed
mkdir -p "$HOME/.claude"

if [ ! -f "$SETTINGS" ]; then
    # No settings file yet, create one
    echo '{"env":{"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS":"1"}}' | python3 -m json.tool > "$SETTINGS"
    echo "Created $SETTINGS with teams enabled."
else
    # Settings exist, add/update the env var
    python3 -c "
import json
with open('$SETTINGS') as f:
    settings = json.load(f)
if 'env' not in settings:
    settings['env'] = {}
settings['env']['CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS'] = '1'
with open('$SETTINGS', 'w') as f:
    json.dump(settings, f, indent=2)
print('Updated $SETTINGS with teams enabled.')
print('Preserved all existing settings.')
"
fi

echo ""
echo "Agent Teams: ENABLED"
echo ""
echo "Restart Claude Code for the change to take effect."
echo "Then try: 'Launch 2 agents to research X and Y in parallel'"
