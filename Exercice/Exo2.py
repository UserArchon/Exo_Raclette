from random import choice
import Fonctions

# 1 . Creation Perso
print()

perso = Fonctions.Classes.Personnage(input("Bonjour, comment tu t'appelles ?\n"), Fonctions.donner_stat_aleatoire(),
                                     "PJ")
# perso = Fonctions.Classes.Personnage("Didier", Fonctions.donner_stat_aleatoire(), "PJ")
perso.ajouter_sort_perso(["Soin", "Mains Brulantes"])
ennemi = Fonctions.Classes.Personnage(Fonctions.choisir_un_nom_perso(), Fonctions.donner_stat_aleatoire(), "Ordinateur")
print()
print(f"Un individu s'approche de vous, vous le reconnaissez, il s'agit de {ennemi.nom} !")
ennemi.ajouter_sort_perso(["Soin", "Mains Brulantes"])
liste_mob = [perso, ennemi]
boucle_jeu = 1

while boucle_jeu < 31:
    print()
    print(f"Tour n°{boucle_jeu}")
    print()
    liste_mob = Fonctions.victoire(perso, ennemi, boucle_jeu)
    if True in liste_mob:
        break
    Fonctions.actualiser_cooldown_et_etat(liste_mob)

    Fonctions.tour_joueurs(perso, ennemi)
    Fonctions.tour_joueurs(ennemi, perso)


    boucle_jeu += 1

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
