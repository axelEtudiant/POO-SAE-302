# -*- coding : utf8 -*-

import socket
import json
import sys


class Client:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        """Méthode constructeur de la classe client.
        Params:
            ip_serveur: str -> L'IP du serveur.
            port_serveur: int -> Le port d'écoute du serveur.
        """
        self.__ip_serveur: str
        self.__port_serveur: int
        self.__socket: socket
        self.__connexion_ok: bool
        self.__authentification_ok: bool

        self.__ip_serveur = ip_serveur
        self.__port_serveur = port_serveur
        self.__connexion_ok = False
        self.__authentification_ok = False

    def connexion(self) -> None:
        """Initialise la connexion au serveur
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création de la socket
        self.__socket.connect((self.__ip_serveur, self.__port_serveur)) # Connection au service distant
        # Filtrage MAC
        msg_serveur = self.recevoir()
        print(msg_serveur)
        if msg_serveur.split()[1].lower() == "accepted":
            self.__connexion_ok = True

    def authentification(self) -> None:
        if self.__connexion_ok:
            msg_serveur: str = "a a"
            nb_tentatives: int= 0
            while str(msg_serveur).split()[1].lower() != "accepted" and nb_tentatives < 3:
                # Demande du user
                msg_serveur = self.recevoir()
                print(msg_serveur)

                # Envoi du user
                self.envoyer(f"CONN USER {input('Votre user: ')}")

                # Demande du password
                msg_serveur = self.recevoir()
                print(msg_serveur)

                # Envoi du password
                self.envoyer(f"CONN PASSWORD {input('Votre mot de passe: ')}")

                # Demande d'acceptation
                msg_serveur = self.recevoir()
                print(msg_serveur)

                # Si la connexion est acceptée
                if msg_serveur.split()[1].lower() == "accepted":
                    self.__authentification_ok = True

                if msg_serveur.split()[1].lower() == "conn quit":
                    nb_tentatives = 3
                    self.quitter()
                nb_tentatives += 1

    def mouvement(self, mvmt: str):
        self.envoyer(f"MVMT {mvmt} 1")

    def quitter(self) -> None:
        self.__socket.close()

    def main(self) -> None:
        self.connexion()
        self.authentification()
        self.quitter()

    def envoyer(self, msg: str) -> None:
        self.__socket.send(json.dumps({"q": f"{msg}"}).encode("utf-8"))

    def recevoir(self) -> str:
        return json.loads(self.__socket.recv(1024).decode("utf-8"))["q"]

if __name__=="__main__":
    try:
        ip_serveur = str(sys.argv[1].split(":")[0])
        port_serveur = int(sys.argv[1].split(":")[1])
    except IndexError as e:
        ip_serveur = "10.3.141.1"
        port_serveur = 5001

    client: Client
    client = Client(ip_serveur=ip_serveur, port_serveur=port_serveur)
    client.main()