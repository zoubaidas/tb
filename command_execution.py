import os
import subprocess


def execute_command(command):
    """
    Exécute une commande système.
    Si la commande est interactive, elle est exécutée directement dans le terminal.

    Args:
        command (str): La commande à exécuter.

    Returns:
        str: La sortie standard ou d'erreur si la commande n'est pas interactive.
    """

    # Essaye d'exécuter la commande de manière non interactive
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


    stdout, stderr = process.communicate()
    if process.returncode == 0:
        return stdout.strip()
    else:
        return stderr.strip()



# Exemple d'utilisation
if __name__ == "__main__":
    cmd = input("Entrez une commande : ")
    result = execute_command(cmd)
    print(result)
