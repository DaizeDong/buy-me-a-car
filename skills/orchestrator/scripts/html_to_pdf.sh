#!/bin/bash
# Convert HTML dossier to PDF using Chrome headless.
#
# Usage:
#   bash html_to_pdf.sh input.html output.pdf
#
# Requires Chrome or Edge installed. Tries Chrome first, falls back to Edge.

set -e

INPUT="$1"
OUTPUT="$2"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <input.html> <output.pdf>"
    exit 1
fi

# Convert path for Chrome on Windows / WSL / Git Bash
ABS_INPUT=$(realpath "$INPUT" 2>/dev/null || readlink -f "$INPUT" 2>/dev/null || echo "$INPUT")
ABS_OUTPUT=$(realpath -m "$OUTPUT" 2>/dev/null || echo "$OUTPUT")

# Convert Unix path to Windows path if running on Git Bash / WSL
FILE_URL="file://$ABS_INPUT"
if [[ "$ABS_INPUT" == /c/* ]]; then
    WIN_PATH=$(echo "$ABS_INPUT" | sed 's|^/c/|C:/|' | sed 's|/|\\|g')
    FILE_URL="file:///$(echo $WIN_PATH | sed 's|\\|/|g')"
fi

# Find Chrome or Edge
if [ -x "/c/Program Files/Google/Chrome/Application/chrome.exe" ]; then
    BROWSER="/c/Program Files/Google/Chrome/Application/chrome.exe"
elif [ -x "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" ]; then
    BROWSER="/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
elif [ -x "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" ]; then
    BROWSER="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
elif command -v google-chrome >/dev/null; then
    BROWSER="google-chrome"
elif command -v chromium >/dev/null; then
    BROWSER="chromium"
else
    echo "Error: Chrome or Edge not found"
    exit 2
fi

echo "Using browser: $BROWSER"
echo "Input: $FILE_URL"
echo "Output: $ABS_OUTPUT"

"$BROWSER" --headless=new --disable-gpu --no-margins=0 --print-to-pdf-no-header \
    --print-to-pdf="$ABS_OUTPUT" "$FILE_URL"

if [ -f "$ABS_OUTPUT" ]; then
    SIZE=$(stat -c%s "$ABS_OUTPUT" 2>/dev/null || stat -f%z "$ABS_OUTPUT")
    echo "Done. ${SIZE} bytes written to $ABS_OUTPUT"
else
    echo "Error: PDF output not created"
    exit 3
fi
