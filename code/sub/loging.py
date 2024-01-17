from datetime import datetime
import json
"""

Contient toutes les classes relatives aux logs du serveur.

"""

class Log:
    """Classe Log qui permet de mettre à jour les fichier de logs.
    """
    # Variable globale: Répertoire contenant les fichiers de log
    LOG_DIRECTORY = "log"

    def __init__(self) -> None:
        """Constructeur de la classe Log"""
        None
    
    def write(self, nom_fichier: str, message: str) -> None:
        """Méthode de la classe Log qui permet d'écrire le message de log dans le bon fichier.

        Args:
            nom_fichier (str): Nom du fichier de log
            message (str): Message de log
        """
        with open(f"{Log.LOG_DIRECTORY}/{nom_fichier}", mode="at", encoding="utf-8") as fichier:
            print(message)
            fichier.write(message + "\n")