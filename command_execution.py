import subprocess
import os
import time
import shlex

def is_interactive(command):
    """
    Détecte si une commande est interactive en observant son comportement.
    """
    try:
        cmd_parts = shlex.split(command)

        # Lancer la commande pour tester son comportement
        process = subprocess.Popen(
            cmd_parts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        time.sleep(1)  # Attendre brièvement

        if process.poll() is None:  # Si le processus est encore actif
            process.terminate()  # Arrêter proprement
            return True

        # Vérifier le contenu de stderr pour des indices interactifs
        stderr_output = process.stderr.read().decode()
        stdout_output = process.stdout.read().decode()
        if any(keyword in stderr_output.lower() for keyword in ["input", "interactive", "tty"]):
            return True
        if not stdout_output.strip() and process.returncode is None:
            return True

        return False
    except Exception as e:
        print(f"Erreur lors de la détection interactive : {e}")
        return False

def execute_command(command):
    """
    Exécute une commande interactive dans un terminal externe et capture sa sortie.
    """
    if is_interactive(command):
        print(f"Commande interactive détectée : {command}")
        try:
            log_file = "/tmp/terminal_output.log"
            subprocess.run(f"x-terminal-emulator -e 'bash -c \"{command} | tee {log_file}; exec bash\"'", shell=True)
            with open(log_file, 'r') as f:
                output = f.read()
            os.remove(log_file)  # Nettoyer le fichier temporaire
            return output, None
        except FileNotFoundError:
            error_msg = "Erreur : Aucun terminal graphique détecté. Veuillez installer un émulateur de terminal."
            print(error_msg)
            return None, error_msg
    else:
        print(f"Commande simple détectée : {command}")
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return None, e.stderr
