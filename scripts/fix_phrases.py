#!/usr/bin/env python
import os
import re
import shutil

# Set the detection flag
detect_only = False  # Set to True to only detect, False to replace

# Function to load macros from phrase_macros.tex
def load_macros(filename):
    macros = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.replace("\\xspace", "")
            # Match lines that define a macro
            match = re.match(r'\\newcommand\{\\(\w+)\}\{(.+?)\}', line)
            if match:
                macro_name = match.group(1)  # Macro name without the leading backslash
                phrase = match.group(2)      # Phrase in the macro definition
                macros[phrase] = f'\\{macro_name}'  # Map phrase to macro with backslash
    return macros

# Load macros from phrase_macros.tex into a dictionary
macros_file = 'phrase_macros.tex'  # Path to your macros file
phrases_to_macros = load_macros(macros_file)

# Directory for backups
backup_dir = './baks'
os.makedirs(backup_dir, exist_ok=True)

# Define regex patterns to check for emphasis types
emphasis_patterns = [
    r'"(.*?)"',                 # Double quotes
    r"'(.*?)'",                 # Single quotes
    r"\\emph{(.*?)}",           # \emph{}
    r"\\textit{(.*?)}",         # \textit{}
    r"\\textbf{(.*?)}",         # \textbf{}
    r"\\bf{(.*?)}",             # \bf{}
]

# Function to identify headings, captions, etc.
def is_heading_or_special(line):
    heading_keywords = [r'\\section', r'\\subsection', r'\\subsubsection', 
                        r'\\paragraph', r'\\item', r'\\caption', r'\\begin\{equation\}', r'\\begin\{align\}']
    return any(re.search(keyword, line) for keyword in heading_keywords)

# Loop over the specified files and perform replacements or detections
for filename in os.listdir('.'):
    # Uncomment the line below and comment out the line after if you want to match specific files in the directory.
    if re.match(r'^[1-6A].*\.tex$', filename):
    #if filename == 'test_file.tex':  # Modify this line for your specific test file
        # Make a backup if not in detection mode
        print(filename)
        
        if not detect_only:
            shutil.copy(filename, os.path.join(backup_dir, filename))

        # Read file content
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Prepare a list to store detections if in detect_only mode
        detections = []

        # Replace or detect emphasized phrases in text paragraphs
        updated_lines = []
        for line_num, line in enumerate(lines, 1):
            original_line = line
            # Cleanup step to replace two or more consecutive backslashes followed by a capital letter with a single backslash
            line = re.sub(r'\\{2,}([A-Z])', r'\\\1', line)

            # Skip lines with headings, captions, or equations
            if is_heading_or_special(line):
                updated_lines.append(line)
                continue

            # Process each phrase with emphasis detection or replacement
            for phrase, macro in phrases_to_macros.items():
                for pattern in emphasis_patterns:
                    # Detect or replace emphasized versions of the phrase
                    if re.search(pattern.replace("(.*?)", re.escape(phrase)), line):
                        if detect_only:
                            detections.append(f"Detected '{phrase}' (macro: {macro}) on line {line_num} in {filename}")
                        else:
                            line = re.sub(pattern.replace("(.*?)", re.escape(phrase)), re.escape(macro), line)
                # Detect or replace plain text occurrences of the phrase
                if re.search(rf"\b{re.escape(phrase)}\b", line):
                    if detect_only:
                        detections.append(f"Detected '{phrase}' (macro: {macro}) on line {line_num} in {filename}")
                    else:
                        line = re.sub(rf"\b{re.escape(phrase)}\b", re.escape(macro), line)

            # Remove any remaining stray quotes if not in detect mode
            if not detect_only:
                line = re.sub(r'["\']', '', line)
                line = re.sub(r'\\{2,}([A-Z])', r'\\\1', line)
            updated_lines.append(line)



        # Write updated content back to file or output detections
        if detect_only:
            print(f"Detections in {filename}:")
            for detection in detections:
                print(detection)
        else:
            with open(filename, 'w') as file:
                file.writelines(updated_lines)
