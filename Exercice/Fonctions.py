from random import randint, choice
from pathlib import Path

import Classes

CHOIX_MENU = ["1", "2", "3"]
CHOIX_MENU_DETAILS = ["Attaquer", "Lancer un sort", "Boire un café"]
current_directory = Path()
chemin_nom = current_directory / "nom.txt"
chemin_comportement = current_directory / "comportement.txt"
with open(chemin_comportement, 'r') as cc:
    liste_comportement = cc.read().split('\n')
##############################################################

dico_sort = {"Protection": [Classes.Sort_shield("Shield")],
             "Heal": [Classes.Sort_heal("Soin")],
             "Damage": [Classes.Sort_damage("Mains Brulantes")]}

def ajouter_sort(liste_nom_sort: list) -> list:  # liste en string
    """
    :param liste_nom_sort: du personnage
    :return: liste objets sorts concernés
    """
    liste_objets_sorts = []
    for sort_du_perso in liste_nom_sort:  # Pour chaque sort du perso
        for nom_attributs, sorts_du_dico in dico_sort.items():  # Pour chaque cle, valeur dans le dico
            for sortilege in sorts_du_dico:  # Pour chaque sort de chaque attribut
                if sort_du_perso == sortilege.nom:  # si le nom du sort du perso == nom du sort du dico
                    liste_objets_sorts.append(sortilege)
    return liste_objets_sorts

def retourne_dict_choix_sort(joueur):
    dictio_sort = {}
    i = 1
    for cle, sort_connu in joueur.sorts_connus.items():
        print(f"{i}. {joueur.sorts_connus[cle].nom}")  # choix du sort perso
        dictio_sort.update({str(i): sort_connu})
        i += 1
    return dictio_sort


def choisir_un_nom_perso() -> str:
    listenom = open(chemin_nom, 'r').read().split('\n')  # splitlines()
    return choice(listenom)  # :-1


def trouver_sort_joueur(nom_du_sort, personnage) -> object:
    """
    :param nom_du_sort: str
    :param personnage: instance personnage
    :return: objet perso.sorts_connus
    """
    for cle, element in personnage.sorts_connus.items():
        if element.nom == nom_du_sort:
            print(element.nom)
            print(personnage.sort_connus[cle].nom)
            return personnage.sort_connus[cle]


def donner_stat_aleatoire():
    """
    Affecte 1 nb entre (min et max) a chaque categorie force, ca et intelligence
    """
    stats = {"force": randint(1, 20), "CA": randint(1, 20), "intelligence": randint(1, 20), "dexterite": 15}
    return stats



def victoire(perso, ennemi, boucle_de_jeu):
    if not ennemi.en_vie:
        print(f"{ennemi.nom} est mort et {perso.nom} gagne le combat ! ")
        perso.xp += ennemi.xp
        print(f"{perso.nom} : {perso.xp} xp")
    if not perso.en_vie:
        print(f"{perso.nom} est mort et {ennemi.nom} gagne le combat !")
        ennemi.xp += perso.xp
        print(f"{ennemi.nom} : {ennemi.xp} xp")
    else:
        if boucle_de_jeu >= 10:
            print("Victoire Ecrasante !")


def defile_menu():
    i = 0
    for element in CHOIX_MENU:
        print(f"{element}. {CHOIX_MENU_DETAILS[i]}\n")
        i += 1

