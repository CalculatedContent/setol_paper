#!/usr/bin/env python
import os
import re
import shutil

# Set detection mode to true, so we only print findings without making changes
detect_only = False

# Load macros from phrase_macros.tex
def load_macros(filename):
    macros = []
    with open(filename, 'r') as file:
        for line in file:
            # Match lines that define a macro
            match = re.match(r'\\newcommand\{\\(\w+)\}\{.+?\}', line)
            if match:
                macro_name = match.group(1)  # Macro name without the leading backslash
                macros.append(f'\\{macro_name}')  # Store macro with backslash
    return macros

# Load macros into a list
macros_file = 'phrase_macros.tex'  # Path to your macros file
macros = load_macros(macros_file)

# TEST
# macros = macros[0:1]

# Directory for backups (only used if detect_only = False)
backup_dir = './baks'
os.makedirs(backup_dir, exist_ok=True)

# Function to identify headings, captions, etc.
def is_heading_or_special(line):
    heading_keywords = [r'\\section', r'\\subsection', r'\\subsubsection', 
                        r'\\paragraph', r'\\item', r'\\caption', r'\\begin\{equation\}', r'\\begin\{align\}']
    return any(re.search(keyword, line) for keyword in heading_keywords)

# Custom sorting function for files
def custom_sort_key(filename):
    match = re.match(r'(\d+|A)(\d*)', filename)
    if match:
        if match.group(1) == 'A':
            # Sort 'A' files by suffix in ascending order after numbered files
            return (1, int(match.group(2) or 0))
        else:
            # Sort numbered files in ascending order
            return (0, int(match.group(1)))
    return (2, 0)  # Catch-all to place any unmatched files at the end

# Sort files using the custom sort key
def sorted_tex_files():
    files = [f for f in os.listdir('.') if re.match(r'^[1-6A].*\.tex$', f)]
    return sorted(files, key=custom_sort_key)

# Dictionary to track if a macro has been found already across all files
isMacroFound = {macro: False for macro in macros}

# Loop over files in custom sorted order and apply changes
for filename in sorted_tex_files():
    # Read file content
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Process each line
    updated_lines = []
    for line_num, line in enumerate(lines, 1):
        # Skip lines with headings, captions, or equations
        if line.strip().startswith('%') or is_heading_or_special(line):
            updated_lines.append(line)
            continue

        # Check each macro and add \emph{} to the first occurrence across all files
        for macro in macros:
            if not isMacroFound[macro]:
                # Search for the macro in the line
                if re.search(rf'(?<!\\)({re.escape(macro)})\b', line):
                    if detect_only:
                        # Print detection message
                        print(f"First instance of '{macro}' found in {filename} on line {line_num}")
                    else:
                        # Add emphasis to the first instance
                        line = re.sub(rf'(?<!\\)({re.escape(macro)})\b', r'\\emph{\1}', line, count=1)
                        print(f"Added emphasis to '{macro}' in {filename} on line {line_num}")
                    isMacroFound[macro] = True  # Mark as found

        updated_lines.append(line)

                    
    # Write updated content back to file if detect_only is False
    if not detect_only:
        with open(filename, 'w') as file:
            file.writelines(updated_lines)
