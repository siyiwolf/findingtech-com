#!/bin/bash
# HTML to PDF converter using Google Chrome headless
# Usage: ./tools/html-to-pdf.sh <input.html> <output.pdf>

set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 <input.html> <output.pdf>"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

if [ ! -f "$INPUT" ]; then
  echo "Error: Input file '$INPUT' not found"
  exit 1
fi

google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="$OUTPUT" "$INPUT" 2>/dev/null || {
  echo "PDF conversion failed. Ensure Google Chrome is installed."
  exit 1
}

echo "Generated: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
