import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image


class PageBase(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__liste_input: list = []
        self.__valeur_direct: int = 0
        
        #Page Menu
        # Création des pages
        self.page1 = Screen(name='page1')
        self.page2 = Screen(name='page2')
        self.page3 = Screen(name='page3')
        self.page4 = Screen(name='page4')


        # Page Menu vers Page 2
        label1 = Label(text="Ceci est la page 1")
        button_to_page2 = Button(text="Controle du robot", size_hint=(0.3, 0.1), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.65})
        button_to_page2.bind(on_release=self.show_page2)


        button_to_page1 = Button(text="Aller à la page 2", size_hint=(0.3, 0.1), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5})
        button_to_page1.bind(on_release=self.show_page3)

        button_to_page3 = Button(text="Aller à la page 3", size_hint=(0.3, 0.1), 
                                 pos_hint={'center_x': 0.5, 'center_y': 0.35})
        button_to_page3.bind(on_release=self.show_page4)



        self.page1.add_widget(label1)
        self.page1.add_widget(button_to_page1)
        self.page1.add_widget(button_to_page2)
        self.page1.add_widget(button_to_page3)

        #position boutons: 



        # PAGE 2 controle du robot
        # Charger l'image en tant qu'arrière-plan
        arriere_plan2 = Image(source='oscar.png')
        self.page2.add_widget(arriere_plan2)
        self.page2.bouton_retour_direct = Button(text='Retour Direct', size_hint=(None, None), size=(120, 50))
        self.page2.bouton_retour_arriere = Button(text='Retour Arrière', size_hint=(None, None), size=(120, 50))
        self.page2.bouton3 = Button(text='[size=30]v[/size]', markup=True, size_hint=(None, None), size=(50, 50))
        self.page2.bouton4 = Button(text='[size=40]^[/size]', markup=True, size_hint=(None, None), size=(50, 50))
        self.page2.bouton5 = Button(text='[size=30]<[/size]', markup=True, size_hint=(None, None), size=(50, 50))
        self.page2.bouton6 = Button(text='[size=40]>[/size]', markup=True, size_hint=(None, None), size=(50, 50))

        label2 = Label(text="bienvenue sur la page controle du robot")
        button_to_page1 = Button(text="Menu", size_hint=(0.11, 0.07), 
                                 pos_hint={'center_x': 0.08, 'center_y': 0.95})
        button_to_page1.bind(on_release=self.show_page1)


        self.page2.add_widget(label2)
        self.page2.add_widget(button_to_page1)
        self.page2.add_widget(self.page2.bouton_retour_direct)
        self.page2.add_widget(self.page2.bouton_retour_arriere)
        self.page2.add_widget(self.page2.bouton3)
        self.page2.add_widget(self.page2.bouton4)
        self.page2.add_widget(self.page2.bouton5)
        self.page2.add_widget(self.page2.bouton6)

        #image rond direction
        image_rond = Image(source='rond.png')
        self.page2.add_widget(image_rond)


        # bouton retour direct
        self.page2.bouton_retour_direct.pos_hint = {'center_x': 0.15, 'center_y': 0.125}
        # bouton retour arriere
        self.page2.bouton_retour_arriere.pos_hint = {'center_x': 0.85, 'center_y': 0.125}
        # bouton avancer
        self.page2.bouton3.pos_hint = {'center_x': 0.5, 'center_y': 0.08}
        # bouton reculer
        self.page2.bouton4.pos_hint = {'center_x': 0.5, 'center_y': 0.18}
        # bouton gauche
        self.page2.bouton5.pos_hint = {'center_x': 0.42, 'center_y': 0.13}
        # bouton droite
        self.page2.bouton6.pos_hint = {'center_x': 0.58, 'center_y': 0.13}
        #image rond
        image_rond.pos_hint = {'center_x': 0.5, 'center_y': 0.132}

        # Connecter les méthodes aux événements des boutons
        self.page2.bouton3.bind(on_press=self.bouton_appuye)
        self.page2.bouton3.bind(on_release=self.bouton_relache)
        self.page2.bouton4.bind(on_press=self.bouton_appuye)
        self.page2.bouton4.bind(on_release=self.bouton_relache)
        self.page2.bouton5.bind(on_press=self.bouton_appuye)
        self.page2.bouton5.bind(on_release=self.bouton_relache)
        self.page2.bouton6.bind(on_press=self.bouton_appuye)
        self.page2.bouton6.bind(on_release=self.bouton_relache)
        self.page2.bouton_retour_direct.bind(on_release=self.direct)
        self.page2.bouton_retour_arriere.bind(on_release=self.liste_retour)




        # PAGE 3
        # Charger l'image en tant qu'arrière-plan
        arriere_plan3 = Image(source='oscar.png')
        self.page3.add_widget(arriere_plan3)

        label3 = Label(text="Ceci est la page 3")
        button_to_page1 = Button(text="Menu", size_hint=(0.11, 0.07), 
                                 pos_hint={'center_x': 0.08, 'center_y': 0.95})
        button_to_page1.bind(on_release=self.show_page1)

        self.page3.add_widget(label3)
        self.page3.add_widget(button_to_page1)


        # PAGE 4
        # Charger l'image en tant qu'arrière-plan
        arriere_plan4 = Image(source='oscar.png')
        self.page4.add_widget(arriere_plan4)

        label4 = Label(text="Ceci est la page 4")
        button_to_page1 = Button(text="Menu", size_hint=(0.11, 0.07), 
                                 pos_hint={'center_x': 0.08, 'center_y': 0.95})
        button_to_page1.bind(on_release=self.show_page1)

        self.page4.add_widget(label4)
        self.page4.add_widget(button_to_page1)

        # ajout des pages
        self.add_widget(self.page1)
        self.add_widget(self.page2)
        self.add_widget(self.page3)
        self.add_widget(self.page4)

        self.current = 'page1'

    def show_page1(self, *args):
        self.current = 'page1'

    def show_page2(self, *args):
        self.current = 'page2'

    def show_page3(self, *args):
        self.current = 'page3'

    def show_page4(self, *args):
        self.current = 'page4'

    def bouton_appuye(self, instance):
        if instance.text == '[size=30]v[/size]':
            self.__liste_input.append(-1)
            print("-1")  # "-1" lorsque le bouton3 est appuyé
        elif instance.text == '[size=40]^[/size]':
            self.__liste_input.append(1)
            print("1")  # "1" lorsque le bouton4 est appuyé
        elif instance.text == '[size=30]<[/size]':
            self.__liste_input.append(-2)
            print("-2")  # "-2" lorsque le bouton5 est appuyé
        elif instance.text == '[size=40]>[/size]':
            self.__liste_input.append(2)
            print("2")  # "2" lorsque le bouton6 est appuyé

    def bouton_relache(self, instance):
        print("0")  # "0" lorsque le bouton est relâché

    def liste_retour(self, temp):
        self.__liste_input.reverse()
        liste_inversee = self.__liste_input[:]
        self.__liste_input = []
        print(liste_inversee)
        return liste_inversee

    def direct(self, temp):
        for element in self.__liste_input:
            self.__valeur_direct += element
        print(self.__valeur_direct)
        self.__valeur_direct = 0
        self.__liste_input = []

class MyApp(App):
    def build(self):
        # Définir la taille de la fenêtre (largeur, hauteur) en utilisant Window
        Window.size = (400, 600)
        # Changer le nom de la fenêtre
        self.title = 'Oscar Beaupel le don Juan'
        return PageBase()

if __name__ == '__main__':
    MyApp().run()
