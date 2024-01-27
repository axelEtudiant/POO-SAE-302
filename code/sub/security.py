from typing import List
import getmac
"""

Contient toutes les classes relatives à la sécurité client/serveur.

"""

class MacFilter:
    """Class MacFilter for filtering MAC addresses connecting to the robot.
    """
    # Global variable: list of valid MAC addresses
    MAC_LIST: List = [
        "d4:d8:53:c4:f0:bd",
        "4c:d5:77:cc:22:a7"
    ]

    def __init__(self) -> None:
        """Constructor for the MacFilter class.
        """
        self.__ip: str
        self.__mac_address: str

    def filter(self, ip: str) -> bool:
        """Method of the MacFilter class that retrieves the client's MAC address, tests if it matches the allowed MAC addresses, and returns the result.

        Args:
            ip (str): IP address of the client machine.

        Returns:
            bool: Filtering result, True if the client is allowed, False otherwise.
        """
        # Initialization
        self.__ip = ip  # Client's IP address
        result: bool = False

        # Retrieving the client's MAC address using getmac
        try:
            self.__mac_address = getmac.get_mac_address(ip=self.__ip)
        except getmac.GetMacError:
            return False  # Unable to retrieve MAC address, reject the client

        if self.__mac_address in MacFilter.MAC_LIST:
            result = True
        else:
            result = False

        return result
     