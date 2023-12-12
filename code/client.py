import socket
import json

def get_query(dict_query: dict) -> str:
    return json.loads(dict_query)["q"]

if __name__=="__main__":
    # Déclaration des variables
    ip_serveur: str
    port_serveur: int
    socket_echange: socket
    msg: str
    msg_serveur: str
    tab_bytes: bytes

    # Initialisation
    ip_serveur = "localhost"
    port_serveur = 5001

    # Création de la socket d'échhange
    socket_echange = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Tentative de connexion au serveur
    socket_echange.connect((ip_serveur, port_serveur))

    # Filtrage MAC
    msg_serveur = get_query(socket_echange.recv(1024).decode("utf-8"))
    print(msg_serveur)

    if msg_serveur.split()[1].lower() == "accepted":
        # Demande du user
        msg_serveur = get_query(socket_echange.recv(1024).decode("utf-8"))
        print(msg_serveur)

        # Envoi du user
        socket_echange.send(json.dumps({"q": f"CONN USER {input("Votre user: ")}"}).encode("utf-8"))

        # Demande du password
        msg_serveur = get_query(socket_echange.recv(1024).decode("utf-8"))
        print(msg_serveur)

        # Envoi du password
        socket_echange.send(json.dumps({"q": f"CONN PASSWORD {input("Votre user: ")}"}).encode("utf-8"))

        # CONNEXION ETABLIE
        msg_serveur = get_query(socket_echange.recv(1024).decode("utf-8"))
        print(msg_serveur)

    socket_echange.close()