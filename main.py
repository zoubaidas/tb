import os
from tasktree import TaskTreeChain
from command_execution import execute_command, format_output

import threading
import time
import sys

# Declare `stop_loading` as a global variable
stop_loading = False

def loading_animation(text: str = "Loading..."):
    """
    Displays a loading animation in the terminal.
    """
    animation = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_loading:  # Stops the animation when stop_loading is True
        sys.stdout.write(f"\r{text} {animation[idx % len(animation)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)  # Speed of the animation


def main():
    """
    Example usage of the TaskTreeChain:
    1. Retrieve the first version of the task tree.
    2. Execute the returned command.
    3. Update the task tree with the command's output.
    4. Loop until there are no more commands to execute.
    """

    # Initialisation de la classe
    task_tree_chain = TaskTreeChain("10.10.10.245")

    # Affiche l'arbre initial
    # Display the initial tree
    print(task_tree_chain.get_current_task_tree(), "\n")

    # List to store commands and their outputs
    command_outputs = []

    command_number = 0
    while True:
        # Fetch the next command
        next_command = task_tree_chain.get_next_command()
        if not next_command:
            print("No more commands to execute.")
            break

        # Use the global variable `stop_loading`
        global stop_loading
        stop_loading = False

        # Start the animation in a separate thread
        loading_thread = threading.Thread(target=loading_animation, args=("Executing command...",))
        loading_thread.start()

        try:
            # Execute the command on a Linux machine, then retrieve the output.
            output = execute_command(next_command)
        finally:
            # Stop the animation
            stop_loading = True
            loading_thread.join()  # Attendre que le thread se termine proprement

        print(f"Command output:\n")
        format_output(output)

        # Add the command and its output to the list
        command_outputs.append({
            "command": next_command,
            "output": output
        })

        # Update the task tree with the output
        updated_tree = task_tree_chain.update_task_tree_with_output(output)

        # Display the updated task tree
        print("=== Updated Task Tree ===")
        print(updated_tree, "\n")

        command_number += 1
        if command_number > 10:  # Stop after 10 commands to avoid an infinite loop
            break

    # Write the report to a file
    with open("/home/kali/rapport_pentest.txt", "w") as report_file:
        report_file.write("=== Final Task Tree ===\n")
        report_file.write(updated_tree + "\n\n")
        report_file.write("=== Commandes et leurs sorties ===\n")
        for entry in command_outputs:
            report_file.write(f"Commande: {entry['command']}\n")
            report_file.write(f"Sortie:\n{entry['output']}\n")
            report_file.write("=" * 50 + "\n")

if __name__ == "__main__":
    main()