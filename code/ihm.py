#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import string, random, os
from client import *
from typing import List
from tkinter import *
from sub.exception import *

class Main_IHM(Tk):
    POLICE: str = "times"
    TAILLE_POLICE: int = 12
    
    def __init__(self) -> None:
        self.__client: Client
        self.__ihm_connexion: Connexion
        self.__ihm_authentification: Authentification

    def connexion(self) -> None:
        self.__ihm_connexion = Connexion()
        self.__ihm_connexion.mainloop()
        self.__client = self.__ihm_connexion.get_client()

    def authentification(self) -> None:
        self.__ihm_authentification = Authentification(self.__client)
        self.__ihm_authentification.mainloop()
        self.__client = self.__ihm_authentification.get_client()

    def mouvement(self) -> None:
        self.__ihm_mouvement = Mouvement(self.__client)
        self.__ihm_mouvement.mainloop()
        self.__client = self.__ihm_mouvement.get_client()

    def main(self) -> None:
        self.connexion()
        if self.__client.get_connexion_ok():
            self.authentification()
            if self.__client.get_authentification_ok():
                self.mouvement()
        self.__client.quitter()

class Connexion(Tk):
    def __init__(self) -> None:
        Tk.__init__(self)
        self.__fen_connexion: Frame
        self.__lbl_err: Label
        self.__lbl_ip_serveur: Label
        self.__entree_ip_serveur: Entry
        self.__lbl_port_serveur: Label
        self.__entree_port_serveur: Entry
        self.__btn_connexion: Button
        self.__btn_quitter: Button

        self.__fen_connexion = Frame(self, borderwidth=10, relief="groove", padx=10, pady=10)
        self.__lbl_err = Label(self.__fen_connexion, borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__lbl_ip_serveur = Label(self.__fen_connexion, text="IP du serveur :", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_ip_serveur = Entry(self.__fen_connexion, width=30)
        self.__lbl_port_serveur = Label(self.__fen_connexion, text="Port du serveur :", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_port_serveur = Entry(self.__fen_connexion, width=30)
        self.__btn_connexion = Button(self.__fen_connexion, text="Connexion", font=(Main_IHM.POLICE,Main_IHM.TAILLE_POLICE), bg="grey", command=self.connexion)
        self.__btn_quitter = Button(self.__fen_connexion, text = "Quitter", font= (Main_IHM.POLICE,Main_IHM.TAILLE_POLICE), bg="red", command=self.destroy)

        self.__entree_ip_serveur.insert(0, "10.3.141.1")
        self.__entree_port_serveur.insert(0, "5001")

        self.__fen_connexion.pack()
        self.__lbl_ip_serveur.grid(row=1, column=0)
        self.__entree_ip_serveur.grid(row=1, column=1)
        self.__lbl_port_serveur.grid(row=2, column=0)
        self.__entree_port_serveur.grid(row=2, column=1)
        self.__btn_connexion.grid(row=3, column=1)
        self.__btn_quitter.grid(row=3, column=2)

        self.__ip_serveur: str
        self.__port_serveur: int
        self.__client: Client

    def get_client(self) -> Client:
        return self.__client

    def connexion(self):
        try:
            erreur: bool = False
            self.__ip_serveur = self.__entree_ip_serveur.get()
            self.__port_serveur = self.__entree_port_serveur.get()
            if len(self.__ip_serveur.split(".")) != 4:
                raise ErrIP
            if not self.__port_serveur.isdigit():
                raise ErrPORT
        except ErrIP as e:
            erreur = True
            text = f"Erreur 'IP' : {e}"
            color = "red"
        except ErrPORT as e:
            erreur = True
            text = f"Erreur 'PORT' : {e}"
            color = "red"
        except TimeoutError as e:
            erreur = True
            text = f"Erreur 'TIMEOUT' : Le serveur n'est pas accessible."
            color = "red"
        except Exception as e:
            erreur = True
            text = f"Erreur : {e}"
            color = "red"
        finally:
            if erreur:
                self.__lbl_err.configure(text=text, background=color)
                self.__lbl_err.grid(row=0, column=1)
            else:
                self.__port_serveur = int(self.__port_serveur)
                self.__client = Client(ip_serveur=self.__ip_serveur, port_serveur=self.__port_serveur)
                self.__client.connexion()
                self.destroy()

class Authentification(Tk):
    def __init__(self, client: Client) -> None:
        Tk.__init__(self)
        self.__fen_authentification: Frame
        self.__lbl_err: Label
        self.__lbl_login: Label
        self.__entree_login: Entry
        self.__lbl_mdp: Label
        self.__entree_mdp: Entry
        self.__btn_authentification: Button
        self.__btn_quitter: Button

        self.__fen_authentification = Frame(self, borderwidth=10, relief="groove", padx=10, pady=10)
        self.__lbl_err = Label(self.__fen_authentification, borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__lbl_login = Label(self.__fen_authentification, text="Login :", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_login = Entry(self.__fen_authentification, width=30)
        self.__lbl_mdp = Label(self.__fen_authentification, text="Mot de passe :", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_mdp = Entry(self.__fen_authentification, width=30, show='*')
        self.__btn_authentification = Button(self.__fen_authentification, text="Authentification", font=(Main_IHM.POLICE,Main_IHM.TAILLE_POLICE), bg="grey", command=self.authentification)
        self.__btn_quitter = Button(self.__fen_authentification, text = "Quitter", font= (Main_IHM.POLICE,Main_IHM.TAILLE_POLICE), bg="red", command=self.destroy)

        self.__fen_authentification.pack()
        self.__lbl_login.grid(row=1, column=0)
        self.__entree_login.grid(row=1, column=1)
        self.__lbl_mdp.grid(row=2, column=0)
        self.__entree_mdp.grid(row=2, column=1)
        self.__btn_authentification.grid(row=3, column=1)
        self.__btn_quitter.grid(row=3, column=2)

        self.__ip_serveur: str
        self.__port_serveur: int
        self.__client: Client = client

    def get_client(self) -> Client:
        return self.__client
    
    def authentification(self) -> None:
        try:
            erreur: bool = False
            login: str = self.__entree_login.get()
            passwd: str = hashlib.sha256((self.__entree_mdp.get()).encode("utf-8")).hexdigest()
            if login == "" or passwd == "":
                raise ErrEMPTY
            msg_serveur = self.__client.authentification(login=login, passwd=passwd)
            if msg_serveur.split()[1].lower() == "refused":
                raise ErrREFUSED
        except ErrEMPTY as e:
            erreur = True
            text = f"Erreur 'EMPTY' : {e}"
            color = "red"
        except ErrREFUSED as e:
            erreur = True
            text = f"Erreur 'REFUSED' : {e}"
            color = "red"
        except Exception as e:
            print(e)
        finally:
            if erreur:
                self.__lbl_err.configure(text=text, background=color)
                self.__lbl_err.grid(row=0, column=1)
            else:
                self.destroy()

class Mouvement(Tk):
    def __init__(self, client: Client) -> None:
        Tk.__init__(self)
        self.__fen_mouvement: Frame
        self.__btn_quitter: Button
        self.__lbl_joystick_status: Label
        self.__client: Client

        self.__fen_mouvement = Frame(self, borderwidth=10, relief="groove", padx=10, pady=10)
        self.__lbl_joystick_status = Label(self.__fen_mouvement, text="[-] Pas de joystick connecté.", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__btn_quitter = Button(self.__fen_mouvement, text = "Quitter", font= (Main_IHM.POLICE,Main_IHM.TAILLE_POLICE), bg="red", command=self.destroy)
        self.__text = Text(self.__fen_mouvement, width=40, height=10)

        self.__fen_mouvement.pack()
        self.__btn_quitter.grid(row=1, column=0)
        self.__lbl_joystick_status.grid(row=2, column=0)
        self.__text.grid(row=3, column=0)

        self.__client = client

        if self.__client.get_joystick().is_connected():
            self.__lbl_joystick_status.configure(text=f"[+] Joystick connecté : {self.__client.get_joystick().get_name()}")

    def get_client(self) -> Client:
        return self.__client
    
    def mouvement(self) -> None:
        if self.__client.get_joystick().is_connected():
            try:
                self.__client.get_joystick().mainloop(self.__socket)
            except KeyboardInterrupt as e:
                print(e)
            finally:
                self.__client.get_joystick().quit()
        self.quitter()


if __name__=="__main__":
    main_ihm : Main_IHM
    main_ihm = Main_IHM()
    main_ihm.main()