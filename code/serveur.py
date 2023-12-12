import socket, json
from typing import *
from sub.security import MacFilter
from sub.loging import Log
from sub.requests import Requests
from sub.exception import *
from datetime import datetime

class Serveur:
    def __init__(self, port_serveur: int) -> None:
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
        message = json.dumps({"q": query}).encode("utf-8")
        self.__sock_ex.send(message)
        self.__log.write("donnees.log", f"[{datetime.now()}] - SERVER has send '{query}' to {self.__addr}.")

    def recevoir(self) -> str:
        received = json.loads(self.__sock_ex.recv(1024).decode("utf-8"))["q"]
        self.__log.write("donnees.log", f"[{datetime.now()}] - {self.__addr} has send '{received}' to SERVER.")
        return received
    
    def authentification(self) -> None:
        self.__sock.listen(1)
        self.__sock_ex, self.__addr = self.__sock.accept()
        self.__addr = self.__addr[0]

        self.__log.write("connexion.log", f"[{datetime.now()}] - {self.__addr} has initialized the connection.")

        if self.__addr == "127.0.0.1" or self.__mac_filter.filter(self.__addr) is True:
            status_mac = f"CONN ACCEPTED MAC"
            self.envoyer(status_mac)
        else:
            status_mac = f"CONN REFUSED MAC"
            self.envoyer(status_mac)
        
        if status_mac.split()[1].lower() == "accepted":
            self.envoyer(f"CONN WAITING USER")
            self.__login = self.recevoir().split()[2]

            self.envoyer(f"CONN WAINTING PASSWORD")
            self.__password = self.recevoir().split()[2]

            self.__bdd_connexion.open()
            liste_login = self.__bdd_connexion.reponse_multiple('SELECT login, password FROM login ;')
            self.__bdd_connexion.close()

            if (self.__login, self.__password) in liste_login:
                self.envoyer(f"CONN ACCEPTED LOGIN")
                self.__connected = True
            else:
                self.envoyer(f"CONN REFUSED LOGIN")
                self.__connected = True
            
    def main(self) -> None:
        while not self.__connected:
            self.authentification()
        
if __name__=="__main__":
    server: Serveur = Serveur(5001)
    server.main()