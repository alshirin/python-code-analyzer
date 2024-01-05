import subprocess
import sys


def run_command(command):
    """Run a shell command and return its success as a boolean."""
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def format_with_black(script_name):
    """Format the script with Black."""
    return run_command(f"black {script_name}")


def lint_with_pylint(script_name):
    """Lint the script with Pylint and check if the rating is more than 5.0."""
    try:
        # Run Pylint and capture the output
        result = subprocess.run(
            f"pylint {script_name}", capture_output=True, text=True, shell=True
        )

        # Check for a successful run
        if result.returncode == 1:
            print("Error occurred while running Pylint.")
            return False

        # Parse the output for the rating
        output = result.stdout
        warnings = []
        for line in output.split("\n"):
            if line.startswith(f"{script_name}"):
                warnings.append(line)
            elif line.startswith("Your code has been rated at"):
                # Extract the rating value
                rating_str = line.split()[6]
                rating = float(rating_str.split("/")[0])
                if rating >= 8.0:
                    return True
                else:
                    print("rating_str", rating_str)
                    print("output", output)
                    print("warnings:\n")
                    for warn in warnings:
                        print(warn)
                    print("\n")

        # If the rating is not found, return False
        return False

    except subprocess.CalledProcessError:
        # Handle any error during the Pylint run
        print("Error occurred while running Pylint.")
        return False


def type_check_with_mypy(script_name):
    """Type check the script with Mypy and return True if no issues are found."""
    try:
        # Run Mypy and capture the output
        result = subprocess.run(
            ["mypy", script_name],
            capture_output=True,
            text=True,
            check=False,  # Set check to False for handling the output manually
        )

        output = result.stdout
        if "Success: no issues found" in output:
            return True  # Success case
        else:
            # Mypy found issues, print them and return False
            print("Mypy issues found:")
            print(output)
            return False

    except subprocess.CalledProcessError:
        # Handle any error during the Mypy run
        print("Error occurred while running Mypy.")
        return False


def analyze_with_radon_cc(script_name):
    """Analyze the script with Radon Complexity Check and ensure that all methods are graded 'A' or 'B'."""
    try:
        # Run Radon CC and capture the output
        result = subprocess.run(
            ["radon", "cc", "-s", script_name],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout

        # Parse the output to find method grades
        for line in output.split("\n")[1:]:
            if line.strip() and not line.startswith(" "):
                # Skip blank lines and details
                parts = line.split()
                # Ensure the line has enough parts to prevent IndexError
                if len(parts) >= 3:
                    grade = parts[2]
                    if grade not in ["A", "B"]:
                        return False  # Fail if any method is graded lower than 'B'
        return True  # Pass if all methods are graded 'A' or 'B'

    except subprocess.CalledProcessError:
        # Handle any error during the Radon run
        print("Error occurred while running Radon Complexity Check.")
        return False


def analyze_with_radon_mi(script_name):
    """Analyze the script with Radon Maintainability Index Check to ensure that the maintainability index is 'A'."""
    try:
        # Run Radon MI and capture the output
        result = subprocess.run(
            ["radon", "mi", "-s", script_name],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout
        # The maintainability index is a single grade for the whole module
        # Example line: "my_module.py - A"
        grade = output.split()[2]
        return grade == "A"

    except subprocess.CalledProcessError:
        # Handle any error during the Radon run
        print("Error occurred while running Radon Maintainability Index Check.")
        return False


def execute_script(script_name):
    """Execute the given Python script."""
    print("\n\033[1;43mScript Execution ...\033[0m\n")
    run_command(f"python {script_name}")


def main(script_name):
    """Run checks and execute the script if all checks pass."""
    checks = [
        (
            format_with_black,
            "Black formatting \033[31mFAILED\033[0m",
            "Black formatting \033[32mPASSED\033[0m",
        ),
        (
            lint_with_pylint,
            "Pylint check \033[31mFAILED\033[0m",
            "PyLint check \033[32mPASSED\033[0m",
        ),
        (
            type_check_with_mypy,
            "Mypy type checking \033[31mFAILED\033[0m",
            "Mypy type checking \033[32mPASSED\033[0m",
        ),
        (
            analyze_with_radon_cc,
            "Radon complexity analysis \033[31mFAILED\033[0m",
            "Radon complexity analysis \033[32mPASSED\033[0m",
        ),
        (
            analyze_with_radon_mi,
            "Radon Maintainability Index analysis \033[31mFAILED\033[0m",
            "Radon Maintainability Index analysis \033[32mPASSED\033[0m",
        ),
    ]

    failed_checks = []
    for check, error_message, success in checks:
        if not check(script_name):
            failed_checks.append(error_message)
        else:
            print(success)

    if failed_checks:
        # print("The following checks failed:")
        print("\n\033[1;43mThe following checks failed: ...\033[0m\n")
        for error_message in failed_checks:
            print(error_message)
    else:
        execute_script(script_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <python_script_to_check_and_run>")
        sys.exit(1)

    script_to_check = sys.argv[1]
    main(script_to_check)
