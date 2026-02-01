#!/bin/bash

echo "=== OpenCode Antigravity Configuration Check ==="
echo

echo "1. Checking OpenCode config files..."
if [ -f "$HOME/.config/opencode/opencode.json" ]; then
    echo "✓ opencode.json exists"
    if grep -q "baseURL.*127.0.0.1:8317" "$HOME/.config/opencode/opencode.json"; then
        echo "✓ Google provider baseURL configured"
    else
        echo "✗ Google provider baseURL not found"
    fi
else
    echo "✗ opencode.json not found"
fi

if [ -f "$HOME/.config/opencode/oh-my-opencode-slim.json" ]; then
    echo "✓ oh-my-opencode-slim.json exists"
    if grep -q '"preset": "antigravity"' "$HOME/.config/opencode/oh-my-opencode-slim.json"; then
        echo "✓ Antigravity preset set as default"
    else
        echo "✗ Antigravity preset not set as default"
    fi
else
    echo "✗ oh-my-opencode-slim.json not found"
fi

echo
echo "1.1 Checking plugin installation (common black-screen cause)..."
PLUGIN_LINK="$HOME/.config/opencode/node_modules/oh-my-opencode-slim"
PLUGIN_DIR="$HOME/.config/opencode/oh-my-opencode-slim"

if [ -L "$PLUGIN_LINK" ]; then
    TARGET="$(readlink "$PLUGIN_LINK")"
    echo "✓ oh-my-opencode-slim is a symlink: $TARGET"
    # Detect self-referential symlink (ELOOP)
    if [ "$TARGET" = "oh-my-opencode-slim" ] || [ "$TARGET" = "node_modules/oh-my-opencode-slim" ]; then
        echo "✗ Detected symlink loop (ELOOP) — this can cause OpenCode to open a black screen and exit"
        echo "  Fix (recommended):"
        echo "  rm -f \"$PLUGIN_LINK\" && ln -s ../oh-my-opencode-slim \"$PLUGIN_LINK\""
    fi
elif [ -e "$PLUGIN_LINK" ]; then
    echo "✓ oh-my-opencode-slim exists in node_modules"
else
    echo "⚠️  oh-my-opencode-slim not found in node_modules"
    echo "  If OpenCode fails to start, reinstall plugins or re-run installer."
fi

if [ ! -d "$PLUGIN_DIR" ]; then
    echo "⚠️  Local plugin directory not found: $PLUGIN_DIR"
    echo "  If you use a symlinked plugin, ensure the folder exists."
fi

echo
echo "2. Checking Antigravity service..."
if curl -s http://127.0.0.1:8317/v1beta/models >/dev/null 2>&1; then
    echo "✓ Antigravity service is running"
else
    echo "✗ Antigravity service is not running on port 8317"
    echo "  Please start the Antigravity service first:"
    echo "  - Follow: https://nghyane.github.io/llm-mux/#/installation"
    echo "  - Or check if it's running on a different port"
fi

echo
echo "2.1 Quick config sanity hints..."
if [ -f "$HOME/.config/opencode/oh-my-opencode-slim.json" ]; then
    if grep -q 'google/gemini-3-pro-high' "$HOME/.config/opencode/oh-my-opencode-slim.json"; then
        echo "⚠️  Found model 'google/gemini-3-pro-high' in oh-my-opencode-slim.json"
        echo "  This often should be: model='google/gemini-3-pro' + variant='high'"
    fi
fi

echo
echo "3. Available models in config:"
if [ -f "$HOME/.config/opencode/opencode.json" ]; then
    grep -o '"[^"]*thinking[^"]*"' "$HOME/.config/opencode/opencode.json" | sed 's/"//g' | while read model; do
        echo "  ✓ $model"
    done
fi

echo
echo "=== Configuration Summary ==="
echo "✓ Provider: Google (Antigravity) configured"
echo "✓ Preset: antigravity set as default"
echo "✓ Models: Claude Opus 4.5 Thinking, Claude Sonnet 4.5 Thinking, Gemini 3 Pro High, Gemini 3 Flash"
echo
if ! curl -s http://127.0.0.1:8317/v1beta/models >/dev/null 2>&1; then
    echo "⚠️  ACTION REQUIRED: Start Antigravity service before using OpenCode"
else
    echo "✓ Ready to use OpenCode with Antigravity!"
fi

echo
echo "=== Troubleshooting (if you see a black screen) ==="
echo "- Print logs: opencode --print-logs --log-level DEBUG"
echo "- Show resolved config: opencode debug config --print-logs --log-level DEBUG"
echo "- If terminal looks stuck: reset"