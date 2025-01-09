#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le deuxième exercice du laboratoire - APP du cours GIF270

    L'exercice 2 touche les tableaux de hachage et leur redéfinition en Python :
        - Redéfinition de la méthode pour établir l'égalité entre deux objets
        - Redéfinition de la méthode de hachage pour obtenir un nombre à partir d'un objet
        - Redéfinition de la méthode d'ajout d'un bigramme dans un vecteur (dict qui contient un ensemble de bigrammes)
        - Redéfinition de la méthode pour calculer la taille d'un vecteur
        - Redéfinition de la méthode de calcul du produit scalaire entre deux vecteurs
        - Redéfinition de la méthode de calcul du cosinus de l'angle entre deux vecteurs

    Note :
        - Le traitement des arguments a été inclus dans la classe ParsingClass2, qui est utilisée dans le code principal
        - Tous les arguments requis sont présents et accessibles dans ParsingClass2.args
        - Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
        - La classe SmartFormatter permet d'imprimer correctement la chaîne de caractère "help" lorsqu'elle débute par "R|"

  Copyright 2018-2025, Frédéric Mailhot et Université de Sherbrooke
"""

import argparse
import sys
import math
from typing import Any, Callable

from smart_formatter_common import SmartFormatter
from handle_unicode_common import HandleUnicodeCommon


class ParsingClass2(HandleUnicodeCommon):
    """Création d'un parser prédéfini pour lire les paramètres de la ligne de commande pour le deuxième exercice
    """

    def setup_and_parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog='Labo1:Exercice2.py', formatter_class=SmartFormatter)
        parser.add_argument('-p', default=1, type=int,
                            help="R|"
                                 "Type de problème à débugger l'utilisation de n-grammes (par défaut, 1):\n"
                                 "  1: Utilisation de vecteurs dans un tableau de hachage (ne fonctionnera pas),\n"
                                 "  2: utilisation d'une classe dédiée dans un tableau de hachage,\n"
                                 "  3: modification de l'utilisation de vecteurs dans un tableau de hachage")
        parser.add_argument('-f', required=True, help='Fichier contenant la liste de paires de mots de départ')
        parser.add_argument('-t', required=True, help='Fichier contenant la liste de paires de mots à vérifier')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        self.parser = parser
        self.args: argparse.Namespace = parser.parse_args()
        return

    @staticmethod
    def read_file_lines(filename: str) -> list:
        """Lecture d'un fichier' :

        Args :
            filename (str) : Le nom du fichier à lire

        Returns :
            file_lines (array) : Tableau avec les lignes du fichier lu
        """

        try:
            with open(filename) as file:
                file_lines = [line.rstrip() for line in file]
            return file_lines
        except FileNotFoundError:
            print("Fichier ", filename, " inexistant")
            sys.exit(1)

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de ParsingClass2 :
            - Ajoute toutes les valeurs par défaut des paramètres utilisés
            - Modifie les valeurs redéfinies sur la ligne de commande

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        self.parser: argparse.ArgumentParser = None
        self.args: argparse.Namespace = None
        self.setup_and_parse_cli()

        # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
        if self.args.v:
            print("Mode verbose:")
            print("Fichier de paires de mots de départ: " + self.args.f)
            print("Fichier de paires de mots à vérifier: " + self.args.t)
            match self.args.p:
                case 1:
                    print("Utilisation de vecteurs dans un tableau de hachage (ne fonctionnera pas)")
                case 2:
                    print("Utilisation d'une classe dédiée dans un tableau de hachage")
                case 3:
                    print("Modification de l'utilisation de vecteurs dans un tableau de hachage")
                case _:
                    print("Type inconnu de traitement d'objets dans un tableau de hachage (doit être 1,2 ou 3)")
        return


class BigramCommon(HandleUnicodeCommon):
    """Création de méthodes permettant de personnaliser un dictionnaire (tableau de hachage)
    - Dans cette classe, on redéfinit comment faire le hash et comparer deux objets de type Bigramme
    """

    def __eq__(self, other) -> bool:
        """Redéfinition de l'égalité entre deux bigrammes :
            - L'un des bigrammes est self (celui avec lequel __eq__ est appelé)
            - Le deuxième bigramme est other, fourni en paramètre

        Args :
            other (BigramCommon) : Le bigramme avec lequel il faut se comparer

        Returns :
            (bool) : Retourne True ou False, selon l'égalité entre les bigrammes
        """
        # Code incomplet.  Doit être modifié dans la classe Bigram, qui hérite de BigramCommon.
        return isinstance(other, self.__class__)

    def __ne__(self, other) -> bool:
        """Redéfinition de l'inégalité entre deux bigrammes :
            - Utilise __eq__ et inverse la réponse

        Args :
            other (BigramCommon) : Le bigramme avec lequel il faut se comparer

        Returns :
            (bool) : Retourne True ou False, selon l'inégalité entre les bigrammes
        """
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """Redéfinition de la méthode de hachage d'un bigramme :
            - Doit utiliser les deux mots du bigramme

        Args :
            (void) : Toute l'information nécessaire (word1 et word2) se trouve dans le bigramme

        Returns :
            (int) : Retourne la valeur de hachage
        """
        # Code incomplet. Doit être modifié dans la classe Bigram, qui hérite de BigramCommon.
        return hash(self.word1)

    def __str__(self) -> str:
        """Redéfinition de la méthode pour faire un print d'une instance de type Bigramme :

        Args :
            (void) : Toute l'information nécessaire (word1 et word2) se trouve dans le bigramme

        Returns :
            (void) : Au retour, une chaîne de caractères imprimable est créée
        """
        return "Objet BigramCommon: " + self.word1 + "," + self.word2

    def __init__(self, premier_mot: str, deuxieme_mot: str) -> None:
        """Initialisation d'une nouvelle instance de Bigramme :

        Args :
            premier_mot (str) : Premier mot du bigramme
            deuxieme_mot (str) : Deuxième mot du bigramme

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()

        self.word1 = HandleUnicodeCommon.normalize_string(premier_mot)
        self.word2 = HandleUnicodeCommon.normalize_string(deuxieme_mot)
        return


class LaboProb2Common(ParsingClass2):
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
        # Code incomplet.  Doit être modifié dans la classe LaboProb2
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
        bigram = [word1, word2] # Création d'un bigramme
        LaboProb2Common.add_bigram(bigram, bigram_dict)
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
        # Code incomplet.  Doit être modifié dans la classe LaboProb2
        print(word1)
        print(word2)
        print(bigram_dict)
        LaboProb2Common.add_bigram(word1, bigram_dict) # Ajout d'un bigramme dans le tableau de hachage
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
        # Code invalide.  Doit être modifié dans la classe LaboProb2
        bigram = [word1, word2]
        LaboProb2Common.add_bigram(bigram, bigram_dict)
        return

    def read_one_file(self, filename: str, file_dict: dict) -> None:
        """Lecture d'un fichier de bigrammes et ajout dans le tableau de hachage fourni :

        Args :
            filename (str) : Nom du fichier à traiter
            file_dict (dict) : Tableau de hachage à remplir

        Returns :
            (void) : Au retour, le tableau de hachage est complet
        """
        file_lines = self.read_file_lines(filename)
        for one_line in file_lines:
            word1, word2 = one_line.split()
            self.add_bigram_f(word1, word2, file_dict)
        return

    def read(self) -> None:
        """Lecture des deux fichiers nécessaires à l'exercice :

        Args :
            (void) : Tout se trouve déjà dans l'objet

        Returns :
            (void) : Au retour, les tableaux de hachage sont complets
        """
        self.read_one_file(self.args.f, self.input_dict)
        self.read_one_file(self.args.t, self.test_dict)
        return

    @staticmethod  # Cette méthode est statique, parce qu'elle n'utilise aucune valeur de l'objet.
    def vector_size(vector: dict) -> int:
        """Méthode appelée pour calculer la taille d'un vecteur (tableau de hachage, dict) :

        Args :
            vector (dict) : tableau de hachage contenant tous les bigrammes

        Returns :
            size (int) : La taille du vecteur
        """
        # Code incomplet.  Doit être modifié dans la classe LaboProb2, qui hérite de LaboProb2Common.
        size = 0
        size = math.sqrt(size)
        size += LaboProb2Common.scalar_product(vector, vector)
        return size

    @staticmethod
    def scalar_product(vector1: dict, vector2: dict) -> int:
        """Méthode calculant le produit scalaire entre 2 vecteurs :

        Args :
            vector1 (dict) : tableau de hachage contenant tous les bigrammes du premier fichier
            vector2 (dict) : tableau de hachage contenant tous les bigrammes du deuxième fichier

        Returns :
            prod_scal (int) : Produit scalaire entre les deux vecteurs
        """
        # Code incomplet.  Doit être modifié dans la classe LaboProb2, qui hérite de LaboProb2Common.
        print(vector1, vector2)
        prod_scal = 1
        return prod_scal

    @staticmethod
    def cosine(vector1: dict, vector2: dict) -> float:
        """Méthode calculant le cosinus de l'angle entre 2 vecteurs (produit scalaire normalisé) :

        Args :
            vector1 (dict) : tableau de hachage contenant tous les bigrammes du premier fichier
            vector2 (dict) : tableau de hachage contenant tous les bigrammes du deuxième fichier

        Returns :
            angle_cos (float) : Cosinus de l'angle entre les deux vecteurs (produit scalaire normalisé)
        """
        # Code incomplet.  Doit être modifié dans la classe LaboProb2, qui hérite de LaboProb2Common.
        print(vector1, vector2, LaboProb2Common.vector_size(vector1), LaboProb2Common.vector_size(vector2))
        angle_cos = 0.0
        return angle_cos

    @staticmethod
    def print_dict_bigram(bigram_dict: dict) -> None:
        """Méthode utilisée pour imprimer tous les bigrammes contenus dans un tableau de hachage :

        Args :
            bigram_dict (dict) : tableau de hachage contenant des bigrammes

        Returns :
            (void) : Rien n'est retourné
        """
        # Le dictionnaire de bigrammes est parcouru et chacun des bigrammes est imprimé individuellement
        #   de même que le nombre d'occurrences de chaque bigramme.
        for bigram in bigram_dict:
            print(bigram, ":", bigram_dict[bigram])
        return

    @staticmethod
    def print_common_bigrams(input_dict: dict, test_dict: dict) -> None:
        """Méthode utilisée pour imprimer tous les bigrammes communs à deux tableaux de hachage :

        Args :
            input_dict (dict) : tableau de hachage contenant les bigrammes issus du premier fichier
            test_dict (dict) : tableau de hachage contenant les bigrammes issus du deuxième fichier

        Returns :
            (void) : Rien n'est retourné
        """
        # Cette méthode imprime tous les bigrammes communs aux tableaux input_dict et test_dict.
        common_bigram = LaboProb2Common.get_common_bigrams(input_dict, test_dict)
        LaboProb2Common.print_dict_bigram(common_bigram)
        return

    @staticmethod
    def get_common_bigrams(input_dict: dict, test_dict: dict) -> dict:
        """Méthode utilisée pour produire un tableau de hachage avec tous les bigrammes communs
            à input_dict et test_dict

        Args :
            input_dict (dict) : tableau de hachage contenant les bigrammes issus du premier tableau
            test_dict (dict) : tableau de hachage contenant les bigrammes issus du deuxième tableau

        Returns :
            common_dict (dict) : tableau de hachage contenant les bigrammes communs aux deux tableaux
        """
        common_dict = {}
        for bigram in input_dict:
            if bigram in test_dict:
                common_dict[bigram] = {**input_dict[bigram], **test_dict[bigram]}
        return common_dict

    def do_something(self) -> None:
        """Méthode appelée pour donner les statistiques voulues :

        Args :
            (void) : Tout se trouve dans l'objet

        Returns :
            (void) : Au retour, tout a déjà été imprimé à l'écran
        """
        print()
        print("Ici on donne la liste des paires de mots, avec leurs nombres d'occurrences,")
        print("\t et quels éléments apparaissent dans les deux fichiers")

        print()
        print("Input file: -----------------------------------------------")
        print("Input file: ", self.input_dict)
        self.print_dict_bigram(self.input_dict)  # Imprime la liste des bigrammes du fichier d'entrées

        print()
        print("Test file: -----------------------------------------------")
        print("Test file: ", self.test_dict)
        self.print_dict_bigram(self.test_dict)  # Imprime la liste des bigrammes du fichier de test

        print()
        print("Communs: ---------------------------------")
        self.print_common_bigrams(self.input_dict, self.test_dict)  # Imprime la liste des bigrammes communs

        print()
        print("Autres informations: --------------------------")
        print("Nombre de bigrammes - Input file:", len(self.input_dict))
        print("Nombre de bigrammes - Test file:", len(self.test_dict))
        print("Nombre de bigrammes communs:", len(self.get_common_bigrams(self.input_dict, self.test_dict)))
        print("Taille du vecteur de bigrammes - Input file:", f"{self.vector_size(self.input_dict):.2f}")
        print("Taille du vecteur de bigrammes - Test file:", f"{self.vector_size(self.test_dict):.2f}")
        produit_scalaire = self.scalar_product(self.input_dict, self.test_dict)
        cosine = self.cosine(self.input_dict, self.test_dict)
        print("Produit scalaire normalisé des bigrammes communs entre fichiers Input et Test: ", f"{produit_scalaire:.2f}")
        print("Produit scalaire normalisé (cosinus de l'angle) entre fichiers Input et Test: ", f"{cosine:.2f}")
        print("Angle entre les deux fichiers:", f"{180 * math.acos(cosine) / math.pi:.2f}", "degrés")

        return

    def define_add_bigram_func(self, add_bigram_func: Callable) -> None:
        """Méthode utilisée pour redéfinir la fonction d'ajout de bigrammes :

        Args :
            add_bigram_func (Callable) : Méthode à utiliser par l'objet pour ajouter un bigramme à un tableau

        Returns :
            (void) : Au retour, la méthode d'ajout de bigrammes a été redéfinie
        """
        self.add_bigram_f = add_bigram_func
        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de LaboProb2 :

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()
        self.input_dict = {}
        self.test_dict = {}
        self.add_bigram_f = None
        return
