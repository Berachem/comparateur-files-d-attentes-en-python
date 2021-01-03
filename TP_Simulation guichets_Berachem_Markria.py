# Créé par Berachem, le 11/12/2020 en Python 3.7
from queue import Queue
from random import randint


class Client :
    def __init__(self, temps):
        """
        Méthode qui crée un client caractérisé par son temps d'arrivé
        """
        self.temps_initial = temps

class Guichet:
    def __init__(self):
        """
        Crée un guichet
        """
        self.temps_indispo = 0
        self.client = 0
        #Chaque guichet aura une file pour la strat 1 et 2
        self.file = Queue()

    def estDispo(self):
        """
        Renvoie True si le guichet est Dispo sinon renvoie False
        """
        return self.temps_indispo==0

class Strat3:

    def __init__(self, nb_guichets, nb_tours_horloge):
        """
        Crée un environnement pour cette stratégie :
        Une seule file pour tous les guichets
        """
        self.horloge = 0
        self.nb_tours_horloge = nb_tours_horloge
        #Je crée un tableau de nb_guichets case qui sont tous des instance de la classe Guichet
        self.dispo = [Guichet() for _ in range(nb_guichets)]
        self.file = Queue()
        self.nb_client_total = 0
        self.temps_attente_total = 0

    def moyenne_attente(self):
        """
        Renvoie la moyenne d'attente par client
        """
        return self.temps_attente_total / self.nb_client_total

    def simuler(self):
        """
        Fais tourner la simulation pour nb_tours_horloge cette stratéfie et affiche
        la moyenne attendu pour chaque client
        """
        while self.horloge < self.nb_tours_horloge:
            self.file.put(Client(self.horloge))
            for g in self.dispo:
                if g.estDispo() and not self.file.empty():
                    self.nb_client_total+=1
                    # On met le client suivant à ce guichet et on dit
                    # aléatoirement cb de temps le guichet sera occupé
                    g.client = self.file.get()
                    self.temps_attente_total += self.horloge - g.client.temps_initial
                    g.temps_indispo = randint(0,len(self.dispo))
                elif g.temps_indispo > 0:
                    g.temps_indispo -= 1
            self.horloge+=1

        print("================Strat 3================")
        print("Stratégie où il y a une seule file pour tous les guichets.")
        print("Il y a eu  " , self.moyenne_attente(), " d'attente en moyenne par client.")

class Strat2:

    def __init__(self, nb_guichets, nb_tours_horloge):
        """
        Crée un environnement pour cette stratégie :
        Une file par guichet guichets et le nouvel arriant va dans une file au hasard
        """
        self.horloge = 0
        self.nb_tours_horloge = nb_tours_horloge
        #Je crée un tableau de nb_guichets case qui sont tous des instance de la classe Guichet
        self.dispo = [Guichet() for _ in range(nb_guichets)]
        self.nb_client_total = 0
        self.temps_attente_total = 0

    def moyenne_attente(self):
        """
        Renvoie la moyenne d'attente par client
        """
        return self.temps_attente_total / self.nb_client_total

    def simuler(self):
        """
        Fais tourner la simulation pour nb_tours_horloge cette stratéfie et affiche
        la moyenne attendu pour chaque client
        """
        while self.horloge < self.nb_tours_horloge:
            self.dispo[randint(0,len(self.dispo)-1)].file.put(Client(self.horloge))
            for g in self.dispo:
                if g.estDispo() and not g.file.empty():
                    self.nb_client_total+=1
                    # On met le client suivant à ce guichet et on dit
                    # aléatoirement cb de temps le guichet sera occupé
                    g.client = g.file.get()
                    self.temps_attente_total += self.horloge - g.client.temps_initial
                    g.temps_indispo = randint(0,len(self.dispo))
                elif g.temps_indispo > 0:
                    g.temps_indispo -= 1
            self.horloge+=1


        print("================Strat 2================")
        print("Stratégie où il y a une file par guichet et le client va dans une file aléatoire.")
        print("Il y a eu  " , self.moyenne_attente(), " d'attente en moyenne par client.")

class Strat1:
    def __init__(self, nb_guichets, nb_tours_horloge):
        """
        Crée un environnement pour cette stratégie :
        Une file par guichet guichets et le nouvel arriant va dans la file la moins remplie
        """
        self.horloge = 0
        self.nb_tours_horloge = nb_tours_horloge
        #Je crée un tableau de nb_guichets case qui sont tous des instance de la classe Guichet
        self.dispo = [Guichet() for _ in range(nb_guichets)]
        self.nb_client_total = 0
        self.temps_attente_total = 0

    def file_la_moins_remplie(self):
        """
        Renvoie la file qui possède le moins d'éléments (de clients)
        """
        file = self.dispo[0].file
        for g in self.dispo:
            if file.qsize() > g.file.qsize():
                file = g.file
        return file

    def moyenne_attente(self):
        """
        Renvoie la moyenne d'attente par client
        """
        return self.temps_attente_total / self.nb_client_total

    def simuler(self):
        """
        Fais tourner la simulation pour nb_tours_horloge cette stratéfie et affiche
        la moyenne attendu pour chaque client
        """
        while self.horloge < self.nb_tours_horloge:
            self.file_la_moins_remplie().put(Client(self.horloge))
            for g in self.dispo:
                if g.estDispo() and not g.file.empty():
                    self.nb_client_total+=1
                    # On met le client suivant à ce guichet et on dit
                    # aléatoirement cb de temps le guichet sera occupé
                    g.client = g.file.get()
                    self.temps_attente_total += self.horloge - g.client.temps_initial
                    g.temps_indispo = randint(0,len(self.dispo))
                elif g.temps_indispo > 0:
                    g.temps_indispo -= 1
            self.horloge+=1


        print("================Strat 1================")
        print("Stratégie où il y a une file par guichet et le client va dans la file la moins remplie.")
        print("Il y a eu  " , self.moyenne_attente(), " d'attente en moyenne par client.")



strat1 = Strat1(5,100000)
strat1.simuler()
strat2 = Strat2(5,100000)
strat2.simuler()
strat3 = Strat3(5,100000)
strat3.simuler()


