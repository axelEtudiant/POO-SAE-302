# -*- coding : utf8 -*-
import socket, json
from typing import *
from sub.security import MacFilter
from sub.loging import Log
from sub.requests import Requests
from sub.exception import *
from datetime import datetime
from threading import Thread

class Serveur:
    # -- CONSTRUCTEUR
    def __init__(self, port_serveur: int) -> None:
        """Constructeur de la classe Serveur.
        
        Args:
            port_serveur (int): Port sur lequel le serveur écoute.
        """
        # Déclaration
        self.__port_serveur: int
        self.__log: Log
        self.__mac_filter: MacFilter
        self.__bdd_connexion: Requests
        self.__login: str
        self.__password: str
        self.__addr_client: str
        self.__port_client: int
        self.__connected: bool
        self.__socket_ecoute: socket
        self.__socket_echange: socket

        # Initialisation
        Thread.__init__(self)
        self.__port_serveur = port_serveur
        self.__log = Log()
        self.__mac_filter = MacFilter()
        self.__bdd_connexion = Requests("bdd/connexion.sqlite3")
        self.__connected = False
        self.__authentificated = False

    # -- OBSERVATEUR
    def get_connected(self) -> bool:
        """Méthode de la classe Serveur qui permet de savoir si un utilisateur est connecté ou non.
        
        Returns:
            bool: Statut de la connexion
        """
        return self.__connected
    
    def get_authentificated(self) -> bool:
        """Méthode de la classe Serveur qui renvoie le statut de l'authentification.

        Returns:
            bool: Statut de l'authentification
        """
        return self.__authentificated

    # -- MODIFICATEURS

    # - ENVOYER / RECEVOIR
    def envoyer(self, query: str) -> None:
        """Méthode de la classe Serveur qui permet d'envoyer un message au client connecté.

        Args:
            query (str): message à envoyer
        """
        message = json.dumps({"q": query}).encode("utf-8")
        self.__socket_echange.send(message)
        self.__log.write("donnees.log", f"[{datetime.now()}] - SERVER has send '{query}' to {self.__addr_client}.")

    def recevoir(self) -> str:
        """Méthode de la classe Serveur qui permet de recevoir le message envoyé par le client.

        Returns:
            str: Message du client
        """
        msg = self.__socket_echange.recv(1024).decode("utf-8")
        print(msg)
        received = json.loads(msg)["q"]
        self.__log.write("donnees.log", f"[{datetime.now()}] - {self.__addr_client} has send '{received}' to SERVER.")
        return received
    
    # - ECOUTE
    def ecoute(self) -> None:
        """Méthode de la classe Serveur qui écoute sur le port du serveur, toutes nouvelles tentatives de connexions.
        """
        self.__socket_ecoute: socket
        self.__socket_ecoute = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__socket_ecoute.bind(("", self.__port_serveur))
        self.__log.write("connexion.log", f"[{datetime.now()}] - Server has initialized the port {self.__port_serveur}.")

    def attente_client(self) -> None:
        """Méthode de la classe Serveur qui attend la connexion du client sur l'échange TCP avec le serveur."""
        self.__socket_ecoute.listen(1)
        self.__socket_echange, addr = self.__socket_ecoute.accept()
        self.__addr_client = addr[0]
        self.__port_client = addr[1]
        self.__connected = True
        self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr_client} has initialized the port {self.__port_client}.")
    
    # - AUTHENTIFICATION
    def authentification(self) -> None:
        """Méthode de la classe Serveur qui gère l'authentification du client connecté.
        """
        if self.__addr_client == "127.0.0.1" or self.__mac_filter.filter(self.__addr_client): # Si l'adresse est autorisé alors on envoie un message de confirmation
            status_mac = f"CONN ACCEPTED MAC"
            self.envoyer(status_mac) # Envoie du message de confirmation

            self.envoyer(f"CONN WAITING USER") # Envoie la demande d'authentification
            self.__login = self.recevoir().split()[2]

            self.envoyer(f"CONN WAINTING PASSWORD")
            self.__password = self.recevoir().split()[2]

            self.__bdd_connexion.open() # Ouverture de la base de données
            liste_login = self.__bdd_connexion.reponse_multiple('SELECT login, password FROM login ;') # Requête si les identifiants correspondent
            self.__bdd_connexion.close() # Fermeture de la base de données

            if (self.__login, self.__password) in liste_login: # Si les identifiants sont bien dans la base de données alors on accepte l'authentification
                self.envoyer(f"CONN ACCEPTED LOGIN")
                self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr_client} has log in with {self.__login} account.")
                self.__authentificated = True
            else: # Sinon on refuse l'authentification
                self.envoyer(f"CONN REFUSED LOGIN")
                self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr_client} has failed to log in with {self.__login} account.")
        else: # Sinon on refuse la connection
            status_mac = f"CONN REFUSED MAC"
            self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr_client} has tried to connect but his address is invalid.")
            self.envoyer(status_mac)

    # - MAIN
    def main(self) -> None:
        """Méthode de la classe qui permet de lancer l'écoute sur le port ainsi que l'authentification en cas de connexion
        """
        self.ecoute()
        while True:
            self.attente_client()
            while not self.get_authentificated():
                while not self.get_connected():
                    self.attente_client()
                self.authentification()
                while True:
                    print(self.recevoir())

if __name__ == "__main__":
    serveur: Serveur = Serveur(5001)
    serveur.main()