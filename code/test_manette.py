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

print(f"Manette détectée: {joystick.get_name()}")


text: str = ''
ancien_text: str = ''

try:
    while True:
        pygame.event.pump()  # Met à jour les événements de la fenêtre

        # Lecture des axes
        for i in range(joystick.get_numaxes()):
            axis_value = joystick.get_axis(i)
            text += f"Axe {i}: {axis_value}\n"

        # Lecture des boutons
        for i in range(joystick.get_numbuttons()):
            button_state = joystick.get_button(i)
            text += f"Bouton {i}: {button_state}\n"

        # Lecture des chapeaux (hats)
        for i in range(joystick.get_numhats()):
            hat_state = joystick.get_hat(i)
            text += f"Chapeau {i}: {hat_state}\n"

        if text != ancien_text:
            print("Changements d'état.")
            print(text)

        ancien_text = text
        text = ''



except KeyboardInterrupt:
    print("Script interrompu par l'utilisateur.")

finally:
    joystick.quit()
    pygame.quit()
