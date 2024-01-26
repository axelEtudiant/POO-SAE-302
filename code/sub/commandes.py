# -*- coding : utf8 -*-
import RPi.GPIO as GPIO
import time

class Commandes:
    
    def __init__(self) -> None:
        """Constructeur de la classe Commandes
        """
        # Définir les broches GPIO
        # Roue droite
        self.__droite_vitesse = 18  # Broche pour la vitesse IO1
        self.__droite_sens = 27  # Broche pour le sens IO2
        
        # Roue Gauche 
        self.__gauche_vitesse = 23 # Broche pour la vitesse IO3
        self.__gauche_sens = 22 # Broche pour le sens IO4

        # Configurer le mode de numérotation des broches
        GPIO.setmode(GPIO.BCM)

        # Configurer les broches en sortie
        GPIO.setup(self.__droite_vitesse, GPIO.OUT)
        GPIO.setup(self.__droite_sens, GPIO.OUT)
        GPIO.setup(self.__gauche_vitesse, GPIO.OUT)
        GPIO.setup(self.__gauche_sens, GPIO.OUT)


    def mouvement(self, direction: str, temps: int, pourcentage: int) -> None:
        """Méthode de la classe Commandes qui permet de bouger le robot en fonction des paramètres suivants:
        
        Args:
            time (int): temps pendant lequelle le robot effectue le mouvement
            pourcentage (int): Effet sur la vitesse
        """
        mvt_moteur = {"avancer": [1,1], "reculer": [0,0]}
        # Affectation du sens
        GPIO.output(self.__gauche_sens, mvt_moteur[direction][0])
        GPIO.output(self.__droite_sens, mvt_moteur[direction][1])  

        pwm_gauche = GPIO.PWM(self.__gauche_vitesse, 50)
        pwm_droite = GPIO.PWM(self.__droite_vitesse, 50)
        pwm_gauche.start(pourcentage + (pourcentage*(1/7))) 
        pwm_droite.start(pourcentage) # boost le pourcentage d'un des moteurs pour contrer son manque de puissance 
        
        time.sleep(temps)

        pwm_gauche.stop()
        pwm_droite.stop()
        GPIO.output(self.__gauche_sens, GPIO.LOW)
        GPIO.output(self.__droite_sens, GPIO.LOW)

    def tourner(self, angle: float, pourcentage: int) -> None:
        """Méthode de la classe Commandes qui permet de tourner le robot d'un certain angle.

        Args:
            angle (float): Angle de rotation en degrés (-180 à 180, positif pour tourner à droite, négatif pour tourner à gauche).
            temps (int): Temps pendant lequel le robot effectue le mouvement.
            freq (int): Fréquence PWM pour les moteurs.
            pourcentage (int): Vitesse des moteurs en pourcentage.
        """
        mvt_moteur = {"gauche": [1,0], "droite": [0,1]}
        # Affectation du sens
        direction = "droite"
        if (angle > -180) and (angle < 0):
            direction = "gauche"


        GPIO.output(self.__gauche_sens, mvt_moteur[direction][0])
        GPIO.output(self.__droite_sens, mvt_moteur[direction][1]) 

        pwm_gauche = GPIO.PWM(self.__gauche_vitesse, 50)
        pwm_droite = GPIO.PWM(self.__droite_vitesse, 50)

        pwm_gauche.start(pourcentage + (pourcentage*(1/7)))
        pwm_droite.start(pourcentage)

        tmp_rotation = abs(angle) / 180
        print(tmp_rotation)
        time.sleep(tmp_rotation*(8/10))
        
        pwm_gauche.ChangeDutyCycle(pourcentage*0.3)
        pwm_droite.ChangeDutyCycle(pourcentage*0.3)
        time.sleep(tmp_rotation*(2/10))


        pwm_gauche.stop()
        pwm_droite.stop()
        GPIO.output(self.__gauche_sens, GPIO.LOW)
        GPIO.output(self.__droite_sens, GPIO.LOW)

    def clean(self) -> None:
        """Méthode de la classe Commandes qui permet d'arreter correctement les moteurs
        """
        GPIO.cleanup()
"""
commande: Commandes = Commandes()

fin = True
while fin:
    cmd = input("Commande : ")
    try:
        if cmd.startswith("tourner "):
            angle = float(cmd.split()[1])
            commande.tourner(angle, 3, 50, 40)
        else:
            commande.mouvement(cmd, 3, 50, 80)
    except Exception as e:
        print(f"Erreur: {e}")
        fin = False
"""
