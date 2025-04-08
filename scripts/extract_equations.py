#!/usr/bin/env python
import re
import os

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def extract_equations_and_inputs(content, base_path, encountered_files, output_lines):
    input_pattern = re.compile(r'\\input\{(.*?)\}')
    equation_patterns = [
#        re.compile(r'(\$.*?\$)'),  # Inline equations
        re.compile(r'(\\begin\{align\}.*?\\end\{align\})', re.DOTALL),
        re.compile(r'(\\begin\{eqnarray\}.*?\\end\{eqnarray\})', re.DOTALL),
        re.compile(r'(\\begin\{equation\}.*?\\end\{equation\})', re.DOTALL),
        re.compile(r'(\\begin\{equation\*\}.*?\\end\{equation\*\})', re.DOTALL)
    ]
    
    position = 0
    while position < len(content):
        input_match = input_pattern.search(content, pos=position)
        if input_match:
            # Process content before the \input statement
            pre_content = content[position:input_match.start()]
            for pattern in equation_patterns:
                for match in pattern.findall(pre_content):
                    output_lines.append(match)

            # Process the \input statement
            input_filename = input_match.group(1)
            input_filepath = os.path.join(base_path, input_filename + '.tex')
            if os.path.exists(input_filepath) and input_filepath not in encountered_files:
                encountered_files.add(input_filepath)
                output_lines.append(f'% File: {input_filepath}')
                input_content = read_file(input_filepath)
                input_content = remove_comments(input_content)
                extract_equations_and_inputs(input_content, base_path, encountered_files, output_lines)
            
            position = input_match.end()
        else:
            # Process remaining content
            remaining_content = content[position:]
            for pattern in equation_patterns:
                for match in pattern.findall(remaining_content):
                    output_lines.append(match)
            break

def remove_comments(content):
    return '\n'.join([line for line in content.splitlines() if not line.strip().startswith('%')])

def create_master_file(main_file_path, output_file_path):
    base_path = os.path.dirname(main_file_path)
    encountered_files = set()
    output_lines = []
    
    content = read_file(main_file_path)
    output_lines.append(f'% File: {main_file_path}')
    content = remove_comments(content)
    
    extract_equations_and_inputs(content, base_path, encountered_files, output_lines)
    
    with open(output_file_path, 'w') as file:
        for line in output_lines:
            file.write(line + '\n\n')

# Example usage
if __name__ == '__main__':
    main_file_path = './ww_semiempirical_TRfmt.tex'
    output_file_path = './all_equations.tex'
    create_master_file(main_file_path, output_file_path)
