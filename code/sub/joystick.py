import pygame, math, json
import socket

class Joystick:
    def __init__(self) -> None:
        self.__boutons: dict
        self.__boutons_old: dict
        self.__connected: bool
        self.__joystick_name: str
        self.__socket: socket

        self.__boutons = {}
        self.__boutons_old = {}
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
        return self.__connected

    def get_name(self) -> str:
        return self.__joystick_name

    def get_buttons(self) -> str:
        msg: str = ""

        for i in range(self.__joystick.get_numbuttons()):
            button_state = self.__joystick.get_button(i)
            self.__boutons[f"Bouton{i}"] = f"{button_state}"
        
        pygame.event.pump()

        x_axis = self.__joystick.get_axis(0)
        y_axis = self.__joystick.get_axis(1)

        angle_rad = math.atan2(y_axis, x_axis)
        angle_deg = math.degrees(angle_rad)
        angle_deg += 90

        if self.__boutons != self.__boutons_old:
            if self.__boutons_old == {}:
                pass
            else:
                if self.__boutons_old["Bouton0"] != self.__boutons["Bouton0"]:
                    val = self.__boutons.get("Bouton0")
                    if int(val) == 0:
                        angle_deg = ""
                    
                    msg = f"MVMT {val} {angle_deg}"
        
        self.__boutons_old = self.__boutons
        self.__boutons = {}

        
        return msg
    
    def envoyer(self, msg: str) -> None:
        self.__socket.send(json.dumps({"q": f"{msg}"}).encode("utf-8"))

    def recevoir(self) -> str:
        msg = self.__socket.recv(1024).decode("utf-8")
        return json.loads(msg)["q"]

    def quit(self) -> None:
        self.__joystick.quit()
        pygame.quit()

    def mainloop(self, socket: socket) -> None:
        self.__socket = socket
        while self.__boutons_old.get("Bouton1") != "1":
            button = self.get_buttons()
            if button != "":
                self.envoyer(button)                
        self.envoyer("QUIT")