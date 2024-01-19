# SAE 302 ROBOTO

- 

**INFO MODULE COMPLEMENTAIRE (hors module déjà présent avec python)**

- Scapy


## Etat du programme

- Connection avec identification pour un client
- Gestion des logs et utilisateurs
-

### TO DO

- [ ] Ajout des logs pour les erreurs des requêtes vers la base de données [requests.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/sub/requests.py)
- [X] Ajout de la gestion de plusieurs clients à la fois (Thread) [serveur.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/serveur.py)
- [ ] Ajout de l'interface
    - [ ] Page d'authentification
    - [ ] Page info robot
    - [ ] Page controle robot
    - [ ] Page log/admin
- [ ] Commencer à réfléchir sur les classes pour les contrôles du robot
- [X] Configuration du hotspot sur le robot
    - [X] Nom du hostpot : APRobot6
    - [X] @Ip : 10.3.141.1
    - [X] Mdp : password123456789!
- [ ] Gérer le faite d'avoir qu'un seul utilisateur de login. Les nouvelles connexions verront un message pour les prévenir qu'une connexion est déjà en cours 
    - [X] Rajouter le message de connexion occupée
    - [X] Séparer l'écoute sur le port et la connexion au port
    - [ ] Déplacer le filtrage d'adresse M@C dans la classe [ServeurEcoute](https://github.com/SpiizN/POO-SAE-302/tree/main/code/serveur.py)
    - [ ] Ajouter la gestion du message "CONN OCCUPIED" coté [client.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/client.py)
- [ ] Ajouter la fermeture propre de la connexion tcp coté [client.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/client.py) et [serveur.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/serveur.py)
- [ ] Mettre au propre la boucle while du main de [serveur.py](https://github.com/SpiizN/POO-SAE-302/tree/main/code/serveur.py)


INTERFACE GRAPHIQUE :

- [ ] boutons :
    - [ ] avancer
    - [ ] reculer
    - [ ] tourner à droite (power sur la roue gauche)
    - [ ] tourner à gauche (power sur la roue droite)
    - [ ] retour arrière (rebrousse chemin)
    - [ ] retour direct
          
- [ ] menu déroulant :
    - [ ] page infos sur le robot
    - [ ] page controle robot
    - [ ] page log/admin si le login est correct
     
- [ ] cartographie :
    - [ ] afficher la carte
    - [ ] afficher les obstacles
    - [ ] afficher le robot
    - [ ] afficher le chemin parcouru 
          
