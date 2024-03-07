from Classes import Personnage, Sort_shield, Sort_heal, Sort_damage
from Fonctions import donner_stat_aleatoire

dico_sort = {"Protection": [Sort_shield("Shield")],
             "Heal": [Sort_heal("Soin")],
             "Damage": [Sort_damage("Mains Brulantes")]}

liste_nom_sort_perso = ["Soin", "Shield"]


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


perso = Personnage("Raclette", donner_stat_aleatoire())
perso.sorts_connus = ajouter_sort(liste_nom_sort_perso)

print(perso.sorts_connus)

# dico_crea_objet = {"Protection": Sort_shield(nom_du_sort), "Damage": Sort_damage(nom_du_sort),
#                    "Heal": Sort_heal(nom_du_sort)}
#
