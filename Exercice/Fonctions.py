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
with open(chemin_nom, 'r') as cn:
    listenom = cn.read().split('\n')


##############################################################


def retourne_dict_choix_sort(joueur):
    dictio_sort = {}
    i = 1
    for cle, sort_connu in joueur.sorts_connus.items():
        print(f"{i}. {joueur.sorts_connus[cle].nom}")  # choix du sort perso
        dictio_sort.update({str(i): sort_connu})
        i += 1
    return dictio_sort


def choisir_un_nom_perso() -> str:
    return choice(listenom)  # :-1


def trouver_sort_joueur(nom_du_sort, personnage) -> object:
    """
    :param nom_du_sort: str
    :param personnage: instance personnage
    :return: objet perso.sorts_connus
    """
    for cle, element in personnage.sorts_connus.items():
        if element.nom == nom_du_sort:
            # print(element.nom)
            # print(personnage.sorts_connus[cle].nom)
            return cle


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
        perso.upgrade()
        ennemi = Classes.Personnage(choisir_un_nom_perso(), donner_stat_aleatoire(), "Ordinateur")
        print("\nUn homme louche se presente devant vous....")
        print(f"C'est {ennemi.nom} ! Votre ennemi juré !\n{ennemi.nom} {choice(liste_comportement)}\n")
    if not perso.en_vie:
        print(f"{perso.nom} est mort et {ennemi.nom} gagne le combat !")
        ennemi.xp += perso.xp
        print(f"{ennemi.nom} : {ennemi.xp} xp")
        ennemi.upgrade()
        return [perso, ennemi, True]
    else:
        if boucle_de_jeu >= 31:
            print("Victoire Ecrasante !")
            return [perso, ennemi, True]
    return [perso, ennemi]


def defile_menu(ennemi):
    i = 1
    print(f"1. {CHOIX_MENU_DETAILS[0]} {ennemi.nom}\n")
    for element in CHOIX_MENU[1:]:
        print(f"{element}. {CHOIX_MENU_DETAILS[i]}\n")
        i += 1


def actualiser_cooldown_et_etat(liste_mob):
    liste_a_supprimer = []
    for joueur in liste_mob:  # pour chaque joueur dans la liste_joueurs
        for numero_sort in joueur.sorts_connus.keys():
            joueur.sorts_connus[numero_sort].cooldown -= 1
        for etat_name in joueur.etat_du_perso.keys():  # {"Protection" = 3}
            joueur.etat_du_perso[etat_name] -= 1
            if joueur.etat_du_perso[etat_name] == 0:  # suppression de l'etat
                liste_a_supprimer.append(etat_name)
        for element in liste_a_supprimer:
            if element in joueur.etat_du_perso:
                del (joueur.etat_du_perso[element])
        # print(joueur.etat_du_perso)


def tour_joueurs(celui_qui_joue, celui_qui_attend):
    choix_user = ""
    choix_user_sort = ""
    nom_sort = ""
    if celui_qui_attend.en_vie:
        if celui_qui_joue.statut == "Ordinateur":
            if celui_qui_joue.en_vie:
                for cle, sort_ennemi in celui_qui_joue.sorts_connus.items():
                    if sort_ennemi.nom == "Soin":
                        sort_de_soin = sort_ennemi
                if celui_qui_joue.pv < 20 and sort_de_soin.cooldown <= 0:
                    choix_user = "2"
                    nom_sort = "Soin"
                elif not celui_qui_attend in celui_qui_joue.rival:  # sinon si le joueur n'est pas un rival
                    if choice(["devient hostile", "reste calme", "reste calme",
                               "reste calme"]) == "devient hostile":  # 1/4
                        print(f"{celui_qui_joue.nom} vous attaque ! ")
                        # tentative d'hostilité
                        choix_user = "1"
                    else:
                        print(f"{celui_qui_joue.nom} {choice(liste_comportement)}")  # sinon ronge son frein
                        choix_user = "3"
                else:
                    choix_user = "1"  # si joueur est rival = l'ennemi l'attaque

    if celui_qui_joue.en_vie:
        while not choix_user in CHOIX_MENU:
            defile_menu(celui_qui_attend)  # le joueur choisit son action
            choix_user = input("\n")

    if choix_user == "2":
        if celui_qui_joue.statut == "PJ":
            dico_affichage = retourne_dict_choix_sort(celui_qui_joue)
            while not choix_user_sort in dico_affichage.keys():  # le joueur choisit ses sorts
                choix_user_sort = input()  # {f"Sort {len(self.sorts_connus) + 1}": element})
            nom_sort = celui_qui_joue.sorts_connus[f"Sort {choix_user_sort}"].nom
            print(nom_sort)
        else:
            if nom_sort == "":
                if celui_qui_attend == celui_qui_joue.rival:
                    dico_sort_damage = {}
                    for cle, sortileges in celui_qui_joue.sorts_connus.items():  # l'ennemi choisit ses sorts
                        if sortileges.attributs == "Damage":
                            dico_sort_damage.update({f"{cle}": sortileges})
                        else:
                            choix_user = "1"
                    sort_choisi = choice(list(dico_sort_damage.keys()))
                    nom_sort = celui_qui_joue.sorts_connus[sort_choisi].nom

            else:
                print(f"{celui_qui_joue.nom} {choice(liste_comportement)}")
                # choix_user = "3"

    if not nom_sort == "":
        sort = trouver_sort_joueur(nom_sort, celui_qui_joue)
        celui_qui_joue.sorts_connus[sort].lancer(celui_qui_joue, celui_qui_attend)

    if choix_user == "1":
        celui_qui_joue.attaquer(celui_qui_attend)  # atk

    if choix_user == "3":
        if not celui_qui_joue in celui_qui_attend.rival and celui_qui_joue.statut == "PJ":
            print("Un bon café chaud...\n")
        elif celui_qui_joue.statut == "Ordinateur":
            print()
        else:
            print("Un café ? En plein combat ? Tu perds un tour !")
