import ast
import os


def calculate_documented_percentage(dirpath):
    # Initialize counters
    total_definitions = 0
    documented_definitions = 0

    # Iterate through all Python files in the directory
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    code = f.read()
                tree = ast.parse(code)

                # Count documented definitions
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                        if ast.get_docstring(node):
                            documented_definitions += 1
                        total_definitions += 1

    # Calculate the percentage
    if total_definitions == 0:
        return 0
    else:
        percentage = (documented_definitions / total_definitions) * 100
        return round(percentage, 1)


dirpath = '/home/kamelovn/cookiecutter/cookiecutter/'
percentage = calculate_documented_percentage(dirpath)
print(f"The percentage of documented code in {dirpath} is {percentage}%")
