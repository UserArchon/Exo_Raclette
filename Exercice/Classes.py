from random import randint
from Fonctions import devenir_hostile


class De:
    def __init__(self, nb_faces):
        self.nb_faces = nb_faces

    def lancer_de(self) -> int:
        de = randint(1, self.nb_faces)
        return de


class Personnage:
    def __init__(self, nom, stats):
        self.nom = nom
        self.force = stats["force"]
        self.intelligence = stats["intelligence"]
        self.dexterite = stats["dexterite"]
        self.classe_d_armure = stats["CA"]
        self.pv = 100
        self.xp = 100
        self.niveau = 1
        self.de_perso = De(20)
        self.en_vie = True
        self.rival = []
        self.sorts_connus = {}
        self.etat_du_perso = {}

    # def upgrade(self):
    #     if self.xp >= 200:  # TODO remettre les niveaux en place
    #         self.niveau += 1
    #         self.passer_un_niveau()
    #         self.xp = 0
    #         print(self.nom, "passe au niveau ", self.niveau)
    #
    # def passer_un_niveau(self):
    #     if self.niveau == 2:
    #         self.sorts_connus.update(Sort_damage("Mains Brulantes"))
    #         print("\nVous Obtenez le sort Mains Brulantes et 20 de force en plus\n")
    #         self.force += 20
    #     if self.niveau == 3:
    #         self.sorts_connus.append(Sort_shield("Shield"))
    #         print("\nVous Obtenez le sort Protection et 30 de force en plus\n")
    #         self.force += 30
    #     if self.niveau == 4:
    #         self.force += 40

    def attaquer(self, cible):
        """Si dexterite de l'attaquant superieur a la classe d'armure de l'attaqué :
        degats de force dans pv cible"""
        touche = False
        self.dexterite = self.de_perso.lancer_de()
        devenir_hostile(self, cible)
        devenir_hostile(cible, self)

        if self.dexterite + 5 > cible.classe_d_armure:
            cible.prendre_degats(self.force)
            touche = True
        if self.pv > 0:
            print(
                f"{self.nom} ({self.pv} pv) attaque {cible.nom} de {self.force} pts : {'Touche' if touche else 'Loupe'}"
            )

    def prendre_degats(self, degats):
        self.pv -= degats
        if self.pv <= 0:
            self.en_vie = False


class Sort:
    def __init__(self, nom):
        self.nom = nom
        self.cooldown = 0
        self.sort_parti = True
        self.CA_de_base = 0
        self.action = ""

    def lancer(self, sort, lanceur, cible):

        if self.cooldown > 0:
            print(f"Reste {self.cooldown} tour avant de pouvoir le lancer\n")

        if self.cooldown <= 0:
            print(lanceur.nom, self.action, self.nom)
            for categorie_sort in dict_categorie_sort.keys():
                if sort.attributs == categorie_sort:  # sort.attribut donne l'attribut du sort lancé : "Heal"
                    sort.effet(lanceur, cible)

    def reset_sort(self):
        self.cooldown = 3


class Sort_shield(Sort):
    def __init__(self, nom):
        super().__init__(self)
        self.action = " se protege "
        self.nom = nom
        self.attributs = "Protection"

    def effet(self, lanceur, cible):
        lanceur.CA_de_base = lanceur.classe_d_armure
        lanceur.classe_d_armure += 10  # donne une protection temporaire
        print(f"{lanceur.classe_d_armure} de Classe d'Armure")
        if not self.nom in lanceur.etat_du_perso:
            lanceur.etat_du_perso.update({self.nom: 3})
        # print(self.nom)
        self.reset_sort()


class Sort_damage(Sort):
    def __init__(self, nom):
        super().__init__(self)
        self.nom = nom
        self.action = " lance le sort : "
        self.attributs = "Damage"

    def effet(self, lanceur, cible):
        degats = lanceur.de_perso.lancer_de() + lanceur.force
        print("Il inflige ", degats, " pts")  # DAMAGE : Mains Brulantes
        cible.prendre_degats(degats)
        self.reset_sort()
        self.cooldown += 2


class Sort_heal(Sort):
    def __init__(self, nom):
        super().__init__(self)
        self.action = " se regenere : "
        self.nom = nom
        self.attributs = "Heal"

    def effet(self, lanceur, cible):
        lanceur.pv += lanceur.de_perso.lancer_de() + lanceur.intelligence
        self.reset_sort()


# dico_sort = {"Protection": [Sort_shield("Shield")],
#              "Heal": [Sort_heal("Soin")],
#              "Damage": [Sort_damage("Mains Brulantes")]}

dict_categorie_sort = {"Heal": Sort_heal("Soin"), "Damage": Sort_damage("Mains Brûlantes"),
                       "Protection": Sort_shield("Shield")}
