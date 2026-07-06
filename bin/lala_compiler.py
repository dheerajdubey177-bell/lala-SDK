import sys
import os
import subprocess
import re

def compile_lala(source_file):
    if not source_file.endswith('.lala'):
        print("Error: File must have a .lala extension.")
        return

    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {source_file}: {e}")
        return

    cpp_lines = []
    indent_stack = [0]

    # Pre-add headers
    cpp_lines.append("#include <iostream>")
    cpp_lines.append("#include <string>")
    cpp_lines.append("#include <vector>")
    cpp_lines.append('#include "core/lala_runtime.hpp"')
    cpp_lines.append("using namespace std;\n")

    for line in lines:
        stripped_line = line.rstrip('\n')
        # preserve left indentation
        text_only = stripped_line.lstrip()
        
        if not text_only:
            continue
            
        current_indent = len(stripped_line) - len(text_only)
        
        # Handle dedent
        while current_indent < indent_stack[-1]:
            indent_stack.pop()
            cpp_lines.append(" " * indent_stack[-1] + "}")
            
        # Handle indent
        if current_indent > indent_stack[-1]:
            indent_stack.append(current_indent)
            
        is_block_start = text_only.endswith(":")
        if is_block_start:
            text_only = text_only[:-1].strip()
            
        # Program Structure
        text_only = text_only.replace("lala.start", "int main()")
        
        # I/O
        text_only = re.sub(r'^lala\.print\((.*?)\)$', r'std::cout << \1 << std::endl', text_only)
        text_only = re.sub(r'^lala\.pucho\((.*?)\)$', r'std::cin >> \1', text_only)
        
        # Variables
        text_only = re.sub(r'^lala\.number\s+(\w+)\s*=\s*(.*)', r'int \1 = \2', text_only)
        text_only = re.sub(r'^lala\.number\s+(\w+)$', r'int \1', text_only)
        text_only = re.sub(r'^lala\.text\s+(\w+)\s*=\s*(.*)', r'std::string \1 = \2', text_only)
        text_only = re.sub(r'^lala\.text\s+(\w+)$', r'std::string \1', text_only)
        text_only = re.sub(r'^lala\.decimal\s+(\w+)\s*=\s*(.*)', r'float \1 = \2', text_only)
        text_only = re.sub(r'^lala\.decimal\s+(\w+)$', r'float \1', text_only)
        text_only = re.sub(r'^lala\.flag\s+(\w+)\s*=\s*(.*)', r'bool \1 = \2', text_only)
        text_only = re.sub(r'^lala\.flag\s+(\w+)$', r'bool \1', text_only)
        
        # Conditionals
        text_only = re.sub(r'^lala\.agar\s+(.*)', r'if (\1)', text_only)
        text_only = re.sub(r'^lala\.warna_agar\s+(.*)', r'else if (\1)', text_only)
        text_only = re.sub(r'^lala\.warna$', r'else', text_only)
        
        # Loops
        text_only = re.sub(r'^lala\.jab_tak\s+(.*)', r'while (\1)', text_only)
        har_match = re.match(r'^lala\.har\s+(\w+)\s+in\s+range\((.*?)\)', text_only)
        if har_match:
            var = har_match.group(1)
            limit = har_match.group(2)
            text_only = f"for (int {var} = 0; {var} < {limit}; {var}++)"
            
        # Collections
        text_only = re.sub(r'^lala\.suchi<(.+?)>\s+(\w+)$', r'std::vector<\1> \2', text_only)
        
        # Functions
        text_only = re.sub(r'^lala\.kaam\s+(\w+)\s+(\w+)\((.*?)\)', r'\1 \2(\3)', text_only)
        text_only = re.sub(r'^lala\.lautao\s+(.*)', r'return \1', text_only)
        
        # Raylib Game Engine
        text_only = re.sub(r'^lala\.khel_loop', r'while (!WindowShouldClose())', text_only)
        text_only = text_only.replace("lala.shuru_drawing()", "BeginDrawing(); ClearBackground(RAYWHITE);")
        text_only = text_only.replace("lala.khatam_drawing()", "EndDrawing();")
        text_only = re.sub(r'^lala\.draw_circle\((.*?)\)', r'lala_runtime::draw_circle(\1)', text_only)
        text_only = re.sub(r'^lala\.draw_text\((.*?)\)', r'lala_runtime::draw_text(\1)', text_only)
        
        # Custom methods
        text_only = text_only.replace("lala.banau_window", "lala_runtime::create_window")

        out_line = " " * current_indent + text_only
        
        if is_block_start:
            out_line += " {"
        else:
            if not out_line.endswith('{') and not out_line.endswith('}') and not out_line.endswith(';'):
                out_line += ";"
                
        cpp_lines.append(out_line)

    # Dedent remaining blocks
    while len(indent_stack) > 1:
        indent_stack.pop()
        cpp_lines.append(" " * indent_stack[-1] + "}")
        
    final_cpp = "\n".join(cpp_lines) + "\n"

    # Write to a temporary C++ file
    temp_cpp_filename = "_build.cpp"
    with open(temp_cpp_filename, 'w', encoding='utf-8') as f:
        f.write(final_cpp)

    SDK_BIN_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
    GPP_PATH = os.path.join(SDK_BIN_DIR, "g++.exe")

    if not os.path.exists(GPP_PATH):
        bat_path = os.path.join(SDK_BIN_DIR, "g++.bat")
        if os.path.exists(bat_path):
            GPP_PATH = bat_path
        else:
            GPP_PATH = "g++"

    output_exe = source_file.replace('.lala', '.exe')
    print(f"Compiling {source_file} into powerful C++ binary...")
    
    SDK_ROOT = os.path.dirname(SDK_BIN_DIR)
    command = f'"{GPP_PATH}" "{temp_cpp_filename}" -I"{SDK_ROOT}" -I"{SDK_ROOT}/core/include" -L"{SDK_ROOT}/core/lib" -o "{output_exe}" -lraylib -lgdi32 -lwinmm'

    compile_status = subprocess.run(command, shell=True)

    if os.path.exists(temp_cpp_filename):
        os.remove(temp_cpp_filename)

    if compile_status.returncode == 0:
        print(f"Success! Generated: {output_exe}")
    else:
        print("Compilation failed. Check your Lala syntax.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: lala <filename.lala>")
    else:
        compile_lala(sys.argv[1])
