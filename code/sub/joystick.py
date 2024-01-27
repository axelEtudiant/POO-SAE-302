import pygame, math, json, socket, time

class Joystick:
    def __init__(self) -> None:
        """Constructeur de la classe Joystick
        """
        self.__boutons: dict
        self.__boutons_old: dict
        self.__connected: bool
        self.__joystick_name: str
        self.__socket: socket

        self.__boutons_old: int = 0
        self.__connected = False

        pygame.init()
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            self.__connected = False
            print("Err: Aucune manette de connectée.")
            quit()
        else:
            self.__joystick = pygame.joystick.Joystick(0)
            self.__joystick.init()
            self.__joystick_name = self.__joystick.get_name()
            self.__connected = True

    def is_connected(self) -> bool:
        """Méthode de la classe Joystick qui permet de savoir si une manette est connectée.

        Returns:
            bool: Booléen, True si une manette est connectée
        """
        return self.__connected

    def get_name(self) -> str:
        """Méthode de la classe Joystick qui permet de savoir le nom de la manette.

        Returns:
            str: Nom de la manette
        """
        return self.__joystick_name

    def get_buttons(self) -> None:
        """Méthode de la classe Joystick qui permet de récuper les actions faites et les envoyer au serveur.
        """
        pygame.event.pump()
        button_state = int(self.__joystick.get_button(0)) # Bouton X(A)
        while button_state == 1: # Tant que le bouton X(A) de la manette est appuyé on envoie les informations du joystick au serveur
            pygame.event.pump() # Mise à jour des valeurs des boutons
            x_axis = -self.__joystick.get_axis(0) # Axe vertical
            y_axis = -self.__joystick.get_axis(1) # Axe horizontal
            
            msg = f"MVMT {button_state} {round(x_axis,2)} {round(y_axis,2)}"
            print(msg)
            self.envoyer(msg)
            button_state = int(self.__joystick.get_button(0))
            time.sleep(0.2)
    
    def envoyer(self, msg: str) -> None:
        """Méthode de la classe Joystick qui permet d'envoyer un message au serveur.

        Args:
            msg (str): Message à envoyer au serveur
        """
        self.__socket.send(json.dumps({"q": f"{msg}"}).encode("utf-8"))

    def recevoir(self) -> str:
        """Méthode de la classe Joystick qui permet de recevoir un message envoyé par le serveur.

        Returns:
            str: Message reçu
        """
        msg = self.__socket.recv(1024).decode("utf-8")
        return json.loads(msg)["q"]

    def quit(self) -> None:
        """Méthode de la classe Joystick pour arréter l'échange.
        """
        self.__joystick.quit()
        pygame.quit()

    def mainloop(self, socket: socket) -> None:
        """Méthode de la classe Joystick qui permet d'envoyer au serveur les actions effectuées avec la manette.

        Args:
            socket (socket): Socket en cours avec le serveur
        """
        self.__socket = socket
        while self.__boutons_old != 1:
            self.get_buttons() 
            self.__boutons_old = int(self.__joystick.get_button(1))
            
        self.envoyer("QUIT")
