import os
import requests
from bs4 import BeautifulSoup

# URL cible
url = "https://www.kali.org/tools/all-tools/"

# Dossier de destination
destination_folder = "extracted_tools"

# Créer le dossier s'il n'existe pas
os.makedirs(destination_folder, exist_ok=True)

# Envoyer une requête HTTP pour obtenir le contenu de la page
response = requests.get(url)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Récupérer tous les liens qui commencent par "https://www.kali.org/tools/" mais exclure "https://www.kali.org/tools/"
    links = [
        a['href'] for a in soup.find_all('a', href=True)
        if a['href'].startswith("https://www.kali.org/tools/") and a['href'] != "https://www.kali.org/tools/all-tools/"
           and a['href'] != "https://www.kali.org/tools/" and "#" not in a['href']
    ]

    # Afficher le nombre de liens trouvés
    print(f"Nombre de liens trouvés : {len(links)}")

    # Traiter et enregistrer chaque page
    for link in links:
        page_response = requests.get(link)
        if page_response.status_code == 200:
            # Parser le contenu HTML de la page
            tool_soup = BeautifulSoup(page_response.text, "html.parser")

            # Trouver tous les <h5> et leurs contenus siblings pour chaque outil
            h5_sections = tool_soup.find_all("h5")
            if h5_sections:
                content = []
                for tool_section in h5_sections:
                    section_content = [tool_section.get_text(strip=True)]
                    for sibling in tool_section.find_next_siblings():
                        if sibling.name == "h5":
                            break
                        section_content.append(sibling.get_text(strip=True))
                    content.extend(section_content)

                # Nom du fichier basé sur l'URL
                file_name = os.path.join(destination_folder, link.split("/")[-2] + ".txt")
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write("\n".join(content))
                print(f"Description extraite : {link}")
            else:
                print(f"Aucune section trouvée pour : {link}")
        else:
            print(f"Échec du téléchargement : {link}")
else:
    print(f"Échec du chargement de la page. Code d'état : {response.status_code}")