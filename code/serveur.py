import socket, json
from typing import *
from sub.security import MacFilter
from sub.loging import Log
from sub.requests import Requests
from sub.exception import *
from datetime import datetime


class Serveur:
    """Classe Serveur qui permet de gérer la connexion avec des machines clientes. 
    """
    def __init__(self, port_serveur: int) -> None:
        """Constructeur de la classe Serveur

        Args:
            port_serveur (int): Port sur lequel le serveur est en écoute
        """
        # Déclaration
        self.__log: Log
        self.__mac_filter: MacFilter
        self.__bdd_connexion: Requests

        self.__sock: socket
        self.__port_serveur: int

        self.__sock_ex: socket
        self.__login: str
        self.__password: str
        self.__addr: str
        self.__connected: bool

        # Initialisation
        self.__log =  Log()
        self.__mac_filter = MacFilter()
        self.__bdd_connexion = Requests("bdd/connexion.sqlite3")

        self.__port_serveur = port_serveur

        self.__connected = False

        # Mise en écoute du serveur
        self.__sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__sock.bind(("", self.__port_serveur))

    def envoyer(self, query: str) -> None:
        """Méthode de la classe Serveur qui permet d'envoyer un message au client connecté.

        Args:
            query (str): message à envoyer
        """
        message = json.dumps({"q": query}).encode("utf-8")
        self.__sock_ex.send(message)
        self.__log.write("donnees.log", f"[{datetime.now()}] - SERVER has send '{query}' to {self.__addr}.")

    def recevoir(self) -> str:
        """Méthode de la classe Serveur qui permet de recevoir le message envoyé par le client.

        Returns:
            str: Message du client
        """
        received = json.loads(self.__sock_ex.recv(1024).decode("utf-8"))["q"]
        self.__log.write("donnees.log", f"[{datetime.now()}] - {self.__addr} has send '{received}' to SERVER.")
        return received
    
    def authentification(self) -> None:
        """Méthode de la classe Serveur qui gère l'authentification du client connecté.
        """
        # Ecoute sur le port 
        self.__sock.listen(1)
        self.__sock_ex, self.__addr = self.__sock.accept()
        self.__addr = self.__addr[0]
        # Log d'une tentative de connexion
        self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has initialized the connection.")

        if self.__addr == "127.0.0.1" or self.__mac_filter.filter(self.__addr) is True: # Si l'adresse est autorisé alors on envoie un message de confirmation
            status_mac = f"CONN ACCEPTED MAC"
            self.envoyer(status_mac) # Envoie du message de confirmation

            self.envoyer(f"CONN WAITING USER") # Envoie la demande d'authentification
            self.__login = self.recevoir().split()[2] # !!!!

            self.envoyer(f"CONN WAINTING PASSWORD") 
            self.__password = self.recevoir().split()[2] # !!!!

            self.__bdd_connexion.open() # Ouverture de la base de données
            liste_login = self.__bdd_connexion.reponse_multiple('SELECT login, password FROM login ;') # Requête si les identifiants correspondent
            self.__bdd_connexion.close() # Fermeture de la base de données

            if (self.__login, self.__password) in liste_login: # Si les identifiants sont bien dans la base de données alors on accepte l'authentification
                self.envoyer(f"CONN ACCEPTED LOGIN")
                self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has log in with {self.__login} account.")
                self.__connected = True
            else: # Sinon on refuse l'authentification
                self.envoyer(f"CONN REFUSED LOGIN")
                self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has failed to log in with {self.__login} account.")
                self.__connected = True
        else: # Sinon on refuse la connection
            status_mac = f"CONN REFUSED MAC"
            self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has tried to connect but his address is invalid.")
            self.envoyer(status_mac)

    def main(self) -> None:
        """Méthode de la classe Serveur qui permet de lancer la recherche de client si aucun n'est connecté.
        """
        while not self.__connected:
            self.authentification()
        
if __name__=="__main__":
    # Initialisation
    server: Serveur = Serveur(5001)
    server.main()