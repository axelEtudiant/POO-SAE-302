#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import string, random, os
from client import *
from typing import List
from tkinter import *
from sub.exception import *


class Connexion(Tk):
    POLICE: str = "times"
    TAILLE_POLICE: int = 12

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
        self.__lbl_ip_serveur = Label(self.__fen_connexion, text="IP du serveur : ", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_ip_serveur = Entry(self.__fen_connexion, width=30)
        self.__lbl_port_serveur = Label(self.__fen_connexion, text="Port du serveur : ", borderwidth=5, relief="ridge", padx=5, pady=5)
        self.__entree_port_serveur = Entry(self.__fen_connexion, width=30)
        self.__btn_connexion = Button(self.__fen_connexion, text="Connexion", font=(Connexion.POLICE,Connexion.TAILLE_POLICE), bg="grey", command=self.connexion)
        self.__btn_quitter = Button(self.__fen_connexion, text = "Quitter", font= (Connexion.POLICE,Connexion.TAILLE_POLICE), bg="red", command=self.destroy)

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

if __name__=="__main__":
    ihm: Connexion
    ihm = Connexion()
    ihm.mainloop()