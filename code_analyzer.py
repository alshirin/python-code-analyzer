import subprocess
import sys


def run_command(command):
    """Run a shell command and return its success as a boolean."""
    result = subprocess.run(command, shell=True)
    return result.returncode == 0


def format_with_black(script_name):
    """Format the script with Black."""
    return run_command(f"black {script_name}")


def execute_script(script_name):
    """Execute the given Python script."""
    print("\n\033[1;43mScript Execution ...\033[0m\n")
    run_command(f"python {script_name}")
    print("\n\033[1;43mScript Execution End\033[0m\n")


def main(script_name):
    """Run checks and execute the script if all checks pass."""
    checks = [
        (
            format_with_black,
            "Black formatting \033[31mFAILED\033[0m",
            "Black formatting \033[32mPASSED\033[0m",
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
        print("\n\033[1;43mScript Execution ...\033[0m\n")
        execute_script(script_name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <python_script_to_check_and_run>")
        sys.exit(1)

    script_to_check = sys.argv[1]
    main(script_to_check)
