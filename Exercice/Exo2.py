from random import choice
import Fonctions



def tour_joueurs(celui_qui_joue, celui_qui_attend):
    choix_user = ""
    choix_user_sort = ""
    nom_sort = ""
    if celui_qui_attend.en_vie:
        if celui_qui_joue == ennemi:
            if celui_qui_joue.en_vie:
                if celui_qui_joue.pv < 20:
                    choix_user = "2"
                    nom_sort = "Soin"
                elif not celui_qui_attend in celui_qui_joue.rival:  # sinon si le joueur n'est pas un rival
                    if choice(["devient hostile", "reste calme", "reste calme",
                               "reste calme"]) == "devient hostile":  # 1/4
                        print(f"{celui_qui_joue.nom} vous attaque ! ")
                        celui_qui_joue.devenir_hostile(celui_qui_attend)  # tentative d'hostilité
                        choix_user = "1"
                    else:
                        print(f"{celui_qui_joue.nom} {choice(Fonctions.liste_comportement)}")  # sinon ronge son frein
                        choix_user = "3"
                else:
                    choix_user = "1"  # si joueur est rival = l'ennemi l'attaque

    if celui_qui_joue.en_vie:
        while not choix_user in Fonctions.CHOIX_MENU:
            print()
            Fonctions.defile_menu()  # le joueur choisit son action
            choix_user = input("\n")

    if choix_user == "2":
        if celui_qui_joue == perso:
            dico_affichage = Fonctions.retourne_dict_choix_sort(celui_qui_joue)
            while not choix_user_sort in dico_affichage.keys():  # le joueur choisit ses sorts
                choix_user_sort = input()  # {"1":"Soin"}
            nom_sort = dico_affichage[choix_user_sort]

        else:
            if nom_sort == "":
                if celui_qui_attend == celui_qui_joue.rival:
                    for cle, sortileges in celui_qui_joue.sorts_connus.items():  # l'ennemi choisit ses sorts
                        if sortileges.attributs == "Damage":
                            nom_sort = celui_qui_joue.sorts_connus[cle].nom
                        else:
                            choix_user = "1"
                else:
                    print(f"{celui_qui_joue.nom} {choice(Fonctions.liste_comportement)}")
                    choix_user = "3"

        if not nom_sort == "":
            sort = Fonctions.trouver_sort_joueur(nom_sort, celui_qui_joue)
            sort.lancer(celui_qui_joue, celui_qui_attend)

    if choix_user == "1":
        celui_qui_joue.attaquer(celui_qui_attend)  # atk


    else:
        print("Un bon café chaud...\n")


# def tour_perso(perso, ennemi):
#     choix_user = ""
#     while not choix_user in CHOIX_MENU:
#         print()
#         defile_menu()
#         choix_user = input("\n")
#
#     if choix_user == "1":
#         perso.attaquer(ennemi)  # atk du perso dans ennemi
#
#     elif choix_user == "2":
#         liste_nb_sorts = []
#         i = 1
#         for sort in perso.sorts_connus:
#             print(f"{i}. {sort.nom}\n")
#             liste_nb_sorts.append(str(i))
#             i += 1
#         choix_user_sort = ""
#         while not choix_user_sort in liste_nb_sorts:  # range(min,len(perso.sorts_connus)):
#             choix_user_sort = input()  # affiche la liste jusqu'au choix
#         choix_user_sort = int(choix_user_sort)
#
#         perso.sorts_connus[choix_user_sort - 1].lancer(perso, ennemi)
#
#
#     else:
#         print("Ta cru que c'était le moment ?\n")
#
#
# def tour_i_a_ennemi(ennemi, perso):
#     if ennemi.en_vie:
#         if ennemi.pv < 20:
#             if ennemi.pv < 10 and ennemi.sorts_connus[0].cooldown <= 0:
#                 ennemi.sorts_connus[0].lancer(ennemi, ennemi)
#             else:
#                 if choice(["O", "N"]) == "O" and ennemi.sorts_connus[0].cooldown <= 0:
#                     ennemi.sorts_connus[0].lancer(ennemi, ennemi)
#                 else:
#                     print(f"{ennemi.nom} n'arrive pas a se soigner")
#         else:
#
#             if not perso in ennemi.rival:  # si le joueur n'est pas un rival
#                 if choice(["devient hostile", "reste calme", "reste calme", "reste calme"]) == "devient hostile":  # 1/4
#                     print(f"{ennemi.nom} vous attaque ! ")
#                     devenir_hostile(ennemi, perso)
#                 else:
#                     liste_comportement = open(chemin_comportement, 'r').read().split('\n')  # splitlines()
#                     print(f"{ennemi.nom} {choice(liste_comportement)}")  # sinon ronge son frein
#             if perso in ennemi.rival:
#                 ennemi.attaquer(perso)  # si joueur est rival = l'ennemi l'attaque
#     else:
#         print(f"{ennemi.nom} agonise")
#

def dec_del_etat_dict_perso(liste_mob):
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
        print(joueur.etat_du_perso)


# def dec_del_etat_dict_perso(liste_mob):
#     liste_a_supprimer = []
#     for joueur in liste_mob:  # pour chaque joueur dans la liste_joueurs
#         for etat_name in joueur.etat_du_perso:  # pour chaque nom d'etat ("Protection") par exemple
#             if joueur.etat_du_perso[etat_name] > 0:  # si la valeur de l'etat > 0
#                 joueur.etat_du_perso[etat_name] -= 1  # descendre la valeur par tour
#                 for cle in joueur.sorts_connus.keys():
#                     # si le nom de l'etat du perso == nom du sort du perso alors cooldown == valeur de joueur.etat_du_perso
#                     if joueur.sorts_connus[cle].nom == etat_name:
#                         joueur.sorts_connus[cle].cooldown = joueur.etat_du_perso[etat_name]  # cooldown = valeur etat
#                     else:
#                         joueur.sorts_connus[cle].cooldown -= 1  # sinon descendre cooldown
#             if joueur.etat_du_perso[etat_name] == 0:
#                 liste_a_supprimer.append(etat_name)
#         for element in liste_a_supprimer:
#             if element in joueur.etat_du_perso:
#                 del (joueur.etat_du_perso[element])
jeu = False

# 1 . Creation Perso
print()

# perso = Classes.Personnage(input("Bonjour, comment tu t'appelles ?\n"), donner_stat_aleatoire())
perso = Fonctions.Classes.Personnage("Didier", Fonctions.donner_stat_aleatoire())
ennemi = Fonctions.Classes.Personnage("Robert", Fonctions.donner_stat_aleatoire())
liste_mob = [perso, ennemi]

# liste_nom_categorie_sort = ["Protection", "Heal", "Damage"]

# print("ajout 1")
# perso.ajouter_sort_perso(["Soin", "Mains Brulantes"])
print(f"force = {perso.force}")
print(f"dexterite = {perso.dexterite}")
print(f"pv = {perso.pv}")

perso.upgrade()
print(f"prochain = {perso.prochain_niveau}")

for element in perso.sorts_connus.values():
    print(element.nom)
print(f"force 2 = {perso.force}")
print(f"dexterite 2 = {perso.dexterite}")
print(f"pv 2 = {perso.pv}")
print(perso.niveau_passe)

perso.xp += 1300
perso.upgrade()
print()
for element in perso.sorts_connus.values():
    print(element.nom)
print(f"force 2 = {perso.force}")
print(f"dexterite 2 = {perso.dexterite}")
print(f"pv 2 = {perso.pv}")
print(perso.niveau_passe)

# pprint(perso.sorts_connus)
# gibier = 1
# while gibier < 11:
# print()
# print(f"Tour n°{gibier}")
# dec_del_etat_dict_perso(liste_mob)

# tour_joueurs(perso, ennemi)
# tour_joueurs(ennemi, perso)
#
#     gibier += 2
#
# if jeu:
#     pass

# # 2 . Phase de Jeu
# boucle_de_jeu = 0
#
# while boucle_de_jeu < 10:
#
#     print(f"Tour {boucle_de_jeu + 1}")
#
#     ennemi = Personnage(choisir_un_nom_perso(), donner_stat_aleatoire())
#
#     while ennemi.en_vie:  # tant que l'ennemi est en vie
#         liste_mob = [perso, ennemi]
#
#         perso.upgrade()  # test si niveau superieur atteint
#
#         tour_perso(perso, ennemi)
#
#         tour_i_a_ennemi(ennemi, perso)
#
#         victoire(perso, ennemi, boucle_de_jeu)  # Tests des victoires pour affichage
#         if not ennemi.en_vie:
#             break
#         if not perso.en_vie:
#             break
#         # descendre_les_compteurs(liste_mob)
#
#     if not perso.en_vie:
#         break
#     boucle_de_jeu += 1
#

#
# perso.sorts_connus["sort1"].lancer(perso.sorts_connus["sort1"], perso, perso)
# perso.sorts_connus["sort2"].lancer(perso.sorts_connus["sort2"], perso, perso2)
# perso.sorts_connus["sort3"].lancer(perso.sorts_connus["sort3"], perso, perso)


# dico = perso.sorts_connus["sort3"].__dict__
#
# with open(r"D:\Programmation\Pycharm\Exercice\dico_categorie_sort.json",'w') as m:
#     json.dump(dico,m, indent=4)

# with open(r"D:\Programmation\Pycharm\Exercice\dico_categorie_sort.json", 'r') as f:
#     dico = f.read()

# print(dico)
