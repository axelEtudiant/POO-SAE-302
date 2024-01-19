# -*- coding : utf8 -*-
from scapy.all import ARP, Ether, srp
from typing import List
"""

Contient toutes les classes relatives à la sécurité client/serveur.

"""

class MacFilter:
    """Classe MacFilter pour filtrer les adresses mac qui se connectent au robot.
    """
    # Variable gloable: list des adresses MAC valides
    MAC_LIST: List = [
        "d4:d8:53:c4:f0:bd",
        "4c:d5:77:cc:22:a7"
    ]

    def __init__(self) -> None:
        """Constructeur de la classe MacFilter
        """
        self.__ip: str
        self.__mac_address: str

    def filter(self, ip: int) -> bool:
        """Méthode de la classe MacFilter qui retrouve l'adresse MAC du client, test si elle correspond à celle autorisé et renvoie le résultat.

        Args:
            ip (int): Adresse ip de la machine cliente

        Returns:
            bool: Résultat du filtrage True si le client est autorisé, False sinon
        """
        # Initialisation
        self.__ip = ip # Adresse ip du client
        resultat: bool = False

        # Récupération de l'adresse MAC du client
        arp_request = ARP(pdst=self.__ip) # -> Préparation requête ARP
        eth_request = Ether(dst="ff:ff:ff:ff:ff:ff") # -> Préparation requête ethernet
        packet = eth_request/arp_request # -> Préparation du paquet final
        result = srp(packet, timeout=3, verbose=0)[0] # -> Récupération du résultat
        self.__mac_address = result[0][1].hwsrc # -> Récupération de l'adresse MAC dans la trame

        if self.__mac_address in MacFilter.MAC_LIST: # Si l'adresse MAC du client est dans la liste autorisé alors le résultat est bon
            resultat = True
        else: # Sinon on le refuse
            resultat = False

        return resultat
