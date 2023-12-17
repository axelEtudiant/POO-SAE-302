"""

Contient toutes les classes relatives aux requêtes de base de données.

"""

import sqlite3
from typing import *


class Requests:
    """Classe Requests permet la gestion des requêtes vers la base de données
    """
    def __init__(self, nom_bdd: str) -> None:
        """Constructeur de la classe Requests

        Args:
            nom_bdd (str): Nom du fichier de la base de données
        """
        self.__nom_bdd: str = nom_bdd
        self.__connection: sqlite3.Connection
        self.__cursor: sqlite3.Cursor

    def open(self) -> None:
        """Méthode de la classe Requests qui permet d'ouvrir la connexion avec la base de données.
        """
        self.__connection = sqlite3.connect(self.__nom_bdd)
        self.__cursor = self.__connection.cursor()
    
    def reponse_unique(self, requete: str) -> Tuple:
        """Méthode de la classe Requests qui permet d'envoyer une requête unique à la base de données.

        Args:
            requete (str): Requête à envoyer à la base de données

        Returns:
            Tuple: Résultat de la requête
        """
        try:
            resultat = self.__cursor.execute(requete)
            return resultat.fetchone()
        except Exception as e: # Si la requête échoue alors on affiche dans les logs l'erreur
            print(e)

    def reponse_multiple(self, requete: str) -> List[Tuple]:
        """Méthode de la classe Requests qui permet d'envoyer des requêtes multiple à la base de données.

        Args:
            requete (str): Requête à envoyer à la base de données

        Returns:
            List[Tuple]: Résultat de la requête
        """
        try:
            resultat = self.__cursor.execute(requete)
            return resultat.fetchall()
        except Exception as e: # Si la requête échoue alors on affiche dans les logs l'erreur
            print(e)

    def insert(self, requete: str) -> None:
        """Méthode de la classe Requests qui permet d'envoyer une requête d'insertion à la base de données.

        Args:
            requete (str): Requête d'insertion à envoyer à la base de données
        """
        try:
            self.__cursor.execute(requete)
        except Exception as e: # Si la requête échoue alors on affiche dans les logs l'erreur
            print(e)
        
    def sauvegarde_bdd(self) -> None:
        """Méthode de la classe Requests qui permet de sauvegarder les modifications apporter à la base de données.
        """
        self.__connection.commit()

    def close(self) -> None:
        """Méthode de la classe Requests qui permet de fermer la connexion à la base de données.
        """
        try:
            self.__connection.close()
        except Exception as esc: # Si il y a une erreur alors on annule les modifications et on log l'erreur
            print(f'Exception: {esc}')
            self.__connection.rollback()
        finally:
            self.__connection.close()