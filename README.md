# Python Code Analysis Script

This Python script provides an automated way to format and analyze Python code using several popular tools: Black, Pylint, Mypy, and Radon. It checks for code formatting, linting, type correctness, and code quality metrics.

## Features

- **Black**: Ensures your code follows standard Python formatting guidelines.
- **Pylint**: Analyzes code for potential errors and enforces a coding standard.
- **Mypy**: Checks for type correctness in your Python code.
- **Radon**: Offers Cyclomatic Complexity, Maintainability Index, and Raw Metrics analysis.

## Prerequisites

Before running the script, ensure you have the following tools installed:
- Python 3.10 or higher
- Black
- Pylint
- Mypy
- Radon

You can install these dependencies via pip:

```bash
pip install black pylint mypy radon
```

Usage
To use the script, simply pass the path of the Python file you want to analyze as an argument:

```bash
python script_name.py <path_to_python_file>
```

For example:
    
```bash
python script_name.py my_python_script.py
```

The script will run the selected analysis tools on the specified Python file and display the results. It will also attempt to execute the script if all checks pass.

## Output
The script provides detailed output for each tool:

Whether the code meets the Black formatting standards.
Pylint's rating of the code and any warnings or errors found.
Mypy's type check results.
Radon's code complexity, maintainability index, and raw metrics.

## License
This project is free to use and modify for non-commercial purposes.