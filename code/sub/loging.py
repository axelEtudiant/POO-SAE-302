"""

Contient toutes les classes relatives aux logs du serveur.


"""

from datetime import datetime
import json

class Log:
    LOG_DIRECTORY = "log"

    def __init__(self) -> None:
        None
    
    def write(self, nom_fichier: str, message: str) -> None:
        with open(f"{Log.LOG_DIRECTORY}/{nom_fichier}", mode="at", encoding="utf-8") as fichier:
            print(message)
            fichier.write(message + "\n")