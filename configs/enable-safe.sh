#!/bin/bash
# Enable Safe Mode (Level 1: Director's Cut)
# Removes YOLO permissions, Claude asks for everything

set -e

SETTINGS_DST="$HOME/.claude/settings.json"

echo "=== Safe Mode (Level 1: Director's Cut) ==="
echo ""

if [ ! -f "$SETTINGS_DST" ]; then
    echo "No settings file found. You're already in safe mode!"
    exit 0
fi

# Backup existing settings
BACKUP="$SETTINGS_DST.backup.$(date +%Y%m%d_%H%M%S)"
cp "$SETTINGS_DST" "$BACKUP"
echo "Backed up settings to: $BACKUP"

# Remove permissions.allow but keep other settings (env, etc)
python3 -c "
import json, sys
settings = json.load(open('$SETTINGS_DST'))
if 'permissions' in settings:
    settings['permissions'].pop('allow', None)
    if not settings['permissions']:
        del settings['permissions']
json.dump(settings, sys.stdout, indent=2)
" > "${SETTINGS_DST}.tmp" && mv "${SETTINGS_DST}.tmp" "$SETTINGS_DST"

echo ""
echo "Safe mode ENABLED (Level 1: Director's Cut)"
echo ""
echo "Claude will now ask permission for every action."
echo "This is the safest way to work. Perfect for learning."
echo ""
echo "To re-enable YOLO mode: ./configs/enable-yolo.sh"
echo "Or use the /yolo slash command in Claude Code"
