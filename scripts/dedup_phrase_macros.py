#!/usr/bin/env python
import re

# Input and output file paths
input_file = 'phrase_macros.tex'
output_file = 'dedup_phrase_macros.tex'

# Dictionary to store unique macros
unique_macros = {}

# Read the input file and collect unique macros
with open(input_file, 'r') as file:
    for line in file:
        # Match lines that define a macro
        match = re.match(r'\\newcommand\{\\(\w+)\}\{(.+?)\}', line)
        if match:
            macro_name = match.group(1)  # Macro name without the leading backslash
            macro_definition = match.group(2)  # Definition inside the braces
            
            # Store the first occurrence of each macro
            if macro_name not in unique_macros:
                unique_macros[macro_name] = macro_definition

# Write the deduplicated macros to the output file
with open(output_file, 'w') as file:
    for macro_name, macro_definition in unique_macros.items():
        file.write(f"\\providecommand{{\\{macro_name}}}{{{macro_definition}}}\n")

print(f"Deduplicated macros written to {output_file}")
