#!/usr/bin/env python
import os
import re

# Define directory structure
SECTIONS_DIR = "sections"
APPENDIX_DIR = "appendix"
FIGURES_DIR = "figures"

# Regex patterns to match LaTeX commands
input_pattern = re.compile(r'\\input{([^}]+)}')
graphics_pattern = re.compile(r'\\includegraphics(\[.*?\])?{([^}]+)}')

def update_latex_file(filepath):
    """
    Reads a LaTeX file, updates \input{} and \includegraphics{} paths,
    and writes the changes back.
    """
    with open(filepath, "r") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        # Fix \input{} paths
        input_match = input_pattern.search(line)
        if input_match:
            input_file = input_match.group(1)
            corrected_path = None

            # Determine if the file belongs in sections/ or appendix/
            if input_file.startswith("A"):  # Appendix file
                corrected_path = f"appendix/{input_file}"
            else:  # Section file
                corrected_path = f"sections/{input_file}"

            updated_line = line.replace(input_file, corrected_path)
            updated_lines.append(updated_line)
            continue  # Skip to next line

        # Fix \includegraphics{} paths
        graphics_match = graphics_pattern.search(line)
        if graphics_match:
            image_path = graphics_match.group(2)

            # Only add 'figures/' if the path doesn't already include a directory
            if "/" not in image_path:
                corrected_path = f"figures/{image_path}"
                updated_line = line.replace(image_path, corrected_path)
                updated_lines.append(updated_line)
                continue

        updated_lines.append(line)

    # Write back the updated file
    with open(filepath, "w") as file:
        file.writelines(updated_lines)

def process_directory(directory):
    """
    Processes all .tex files in a given directory.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".tex"):
            update_latex_file(os.path.join(directory, filename))

# Run updates on sections and appendix
process_directory(SECTIONS_DIR)
process_directory(APPENDIX_DIR)

print("✅ All references to \input{} and \includegraphics{} have been updated successfully!")
