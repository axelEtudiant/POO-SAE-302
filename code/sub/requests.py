"""

Contient toutes les classes relatives aux requêtes de base de données.


"""

import sqlite3
from typing import *

class Requests:
    def __init__(self, nom_bdd: str) -> None:
        self.__nom_bdd: str = nom_bdd
        self.__connection: sqlite3.Connection
        self.__cursor: sqlite3.Cursor

    def open(self) -> None:
        self.__connection = sqlite3.connect(self.__nom_bdd)
        self.__cursor = self.__connection.cursor()
    
    def reponse_unique(self, requete: str) -> Tuple:
        try:
            resultat = self.__cursor.execute(requete)
            return resultat.fetchone()
        except Exception as e:
            print(e)

    def reponse_multiple(self, requete: str) -> List[Tuple]:
        try:
            resultat = self.__cursor.execute(requete)
            return resultat.fetchall()
        except Exception as e:
            print(e)

    def insert(self, requete: str) -> None:
        try:
            self.__cursor.execute(requete)
        except Exception as e:
            print(e)
        
    def sauvegarde_bdd(self) -> None:
        self.__connection.commit()

    def close(self) -> None:
        try:
            self.__connection.close()
        except Exception as esc:
            print(f'Exception: {esc}')
            self.__connection.rollback()
        finally:
            self.__connection.close()