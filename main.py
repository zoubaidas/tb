import os
from tasktree import TaskTreeChain
from command_execution import execute_command, format_output

import threading
import time
import sys

# Déclarez `stop_loading` comme variable globale
stop_loading = False

def loading_animation(text: str = "Loading..."):
    """
    Affiche une animation de chargement dans le terminal.
    """
    animation = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_loading:  # Arrête l'animation lorsque stop_loading est True
        sys.stdout.write(f"\r{text} {animation[idx % len(animation)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)  # Vitesse de l'animation


def main():
    """
    Exemple d'utilisation de la TaskTreeChain:
    1. Récupère la première version de l'arbre de tâches.
    2. Exécute la commande retournée.
    3. Met à jour l'arbre de tâches avec la sortie de la commande.
    4. Boucle jusqu'à ce qu'il n'y ait plus de commande à exécuter.
    """

    # Initialisation de la classe
    task_tree_chain = TaskTreeChain("10.10.10.245")

    # Affiche l'arbre initial
    print("=== Initial Task Tree ===")
    print(task_tree_chain.get_current_task_tree(), "\n")

    command_number = 0
    while True:
        # Cherche la prochaine commande
        next_command = task_tree_chain.get_next_command()
        if not next_command:
            print("No more commands to execute.")
            break



        # Utiliser la variable globale `stop_loading`
        #global stop_loading
        #stop_loading = False

        # Lancer l'animation dans un thread séparé
        #loading_thread = threading.Thread(target=loading_animation("Excecuting command..."))
        #loading_thread.start()

        try:
            # Executer la commande sur une machine Linux, puis récupérer la sortie.
            output = execute_command(next_command)
        finally:
            # Arrêter l'animation
            stop_loading = True
            #loading_thread.join()  # Attendre que le thread se termine proprement

        print(f"Command output:\n")
        format_output(output)

        # Mise à jour de l'arbre de tâches avec la sortie
        updated_tree = task_tree_chain.update_task_tree_with_output(output)

        # Affiche l'arbre de tâches mis à jour
        print("=== Updated Task Tree ===")
        print(updated_tree, "\n")

        command_number += 1
        if command_number > 10:  # Arrêter après 10 commandes pour éviter une boucle infinie
            break


if __name__ == "__main__":
    main()
