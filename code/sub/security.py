"""

Contient toutes les classes relatives à la sécurité client/serveur.


"""


from scapy.all import ARP, Ether, srp
from typing import List


# Classe pour filtrer les adresses mac qui se connectent au robot.
class MacFilter:
    # Variable gloable: list des adresses MAC valides
    MAC_LIST: List = [
        "d4:d8:53:c4:f0:bd"
    ]

    def __init__(self) -> None:
        self.ip: str
        self.__mac_address: str

    def filter(self, ip: int):
        self.__ip = ip
        resultat: bool = False

        arp_request = ARP(pdst=self.__ip) # -> Préparation requête ARP
        eth_request = Ether(dst="ff:ff:ff:ff:ff:ff") # -> Préparation requête ethernet
        packet = eth_request/arp_request # -> Préparation du paquet final
        result = srp(packet, timeout=3, verbose=0)[0] # -> Récupération du résultat
        self.__mac_address = result[0][1].hwsrc # -> Récupération de l'adresse MAC dans la trame

        if self.__mac_address in MacFilter.MAC_LIST:
            resultat = True
        else:
            resultat = False

        return resultat
