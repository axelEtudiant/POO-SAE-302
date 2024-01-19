# -*- coding : utf8 -*-
import socket, json
from typing import *
from sub.security import MacFilter
from sub.loging import Log
from sub.requests import Requests
from sub.exception import *
from datetime import datetime
from threading import Thread

class ServeurEcoute:
    def __init__(self, port_serveur: int) -> None:
        """Constructeur de la classe ServeurEcoute

        Args:
            port_serveur (int): Port du serveur
        """
        self.__log: Log
        self.__addr: str
        self.__addr: bool
        self.__mac_filter: MacFilter
        self.__socket_echange: socket
        self.__mac_filter = MacFilter()
        self.__log = Log()
        self.__socket_ecoute: socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.__socket_ecoute.bind(("", port_serveur))
        
        self.__log.write("connexion.log", f"[{datetime.now()}] - Server has initialized the port {port_serveur}.")
        
    def attente(self) -> socket:
        """Méthode de la classe ServeurEcoute qui renvoie le socket d'échange du nouveau client

        Returns:
            socket: Socket d'échange du client
        """
        self.__socket_ecoute.listen(1)
        self.__socket_echange, ADR = self.__socket_ecoute.accept()
        self.__addr = ADR[0]
        if self.__addr == "127.0.0.1" or self.__mac_filter.filter(self.__addr) is True: # Si l'adresse est autorisé alors on envoie un message de confirmation
            self.__log.write("connexion.log", f"[{datetime.now()}] - Client {self.__addr} has initialized connection with SERVER to the port {ADR[1]}.")
            self.connexion("accepted") # Envoie du message de confirmation
            self.__addr_valid = True
        else: # Sinon on refuse la connection
            self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has tried to connect but his address is invalid.")
            self.__addr_valid = False
        return self.__addr_valid ,self.__socket_echange, self.__addr

    def connexion(self, message) -> None:
        """Méthode de la classe ServeurEcoute qui envoie un message au client lorsque quelqu'un est déjà connecté au serveur ou alors son adresse est invalide.
        """
        str_message: str
        if message == "accepted":
            query = json.dumps({"q":"CONN ACCEPTED MAC" }).encode("utf-8")
        elif message == "occupee":
            str_message = f"[{datetime.now()}] - SERVER has already an authentified user."
            query = json.dumps({"q":"CONN OCCUPIED" }).encode("utf-8")
            self.__log.write("connexion.log", f"{str_message} Connection refused for {self.__addr}.")
        else:
            str_message = f"[{datetime.now()}] - Invalide address."
            query = json.dumps({"q":"CONN REFUSED MAC" }).encode("utf-8")
            self.__log.write("connexion.log", f"{str_message} Connection refused for {self.__addr}.")

        self.__socket_echange.send(query)


class Serveur(Thread):
    """Classe Serveur qui permet de gérer la connexion avec des machines clientes. 
    """
    def __init__(self, socket_echange: socket, ADR: str) -> None:
        """Constructeur de la classe Serveur

        Args:
            port_serveur (int): Port sur lequel le serveur est en écoute
        """
        # Déclaration
        self.__log: Log
        self.__bdd_connexion: Requests
        self.__nb_tentatives: int
        self.__socket_echange: socket
        self.__login: str
        self.__password: str
        self.__addr: str
        self.__connected: bool

        # Initialisation
        Thread.__init__(self)
        self.__log =  Log()
        self.__bdd_connexion = Requests("bdd/connexion.sqlite3")

        self.__socket_echange = socket_echange
        self.__addr = ADR

        self.__connected = False

    def get_connected(self) -> None:
        """Méthode de la classe Serveur qui permet de savoir si un utilisateur est connecté ou non.
        """
        return self.__connected

    def envoyer(self, query: str) -> None:
        """Méthode de la classe Serveur qui permet d'envoyer un message au client connecté.

        Args:
            query (str): message à envoyer
        """
        message = json.dumps({"q": query}).encode("utf-8")
        self.__socket_echange.send(message)
        self.__log.write("donnees.log", f"[{datetime.now()}] - SERVER has send '{query}' to {self.__addr}.")

    def recevoir(self) -> str:
        """Méthode de la classe Serveur qui permet de recevoir le message envoyé par le client.

        Returns:
            str: Message du client
        """
        received = json.loads(self.__socket_echange.recv(1024).decode("utf-8"))["q"]
        self.__log.write("donnees.log", f"[{datetime.now()}] - {self.__addr} has send '{received}' to SERVER.")
        return received
    
    def authentification(self) -> None:
        """Méthode de la classe Serveur qui gère l'authentification du client connecté.
        """

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

    def main(self) -> None:
        """Méthode de la classe Serveur qui permet de lancer la recherche de client si aucun n'est connecté.
        """
        self.__nb_tentatives = 0
        while not self.__connected and self.__nb_tentatives < 3:
            self.__nb_tentatives += 1
            self.authentification()
        if not self.__connected and self.__nb_tentatives == 3:
            self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has tried too many time to log in.")
            self.quitter()

    def quitter(self) -> None:
        """Méthode de la classe Serveur qui permet de fermer la connexion actuelle.
        """
        self.envoyer(f"CONN QUIT")
        self.__socket_echange.close()
        self.__log.write("connexion.log", f"[{datetime.now()}] - SERVER has closed the connection with {self.__addr}")


if __name__=="__main__":
    # Initialisation
    port_ecoute: int
    serveur_ecoute: ServeurEcoute
    socket_client: socket
    serveur: Serveur
    ADR: str
    addr_valid: bool
    # declaration des variables
    port_ecoute = 5001

#    try:
    serveur_ecoute = ServeurEcoute(port_ecoute)
    addr_valid, socket_client, ADR = serveur_ecoute.attente()
    if addr_valid:
        serveur = Serveur(socket_client, ADR)
        serveur.start()
        serveur.main()
    while True :
        addr_valid, socket_client, ADR = serveur_ecoute.attente()
        if addr_valid:    
            if (serveur is not None) and (serveur.get_connected()):
                serveur_ecoute.connexion("occupee")
            else:
                serveur = Serveur(socket_client, ADR)
                serveur.start()
                serveur.main()               
#    except Exception as ex:
#        print("erreur : ", ex)