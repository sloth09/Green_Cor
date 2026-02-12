#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix currency $ signs in paper markdown for pandoc compatibility."""

import re
from pathlib import Path

paper_path = Path("D:/code/Green_Cor/docs/paper/v3/paper_final.md")
content = paper_path.read_text(encoding="utf-8")

# Targeted replacements for currency $ that pandoc misinterprets as math
# Pattern: $ followed by digit, NOT inside LaTeX math $...$
# We handle this by processing line by line

lines = content.split("\n")
fixed_lines = []
total_fixes = 0

for line in lines:
    # Skip lines that are display math ($$...$$)
    if line.strip().startswith("$$"):
        fixed_lines.append(line)
        continue

    # Find all $ positions in the line
    new_line = ""
    i = 0
    while i < len(line):
        if line[i] == "$":
            # Check if this is already escaped
            if i > 0 and line[i-1] == "\\":
                new_line += line[i]
                i += 1
                continue

            # Check if this is $$ (display math)
            if i + 1 < len(line) and line[i+1] == "$":
                new_line += line[i]
                i += 1
                continue

            # Check what follows the $
            rest = line[i+1:]

            # Currency pattern: $ followed by digit or negative number
            # e.g., $410.34M, $1.74/ton, $300, $-8.7 (but not $-8.7\% which is LaTeX)
            if rest and rest[0].isdigit():
                # Check if this could be LaTeX math (has matching close $ with LaTeX content)
                # Look for closing $ within 20 chars
                close_idx = rest.find("$")
                if close_idx > 0 and close_idx < 20:
                    between = rest[:close_idx]
                    # If content between $...$ has LaTeX indicators, it's math
                    if any(c in between for c in ["\\", "^", "_", "{"]):
                        new_line += line[i]
                        i += 1
                        continue

                # This is a currency $, escape it
                new_line += "\\$"
                total_fixes += 1
                i += 1
                continue

            # Check for $- pattern (could be currency like $-8.7 or LaTeX like $-8.7\%$)
            if rest and rest[0] == "-" and len(rest) > 1 and rest[1].isdigit():
                # Look for closing $ with LaTeX content
                close_idx = rest.find("$")
                if close_idx > 0 and close_idx < 30:
                    between = rest[:close_idx]
                    if any(c in between for c in ["\\", "^", "_", "{"]):
                        # This is LaTeX math like $-8.7\%$
                        new_line += line[i]
                        i += 1
                        continue

                # Currency negative amount
                new_line += "\\$"
                total_fixes += 1
                i += 1
                continue

            # Otherwise, assume it's LaTeX math
            new_line += line[i]
            i += 1
        else:
            new_line += line[i]
            i += 1

    fixed_lines.append(new_line)

result = "\n".join(fixed_lines)
paper_path.write_text(result, encoding="utf-8")
print(f"[OK] Fixed {total_fixes} currency $ signs")

# Verify
verify_content = paper_path.read_text(encoding="utf-8")
escaped = len(re.findall(r"\\\$\d", verify_content))
unescaped = len(re.findall(r"(?<!\\)\$\d", verify_content))
print(f"  Escaped currency $: {escaped}")
print(f"  Unescaped $ before digit: {unescaped}")
