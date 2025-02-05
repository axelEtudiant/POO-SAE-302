# -*- coding : utf8 -*-
import socket, json, sys, maskpass, hashlib
from sub.joystick import Joystick

class Client:
    def __init__(self, ip_serveur: str, port_serveur: int) -> None:
        """Méthode constructeur de la classe Client.
        
        Args:
            ip_serveur: str -> L'IP du serveur.
            port_serveur: int -> Le port d'écoute du serveur.
        """
        # Déclaration
        self.__ip_serveur: str
        self.__port_serveur: int
        self.__socket: socket
        self.__connexion_ok: bool
        self.__authentification_ok: bool
        self.__joystick: Joystick
        # Initialisation
        self.__ip_serveur = ip_serveur
        self.__port_serveur = port_serveur
        self.__connexion_ok = False
        self.__authentification_ok = False
        self.__joystick = Joystick()

    def get_connexion_ok(self) -> bool:
        return self.__connexion_ok

    def get_authentification_ok(self) -> bool:
        return self.__authentification_ok

    def get_joystick(self) -> Joystick:
        return self.__joystick

    def connexion(self) -> None:
        """Méthode de la classe Client qui initialise le socket
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création de la socket
        self.__socket.connect((self.__ip_serveur, self.__port_serveur)) # Connection au service distant
        # Filtrage MAC
        msg_serveur = self.recevoir()
        print(msg_serveur)
        if msg_serveur.split()[1].lower() == "accepted": # Mac
            self.__connexion_ok = True

    def authentification(self, login: str, passwd: str) -> str:
        """Méthode de la classe Client qui permet à l'utilisateur de s'authentifier.

        Args:
            login (str): Login de l'utilisateur
            passwd (str): passwd de l'utilisateur

        Return: 
            str: La réponse du serveur 
        """
        msg_serveur = self.recevoir()
        if self.__connexion_ok:
            msg_serveur = "a a"
            self.envoyer(f"CONN LOGIN {login} {passwd}")
            msg_serveur = self.recevoir()
            if msg_serveur.split()[1].lower() == "accepted":
                self.__authentification_ok = True
            return msg_serveur

    def authentification_interactive(self) -> None:
        """Méthode de la classe Client qui permet de récupérer les identifiants de l'utilisateur
        """
        nb_tentatives: int = 0
        while not self.__authentification_ok and nb_tentatives < 3:
            login = input('Votre login: ')
            passwd = hashlib.sha256((maskpass.askpass(prompt='Votre mot de passe: ', mask='*')).encode("utf-8")).hexdigest()
            self.authentification(login=login, passwd=passwd)
            nb_tentatives += 1

    def quitter(self) -> None:
        """Méthode de la classe Client qui permet de fermer le client.
        """
        self.envoyer("QUIT")
        self.__socket.close()

    def main(self) -> None:
        """Méthode de la classe Client qui permet de lancer l'authentification et l'envoie des contrôles.
        """
        self.connexion()
        self.authentification_interactive()
        if self.__joystick.is_connected():
            try:
                self.__joystick.mainloop(self.__socket)
            except KeyboardInterrupt as e:
                print(e)
            finally:
                self.__joystick.quit()
        self.quitter()

    def envoyer(self, msg: str) -> None:
        """Méthode de la classe Client qui permet d'envoyer un message au serveur.

        Args:
            msg (str): Message à envoyer au serveur
        """
        self.__socket.send(json.dumps({"q": f"{msg}"}).encode("utf-8"))

    def recevoir(self) -> str:
        """Méthode de la classe Client qui permet de recevoir le message envoyé par le serveur.

        Returns:
            str: Message reçu
        """
        msg = self.__socket.recv(1024).decode("utf-8")
        return json.loads(msg)["q"]

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