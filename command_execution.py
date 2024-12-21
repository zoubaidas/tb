import subprocess


def execute_command(command: str) -> str:
    """
    Exécute une commande Bash sur la machine et retourne la sortie.
    :param command: Commande Bash à exécuter.
    :return: Sortie de la commande (stdout).
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="/home/kali"  # Répertoire de travail par défaut
        )
        if result.returncode != 0:
            print(f"Erreur lors de l'exécution de la commande: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Exception lors de l'exécution de la commande: {e}")
        return f"Erreur: {e}"
