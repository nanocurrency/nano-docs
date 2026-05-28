#!/usr/bin/env python3
"""
Markdown Spacing Formatter

This script formats Markdown files to insert standard empty lines between distinct 
block-level elements (headings, code blocks, lists, and tables).

Ensuring clean spacing around these blocks prevents layout and rendering issues on 
standard Markdown parsers (like GitHub's file preview and other repository viewers) 
while maintaining 100% compatibility with MkDocs.

Usage:
    python scripts/format_markdown.py
"""

import os
import re

# Resolve the absolute path to the docs directory relative to the repository root
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
docs_dir = os.path.join(repo_root, "docs")

heading_re = re.compile(r"^#{1,6}\s+")
code_block_re = re.compile(r"^```")
list_re = re.compile(r"^(\s*[-*+]\s|\s*\d+\.\s)")

def format_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    had_final_newline = content.endswith("\n")
    lines = content.splitlines()
    output = []
    
    def add_line(l):
        # Prevent consecutive empty lines
        if not l.strip():
            if not output or not output[-1].strip():
                return
        output.append(l)

    in_code_block = False
    idx = 0
    num_lines = len(lines)
    
    while idx < num_lines:
        line = lines[idx]
        stripped = line.strip()
        
        # Code block boundaries
        if code_block_re.match(stripped):
            in_code_block = not in_code_block
            
            if in_code_block: # Starting code block
                if idx > 0:
                    prev_line = lines[idx - 1].strip()
                    if prev_line and not code_block_re.match(prev_line) and not prev_line.startswith(">"):
                        add_line("")
                add_line(line)
            else: # Ending code block
                add_line(line)
                if idx < num_lines - 1:
                    next_line = lines[idx + 1].strip()
                    if next_line and not code_block_re.match(next_line) and not next_line.startswith(">"):
                        add_line("")
            idx += 1
            continue
            
        if in_code_block:
            output.append(line)
            idx += 1
            continue
            
        # Heading boundaries
        if heading_re.match(line):
            if idx > 0:
                prev_line = lines[idx - 1].strip()
                if prev_line and not heading_re.match(prev_line):
                    add_line("")
            
            add_line(line)
            
            if idx < num_lines - 1:
                next_line = lines[idx + 1].strip()
                if next_line and not heading_re.match(next_line):
                    add_line("")
            idx += 1
            continue
            
        # List boundaries
        if list_re.match(line):
            if idx > 0:
                prev_line = lines[idx - 1].strip()
                if prev_line and not list_re.match(lines[idx - 1]) and not heading_re.match(prev_line) and not prev_line.startswith(">"):
                    add_line("")
            
            add_line(line)
            
            if idx < num_lines - 1:
                next_line = lines[idx + 1].strip()
                if next_line and not list_re.match(lines[idx + 1]) and not next_line.startswith(">") and not code_block_re.match(next_line):
                    orig_next_line = lines[idx + 1]
                    if orig_next_line and not orig_next_line.startswith(" ") and not orig_next_line.startswith("\t"):
                        add_line("")
            idx += 1
            continue
            
        add_line(line)
        idx += 1
        
    new_content = "\n".join(output).strip()
    if had_final_newline:
        new_content += "\n"

    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

if __name__ == "__main__":
    if not os.path.exists(docs_dir):
        print(f"Error: Could not find documentation directory at: {docs_dir}")
        exit(1)
        
    modified_count = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                if format_markdown_file(filepath):
                    print(f"Formatted: {os.path.relpath(filepath, docs_dir)}")
                    modified_count += 1

    print(f"\nDone. Formatted {modified_count} files.")
