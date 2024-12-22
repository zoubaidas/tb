import subprocess
import os
import time
import shlex


def is_interactive(command):
    """
    Détecte si une commande est interactive ou non en observant son comportement.

    Args:
        command (str): La commande à tester.

    Returns:
        bool: True si la commande est interactive, False sinon.
    """
    try:
        cmd_parts = shlex.split(command)

        # Lancer la commande pour tester son comportement
        process = subprocess.Popen(
            cmd_parts, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        time.sleep(1)  # Attendre un instant pour observer le comportement

        if process.poll() is None:  # Processus encore actif
            process.terminate()
            return True

        # Vérifier le contenu de stderr ou stdout pour détecter l'interactivité
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
    Exécute une commande en détectant si elle est interactive, tout en fournissant un output formaté.

    Args:
        command (str): La commande à exécuter.

    Returns:
        dict: Dictionnaire contenant `stdout`, `stderr`, et `status`.
    """
    if is_interactive(command):
        print(f"[INFO] Commande interactive détectée : {command}")
        try:
            log_file = "/tmp/terminal_output.log"  # Fichier temporaire pour stocker la sortie
            # Lancer la commande dans un terminal externe
            subprocess.run(
                f"x-terminal-emulator -e 'bash -c \"{command} | tee {log_file}; exec bash\"'",
                shell=True
            )

            # Lire le contenu du fichier temporaire si la commande a généré une sortie
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    output = f.read()
                os.remove(log_file)  # Nettoyer le fichier log après utilisation
                return {"stdout": output.strip(), "stderr": None, "status": "Success"}
            else:
                return {"stdout": None, "stderr": "Aucune sortie capturée depuis le terminal.", "status": "Error"}
        except FileNotFoundError:
            error_msg = "[ERREUR] Aucun terminal graphique détecté. Veuillez installer un émulateur de terminal."
            print(error_msg)
            return {"stdout": None, "stderr": error_msg, "status": "Error"}
    else:
        print(f"[INFO] Commande simple détectée : {command}")
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
            f
            return {
                "stdout": None,
                "stderr": e.stderr.strip(),
                "status": "Error"
            }


def format_output(result):
    """
    Formate et affiche les résultats d'une commande de manière lisible.

    Args:
        result (dict): Le dictionnaire retourné par `execute_command`.
    """
    print("\n" + "=" * 50)
    print("[RESULTATS DE LA COMMANDE]")
    print("=" * 50)

    if result["status"] == "Success":
        print("[STATUT]: ✅ Commande réussie")
    else:
        print("[STATUT]: ❌ Erreur lors de l'exécution")

    print("\n[STDOUT]:")
    if result["stdout"]:
        print(result["stdout"])
    else:
        print("Aucune sortie standard.")

    print("\n[STDERR]:")
    if result["stderr"]:
        print(result["stderr"])
    else:
        print("Aucune erreur détectée.")

    print("=" * 50)
