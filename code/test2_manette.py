import pygame
import math

pygame.init()

# Initialisation de la manette
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("Aucune manette détectée.")
    quit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
boutons: dict = {}
boutons_old: dict = {}

print(f"Manette détectée: {joystick.get_name()}")

try:
    while True:
        # Lecture des boutons
        for i in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(i)
            boutons[f"Bouton{i}"] = f"{button_state}"

        pygame.event.pump()  # Met à jour les événements de la fenêtre

        # Lecture de l'axe horizontal (stick analogique gauche)
        x_axis = joystick.get_axis(0)
        y_axis = joystick.get_axis(1)

        # Calcul de l'angle en radians
        angle_rad = math.atan2(y_axis, x_axis)

        # Conversion de l'angle en degrés
        angle_deg = math.degrees(angle_rad)

        # Soustraction de 90
        angle_deg = math.degrees(angle_rad) + 90

        # Centre = 0
        # Gauche = -90
        # Droite = +90

        if boutons != boutons_old:
            if boutons_old == {}:
                pass
            else:
                if boutons_old["Bouton0"] != boutons["Bouton0"]:
                    val = boutons.get("Bouton0")
                    if int(val) == 0:
                        angle_deg = ""

                    print(f"MVMT {val} {angle_deg}")

        boutons_old = boutons
        boutons = {}

        #print(f"Inclinaison du stick: {angle_deg:.2f} degrés")

except KeyboardInterrupt:
    print("Script interrompu par l'utilisateur.")

finally:
    joystick.quit()
    pygame.quit()