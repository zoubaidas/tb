import subprocess
import os
import time
import shlex


def is_interactive(command):
    """
    Detects if a command is interactive or not by observing its behavior.

    Args:
        command (str): The command to test.

    Returns:
        bool: True if the command is interactive, False otherwise.
    """
    try:
        cmd_parts = shlex.split(command)

        # Launch the command to test its behavior
        process = subprocess.Popen(
            cmd_parts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        time.sleep(1)  # Wait a moment to observe the behavior

        if process.poll() is None:  # Process still active
            process.terminate()
            return True

        # Check the content of stderr or stdout to detect interactivity
        stderr_output = process.stderr.read().decode()
        stdout_output = process.stdout.read().decode()
        if any(keyword in stderr_output.lower() for keyword in ["input", "interactive", "tty"]):
            return True
        if not stdout_output.strip() and process.returncode is None:
            return True

        return False
    except Exception as e:
        print(f"Error during interactivity detection: {e}")
        return False


def execute_command(command):
    """
    Executes a command by detecting if it is interactive, while providing formatted output.

    Args:
        command (str): The command to execute.

    Returns:
        dict: Dictionary containing `stdout`, `stderr`, and `status`.
    """
    if is_interactive(command):
        print(f"[INFO] Interactive command detected: {command}")
        try:
            log_file = "/tmp/terminal_output.log"  # Temporary file to store the output
            # Launch the command in an external terminal
            subprocess.run(
                f"x-terminal-emulator -e 'bash -c \"{command} | tee {log_file}; exec bash\"'",
                shell=True
            )

            # Read the content of the temporary file if the command generated output
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    output = f.read()
                os.remove(log_file)  # Clean up the log file after use
                return {"stdout": output.strip(), "stderr": None, "status": "Success"}
            else:
                return {"stdout": None, "stderr": "No output captured from the terminal.", "status": "Error"}
        except FileNotFoundError:
            error_msg = "[ERROR] No graphical terminal detected. Please install a terminal emulator."
            print(error_msg)
            return {"stdout": None, "stderr": error_msg, "status": "Error"}
    else:
        print(f"[INFO] Simple command detected: {command}")
        try:
            # Exécuter une commande simple avec subprocess
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=True
            )
            return {
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "status": "Success"
            }
        except subprocess.CalledProcessError as e:
            return {
                "stdout": None,
                "stderr": e.stderr.strip(),
                "status": "Error"
            }


def format_output(result):
    """
    Formats and displays the results of a command in a readable manner.

    Args:
        result (dict): The dictionary returned by `execute_command`.
    """
    print("\n" + "=" * 50)
    print("[COMMAND RESULTS]")
    print("=" * 50)

    if result["status"] == "Success":
        print("[STATUS]: ✅ Command successful")
    else:
        print("[STATUS]: ❌ Error during execution")

    print("\n[STDOUT]:")
    if result["stdout"]:
        print(result["stdout"])
    else:
        print("No standard output.")

    print("\n[STDERR]:")
    if result["stderr"]:
        print(result["stderr"])
    else:
        print("No errors detected.")

    print("=" * 50)
