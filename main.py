# main.py
import os
from chain import TaskTreeChain
from command_execution import execute_command


def main():
    """
    Exemple d'utilisation de la TaskTreeChain:
    1. Récupère la première version de l'arbre de tâches.
    2. Exécute la commande retournée (simulation).
    3. Met à jour l'arbre de tâches avec la sortie de la commande.
    4. Boucle jusqu'à ce qu'il n'y ait plus de commande à exécuter (ou qu'on décide d'arrêter).
    """

    # Assurez-vous d'avoir votre clé API OpenAI dans une variable d'environnement
    # ou remplacez ci-dessous par votre clé directement (non recommandé pour la sécurité).
    openai_api_key = os.getenv("OPENROUTER_API_KEY")

    # Initialisation de la classe
    task_tree_chain = TaskTreeChain("127.0.0.1")

    # Affiche l'arbre initial
    print("=== Arbre de tâches initial ===")
    print(task_tree_chain.get_current_task_tree(), "\n")

    while True:
        # Cherche la prochaine commande
        next_command = task_tree_chain.get_next_command()
        if not next_command:
            print("Aucune commande suggérée. Fin du processus.")
            break

        # Affiche la commande suggérée
        print(f"Prochaine commande: {next_command}")

        # Executer la commande sur une machine Linux, puis récupèreriez la sortie.
        output = execute_command(next_command)

        print(f"Sortie de la commande: {output}\n")

        # Mise à jour de l'arbre de tâches avec la sortie
        updated_tree = task_tree_chain.update_task_tree_with_output(output)

        # Affiche l'arbre de tâches mis à jour
        print("=== Arbre de tâches mis à jour ===")
        print(updated_tree, "\n")

        # Condition de sortie (par exemple, nombre itérations max ou détection d'un état final)
        # Dans un vrai scénario, vous vérifieriez l'avancement du test.
        # Ici, on peut limiter arbitrairement le nombre de tours à 3 pour la démo
        # (ou bien continuer tant qu'il y a une commande).
        # On va stopper après quelques boucles pour éviter la boucle infinie.
        # Vous pouvez adapter selon vos besoins.
        break


if __name__ == "__main__":
    main()
