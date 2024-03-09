from random import randint


class De:
    def __init__(self, nb_faces):
        self.nb_faces = nb_faces

    def lancer_de(self) -> int:
        de = randint(1, self.nb_faces)
        return de


dico_des_niveaux = {"1": {"sorts": ["Soin"], "pv": 10, "force": 10, "prochain_niveau": 100},
                    "2": {"sorts": ["Mains Brulantes"], "pv": 20, "dexterite": 5, "prochain_niveau": 300},
                    "3": {"sorts": ["Shield"], "pv": 20, "dexterite": 5, "prochain_niveau": 600},
                    "4": {"sorts": ["Feu"], "pv": 20, "force": 20, "prochain_niveau": 900},
                    "5": {"sorts": ["Glace"], "pv": 20, "dexterite": 15, "prochain_niveau": 1200},
                    "6": {"sorts": ["Toucher"], "pv": 20, "force": 40, "prochain_niveau": 2400},
                    "7": {"sorts": ["Barriere"], "pv": 20, "dexterite": 25, "prochain_niveau": 3600},
                    "8": {"sorts": ["Appel de la lumière"], "pv": 20, "force": 50, "prochain_niveau": 7000}}


class Personnage:
    def __init__(self, nom, stats):
        self.nom = nom
        self.force = stats["force"]
        self.intelligence = stats["intelligence"]
        self.dexterite = stats["dexterite"]
        self.classe_d_armure = stats["CA"]
        self.pv = 100
        self.xp = 100
        self.niveau = 3
        self.de_perso = De(20)
        self.en_vie = True
        self.rival = []
        self.sorts_connus = {}
        self.etat_du_perso = {}
        self.prochain_niveau = 0  # xp
        self.niveau_passe = []

    def ajouter_sort_perso(self, liste_nom_sort: list):  # liste en string
        """
        :param liste_nom_sort: list of str ["Soin","Invocation"] de sorts
        """
        liste_a_injecter = []
        for sort_du_perso in liste_nom_sort:  # Pour chaque sort donné au perso ########################## nom_attributs : (list)sort_du_dico
            for nom_attributs, sorts_du_dico in dico_sort.items():  # Pour chaque cle, valeur dans le dico {"Protection":[Sort_shield(nom)]}
                for sortilege in sorts_du_dico:  # Pour chaque sort de chaque attribut
                    if sort_du_perso == sortilege.nom:  # si le nom du sort du perso == nom du sort du dico
                        liste_a_injecter.append(
                            sortilege)  # Creer une liste temporaire a trier pour eviter les doublons
        for sorts in self.sorts_connus.values():  # ajouter a cette liste les sorts existants
            liste_a_injecter.append(sorts)
        for objets in liste_a_injecter:
            while not liste_a_injecter.count(objets) == 1:  # tant qu'il y a des doublons, les supprimer
                liste_a_injecter.remove(objets)
        self.sorts_connus = {}  # reinitialiser le dict sort
        for element in liste_a_injecter:
            self.sorts_connus.update(
                {f"Sort {len(self.sorts_connus) + 1}": element})  # lui ajouter chaque objet de sort

    def upgrade(self):
        if self.xp >= self.prochain_niveau:
            if not self.niveau in self.niveau_passe:
                nivo = self.niveau
                for niv in range(1, nivo):
                    self.niveau = niv
                    self.passer_un_niveau()
            self.niveau += 1
            self.passer_un_niveau()
            self.xp = 0
            if not self.niveau == 1:
                print(self.nom, "passe au niveau ", self.niveau)

    def passer_un_niveau(self):
        for element in dico_des_niveaux[str(self.niveau)]:
            if element == "sorts":
                list_sortilege = []
                for sortilege in dico_des_niveaux[str(self.niveau)]["sorts"]:
                    list_sortilege.append(sortilege)
                self.ajouter_sort_perso(list_sortilege)
            if element == "pv":  # TODO a refactoriser en mieux
                self.pv += dico_des_niveaux[str(self.niveau)][element]
            if element == "force":
                self.force += dico_des_niveaux[str(self.niveau)][element]
            if element == "dexterite":
                self.dexterite += dico_des_niveaux[str(self.niveau)][element]

        self.prochain_niveau = dico_des_niveaux[str(self.niveau)]["prochain_niveau"]
        self.niveau_passe.append(self.niveau)

    def attaquer(self, cible):
        """Si dexterite de l'attaquant superieur a la classe d'armure de l'attaqué :
        degats de force dans pv cible"""
        touche = False
        self.dexterite = self.de_perso.lancer_de()
        self.devenir_hostile(cible)
        cible.devenir_hostile(self)

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

    def devenir_hostile(self, cible2):
        """
        :param cible2: deviens rival
        """
        if not cible2 in self.rival:
            self.rival.append(cible2)


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

dico_sort = {"Protection": [Sort_shield("Shield"), Sort_shield("Barriere"), Sort_shield("Racines"), Sort_shield("Peau de pierre")],
             "Heal": [Sort_heal("Soin"),Sort_heal("Toucher"),Sort_heal("Mains bénis"),Sort_heal("Appel de la lumière"),Sort_heal("Soleil")],
             "Damage": [Sort_damage("Mains Brulantes"),Sort_damage("Epee"),Sort_damage("Feu"),Sort_damage("Glace")]}
