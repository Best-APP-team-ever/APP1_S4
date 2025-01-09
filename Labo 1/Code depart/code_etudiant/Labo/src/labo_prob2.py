#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le deuxième exercice du laboratoire - APP du cours GIF270

    L'exercice 2 touche les tableaux de hachage et leur redéfinition en Python :
        - Redéfinition de la méthode pour établir l'égalité entre deux objets
        - Redéfinition de la méthode de hachage pour obtenir un nombre à partir d'un objet
        - Redéfinition de la méthode d'ajout d'un bigramme dans un vecteur (dict qui contient un ensemble de bigrammes)
        - Redéfinition de la méthode pour calculer la taille d'un vecteur
        - Redéfinition du produit scalaire entre deux vecteurs
        - Redéfinition de la méthode de calcul du cosinus de l'angle entre deux vecteurs

    De plus, cet exercice touche aussi l'utilisation de :
        - listes (non-immuable)
        - d'autres structures apparentées aux listes, mais immuables (lesquelles ?)

  Copyright 2018-2025, Frédéric Mailhot et Université de Sherbrooke
"""

from labo_prob2_common import LaboProb2Common
from labo_prob2_common import BigramCommon
import math
import numpy as np
from typing import Any


# Pour ce problème, vous devez :
#   - compléter les méthodes suivantes de la classe Bigram :
#       - __eq__()
#       - __hash__()
#   - compléter les méthodes suivantes de la classe LaboProb2 :
#       - add_bigram()
#       - add_bigram_object()
#       - add_bigram_other()
#       - vector_size()
#       - scalar_product()
#       - cosine()
# Lire les commentaires au début de chacune de ces méthodes pour savoir plus précisément ce qui doit être fait.
#
# Important: - Vous ne devez modifier aucun code dans le fichier labo_prob2_common.py
#            - Vous n'avez pas à modifier la méthode add_bigram_vector, mais sachez qu'elle ne fonctionne pas...
#
# Note :
#       1. Vous pouvez constater que la classe Bigram hérite de la classe BigramCommon.
#       On doit y redéfinir les méthodes __eq__() et __hash__()
#
#       2. De même, la classe LaboProb2 hérite de la classe LaboProb2Common.
#       Ici encore, on redéfinit un certain nombre de méthodes :
#           add_bigram_object(), add_bigram_other(), vector_size(), scalar_product(), cosine().


class Bigram(BigramCommon):
    """Création de méthodes permettant de personnaliser un dictionnaire (tableau de hachage)
    - Dans cette classe, on redéfinit comment faire le hash et comparer deux objets de type Bigram
    """

    def __eq__(self: list, other: list) -> bool:
        """Redéfinition de l'égalité entre deux bigrammes :
            - L'un des bigrammes est self (celui avec lequel __eq__ est appelé)
            - Le deuxième bigramme est other, fourni en paramètre

        Args :
            other (Bigram) : Le bigramme avec lequel il faut se comparer

        Returns :
            (bool) : Retourne True ou False, selon l'égalité entre les bigrammes
        """
        # Vous devez coder ici comment déterminer que deux bigrammes (paires de mots) sont les mêmes.
        # Le paramètre "other" est un autre bigramme (instance de la classe Bigram).
        # Pour le moment, la comparaison ne fait que vérifier que les objets sont des instances de la même classe.
        # Vous devrez ajouter d'autres conditions qui déterminent que deux bigrammes sont égaux (ou non).
        # Note: Il n'est pas nécessaire d'utiliser la méthode "isinstance".
        #       Elle est utilisée ici simplement pour démontrer qu'elle existe,
        #       et qu'on peut facilement vérifier si les classes de deux objets correspondent
        if isinstance(other, self.__class__):
            #self est déjà normalisé fait par JT
            # Normaliser sans modifier l'objet "other"
            normalized_other_word1 = Bigram.normalize_string(other[0])
            normalized_other_word2 = Bigram.normalize_string(other[1])
            if (self[0] == normalized_other_word1) and (self[1] == normalized_other_word2):
                return True
        return False

    def __hash__(self: list) -> int:
        """Redéfinition de la méthode de hachage d'un bigramme :
            - Doit utiliser les deux mots du bigramme

        Args :
            (void) : Toute l'information nécessaire (a et b) se trouve dans le bigramme

        Returns :
            (int) : Retourne la valeur de hachage
        """
        # Faire en sorte que la fonction de hachage utilise les deux mots du bigramme.
        # Pour le moment, on n'utilise que le premier mot.
        # Vous devez changer ce qui est utilisé comme entrée dans la fonction de hachage.
        # Vous pourriez utiliser une combinaison des deux mots, avec un séparateur qui n'est pas une lettre.
        combo_string = self[0]+"_"+ self[1]
        return hash(combo_string)


class LaboProb2(LaboProb2Common):
    """Classe de test pour valider la personalisation d'un dictionnaire (tableau de hachage)
        - Classe hérite de ParsingClass2, qui lit les paramètres de la ligne de commande
    """

    @staticmethod
    def add_bigram(bigram: Any, bigram_dict: dict) -> None:
        """Méthode appelée pour ajouter un bigramme au dictionnaire fourni :

        Args :
            bigram (Any) : object (arbitraire) qui représente un bigramme et qui est utilisé comme clé
            bigram_dict (dict) : tableau de hachage de bigrammes.  Utilisé pour emmagasiner et compter les bigrammes

        Returns :
            (void) : Le nouveau bigramme est ajouté au dictionnaire de bigrammes fourni
        """
        # Ici, remplacez les prints par votre code.
        # Le tableau de hachage bigram_dict devrait accumuler et compter les bigrammes à mesure qu'on les ajoute.
        # On suppose qu'au départ, le tableau de hachage est vide

        hash_bigram_rentrant = Bigram.__hash__(bigram) #techniquement déjà handle par python
        if hash_bigram_rentrant in bigram_dict:
            if Bigram.__eq__(bigram, bigram_dict[hash_bigram_rentrant]["bigram"]):
                bigram_dict[hash_bigram_rentrant]["instances"] += 1
            else: #existe seulement pour vérifier s'il a eu plus que 2 fois le même Bigram
                test = True
                while test:
                    hash_bigram_rentrant += 1
                    if hash_bigram_rentrant in bigram_dict:
                        if Bigram.__eq__(bigram, bigram_dict[hash_bigram_rentrant]["bigram"]):
                            bigram_dict[hash_bigram_rentrant]["instances"] += 1
                            test = False
                    else:
                        bigram_dict[hash_bigram_rentrant] = {"bigram": bigram, "instances": 1}
                        test = False
        else:
            bigram_dict[hash_bigram_rentrant] = {"bigram": bigram, "instances": 1}
        print(bigram)
        print(bigram_dict)
        return

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def add_bigram_vector(word1: str, word2: str, bigram_dict: dict) -> None:
        """Méthode appelée pour créer un vecteur de deux mots et pour l'ajouter au dictionnaire fourni :
            - Est-ce que cette méthode fonctionne ?  Pourquoi ?
            - Si elle ne fonctionne pas, utilisez plutôt les méthodes add_bigram_object et add_bigram_tuple

        Args :
            word1 (str) : premier mot
            word2 (str) : deuxième mot
            bigram_dict (dict) : tableau de hachage de bigrammes.  Utilisé pour emmagasiner et compter les bigrammes

        Returns :
            (void) : Le nouveau bigramme est ajouté au dictionnaire de bigrammes fourni
        """
        # Code invalide.  Utiliser pour découvrir quel est le problème, mais il n'est pas nécessaire de le corriger :
        #   Regarder quel est le type de l'erreur (TypeError) associée à la ligne 109 de add_bigram()
        # Plutôt que de modifier le code, inclure le paramètre "-p 2" ou "-p 3" sur la ligne de commande
        #    pour utiliser les méthodes add_bigram_object() et add_bigram_other()
        bigram = [word1, word2]
        LaboProb2.add_bigram(bigram, bigram_dict)
        return

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def add_bigram_object(word1: str, word2: str, bigram_dict: dict) -> None:
        """Méthode appelée pour créer un bigramme (à l'aide des deux mots fournis)
            et pour l'ajouter au dictionnaire fourni :

        Args :
            word1 (str) : premier mot
            word2 (str) : deuxième mot
            bigram_dict (dict) : tableau de hachage de bigrammes.  Utilisé pour emmagasiner et compter les bigrammes

        Returns :
            (void) : Le nouveau bigramme est ajouté au dictionnaire de bigrammes fourni
        """
        # Ici, remplacez les prints par votre code.
        # L'utilisation de la classe Bigram est probablement justifiée...
        # Modifier l'appel à la méthode add_bigram pour ajouter le bigramme complet au tableau de bigrammes
        bigram = [word1, word2]
        LaboProb2.add_bigram(bigram, bigram_dict)
        return

    @staticmethod
    def add_bigram_other(word1: str, word2: str, bigram_dict: dict) -> None:
        """Méthode appelée pour créer un bigramme (à l'aide des deux mots fournis)
            et pour l'ajouter au dictionnaire fourni, la clé étant un vecteur :

        Args :
            word1 (str) : premier mot
            word2 (str) : deuxième mot
            bigram_dict (dict) : tableau de hachage de bigrammes.  Utilisé pour emmagasiner et compter les bigrammes

        Returns :
            (void) : Le nouveau bigramme est ajouté au dictionnaire de bigrammes fourni
        """
        # Ici, remplacez les prints par votre code.
        # Que pouvez-vous utiliser pour remplacer un vecteur, mais qui est immuable ?
        bigram = [word1, word2]
        LaboProb2.add_bigram(bigram, bigram_dict)
        return

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def vector_size(vector: dict) -> float:
        """Méthode appelée pour calculer la taille d'un vecteur (tableau de hachage, dict) :

        Args :
            vector (dict) : tableau de hachage contenant tous les bigrammes

        Returns :
            size (int) : La taille du vecteur
        """
        # Ici, vous devez calculer la taille totale du vecteur (le tableau de hachage vector, de type dict).
        # Comme pour tout vecteur, la taille est obtenue en calculant la racine carrée de
        # la somme des carrés des projections dans chacune des dimensions.
        # Cette somme de carrés représente le produit scalaire du vecteur avec lui-même
        # Ici, chaque bigramme distinct est une dimension
        # Remplacez les lignes suivantes par le code approprié.
        # Extract the 'instances' values from the dictionary
        instances = np.array([entry['instances'] for entry in vector.values()])

        # Compute the sum of the squares of the instances values
        sum_of_squares = np.sum(instances ** 2)

        # Compute the square root of the sum of squares to get the magnitude of the vector
        size = np.sqrt(sum_of_squares)

        return size

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def scalar_product(vector1: dict, vector2: dict) -> int:
        """Méthode calculant le produit scalaire entre 2 vecteurs :

        Args :
            vector1 (dict) : tableau de hachage contenant tous les bigrammes du premier fichier
            vector2 (dict) : tableau de hachage contenant tous les bigrammes du deuxième fichier

        Returns :
            prod_scal (int) : Produit scalaire entre les deux vecteurs
        """
        # Ici, vous devez calculer le produit scalaire entre les deux vecteurs.
        # Pour ce faire, vous devez multiplier les valeurs des projections dans chacune des dimensions.
        # De nouveau, les dimensions correspondent aux bigrammes.
        # Si un bigramme existe dans un seul des vecteurs, alors la projection est nulle dans l'autre,
        #   et en conséquence le produit pour cette dimension est nul.
        # Remplacez le print et les lignes suivantes par le code approprié.
        scal_prod = 0
        for hash_id in vector1:
            if hash_id in vector2:
                scal_prod += vector1[hash_id]["instances"] * vector2[hash_id]["instances"]
        return scal_prod

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def cosine(vector1: dict, vector2: dict) -> float:
        """Méthode calculant le cosinus de l'angle entre 2 vecteurs (produit scalaire normalisé) :

        Args :
            vector1 (dict) : tableau de hachage contenant tous les bigrammes du premier fichier
            vector2 (dict) : tableau de hachage contenant tous les bigrammes du deuxième fichier

        Returns :
            angle_cos (float) : Cosinus de l'angle entre les deux vecteurs (produit scalaire normalisé)
        """
        # Ici, vous devez calculer le cosinus de l'angle entre les deux vecteurs, soit le produit scalaire normalisé.
        # Pour normaliser un vecteur, il faut diviser chacune des projections par la longueur totale du vecteur.
        # Vous devez donc :
        #   - Effectuer le produit scalaire entre les deux vecteurs,
        #     puis diviser le résultat par leurs longueurs respectives.
        # Remplacer le print et les lignes qui suivent par le code approprié.
        # Note: Assurez-vous que le résultat ne dépasse pas 1.0, sinon math.acos() causera une exception.
        # Remplacer les lignes qui suivent par le code approprié.
        angle_cos = (LaboProb2.scalar_product(vector1, vector2)/(LaboProb2.vector_size(vector1)*(LaboProb2.vector_size(vector1))))
        return angle_cos


# Main : lecture des paramètres et appel des méthodes appropriées
def main() -> None:
    """Démarrage de l'exercice 2 du labo :
        - Crée une instance de la classe LaboProb2, utilisée pour tester les mots de deux fichiers
        - Trois méthodes sont explorées pour utiliser des bigrammes comme clé d'un tableau de hachage :
            - Vecteur []
            - Instance de la classe Bigramme (qui doit être ajustée adéquatement)
            - Alternative au vecteur, qui est immuable
        - Dans la classe Bigramme de LaboProb2, il faut redéfinir les opérations d'égalité et de hachage

    Returns :
        (void) : Au retour, l'exécution est terminée
    """
    # Vous n'avez rien à modifier dans la méthode main()
    p2 = LaboProb2()
    match p2.args.p: # La méthode d'ajout de bigrammes est modifiée selon le choix effectué sur la ligne de commande
        case 1:
            p2.define_add_bigram_func(LaboProb2.add_bigram_vector)
        case 2:
            p2.define_add_bigram_func(LaboProb2.add_bigram_object)
        case 3:
            p2.define_add_bigram_func(LaboProb2.add_bigram_other)
        case _:
            print("Exercice 2, type inconnu de traitement d'objets dans un tableau de hachage (doit être 1,2 ou 3)")
    p2.read()
    p2.do_something()
    return


if __name__ == "__main__":
    main()
