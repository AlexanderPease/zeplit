import os
import re
import ast

IGNORE_DIRNAMES =[
    '.git',
    'templates',
    'static',
    '.modules'
]

class Function:
    """A single function."""
    def __init__(self, code, file_path):
        self.code = code
        self.file_path = file_path

    def __repr__(self):
        return f'{self.file_path}: {self.name}'

    @property
    def name(self):
        match = re.search(r'def\s+(\w+)', self.code)
        return match.group(1) if match else None


class FunctionExtractor(ast.NodeVisitor):
    """Extract functions from a Python source file."""
    def __init__(self):
        self.functions = []

    def visit_FunctionDef(self, node):
        """Visit a function definition, extract its source, and append it to the list."""
        start_line = node.lineno
        end_line = node.end_lineno
        self.functions.append((start_line, end_line))
        self.generic_visit(node)


def extract_function_code_from_file(file_path):
    """Extract full function code from a given file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        tree = ast.parse(''.join(lines))
        
        extractor = FunctionExtractor()
        extractor.visit(tree)

        function_codes = []
        for start, end in extractor.functions:
            function = Function(code=''.join(lines[start-1:end]), file_path=file_path)
            function_codes.append(function)

        return function_codes


def analyze_repo(repo_path):
    """Walk through a local git repo and extract function names."""
    all_functions = []

    for dirpath, dirnames, filenames in os.walk(repo_path):
        
        # Skip certain directories
        for ignore_dirname in IGNORE_DIRNAMES:
            if ignore_dirname in dirnames:
                dirnames.remove(ignore_dirname)  # os.walk allows for modifying var in situ
        
        for filename in filenames:
            if filename.endswith('.py'):  # Only grep .py files
                full_path = os.path.join(dirpath, filename)
                all_functions.extend(extract_function_code_from_file(full_path))

    return all_functions


if __name__ == "__main__":
    repo_path = "../sentient"
    functions = analyze_repo(repo_path)
    print(functions)








# def extract_function_names_from_file(file_path):
#     """Extract function names from a given file."""
#     function_pattern = re.compile(r'def (\w+)\(')
#     with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
#         content = file.read()
#         return function_pattern.findall(content)

