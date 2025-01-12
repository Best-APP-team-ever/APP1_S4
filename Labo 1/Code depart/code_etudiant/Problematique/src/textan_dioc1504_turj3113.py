#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Ce fichier contient la classe TextAn, à utiliser pour résoudre la problématique.
    C'est un gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers.

    Les méthodes apparaissant dans ce fichier définissent une API qui est utilisée par l'application
    de test test_textan.py
    Les paramètres d'entrée et de sortie (Application Programming Interface, API) sont définis,
    mais le code est à écrire au complet.
    Vous pouvez ajouter toutes les méthodes et toutes les variables nécessaires au bon fonctionnement du système

    La classe TextAn est invoquée par la classe TestTextAn (contenue dans test_textan.py) :

        - Tous les arguments requis sont présents et accessibles dans args (dans le fichier test_textan.py)
        - Note : vous pouvez tester votre code en utilisant les commandes :
            + "python test_textan.py"
            + "python test_textan.py -h" (donne la liste des arguments possibles)
            + "python test_textan.py -v" (mode "verbose", qui indique les valeurs de tous les arguments)

    Copyright 2018-2025, F. Mailhot et Université de Sherbrooke
"""
import io
# import math  # Au besoin, retirer le commentaire de cette ligne
# import random # Au besoin, retirer le commentaire de cette ligne
from textan_common import TextAnCommon
import re


class TextAn(TextAnCommon):
    """Classe à utiliser pour coder la solution à la problématique :

        - La classe héritée TextAnCommon contient certaines fonctions de base pour faciliter le travail :
            - recherche des auteurs
            - ouverture des répertoires
            - obtention de la liste des oeuvres d'un auteur (get_aut_files(auteur))
            - et autres (voir la classe TextAnCommon pour plus d'information)
        - Les interfaces du code à développer sont présentes, mais tout le code est à écrire
        - En particulier, il faut compléter les fonctions suivantes :
            - dot_product_dict (dict1, dict2)
            - dot_product_aut (auteur1, auteur2)
            - doct_product_dict_aut (dict, auteur)
            - get_ngram_occurrence (auteur, ngram)
            - get_total_occurrences (auteur)
            - find_author (oeuvre)
            - gen_text (auteur, taille, textname)
            - get_kth_element (auteur, k)
            - analyze()

    Copyright 2018-2025, F. Mailhot et Université de Sherbrooke
    """

    # Signes de ponctuation à traiter comme des mots (compléter cette liste incomplète)
    PONC = ["!", ";", ",", ".", "-", "?"] # pas vraiment utilisé à date, voir fonction generate_ngrams

    def __init__(self) -> None:
        """Initialize l'objet de type TextAn lorsqu'il est créé

        Args :
            (void) : Utilise simplement les informations fournies dans la classe TextAnCommon

        Returns :
            (void) : Ne fait qu'initialiser l'objet de type TextAn
        """

        # Initialisation des champs nécessaires aux fonctions fournies
        super().__init__()
        self.ngram_dict = {}
        self.ngram_list = []

        # Au besoin, ajouter votre code d'initialisation de l'objet de type TextAn lors de sa création
        # Ajouter les structures de données et les fonctions nécessaires à l'analyse des textes,
        # la production de textes aléatoires, la détection d'oeuvres inconnues,
        # l'identification des k-ièmes mots les plus fréquents.
        #
        # Les méthodes qui suivent doivent toutes être complétées pour que le système soit opérationnel
        # et que le harnais de test (test_textan.py) puisse exécuter tous les tests requis
        #
        return

    def __eq__(self, other: list, dict_ngram: list) -> bool:
        """Redéfinition de l'égalité entre deux bigrammes :
            - L'un des bigrammes est self (celui avec lequel __eq__ est appelé)
            - Le deuxième bigramme est other, fourni en paramètre

        Args :
            other (Bigram) : Le bigramme avec lequel il faut se comparer

        Returns :
            (bool) : Retourne True ou False, selon l'égalité entre les bigrammes
        """
        if isinstance(other, self.ngram_list.__class__):
                return dict_ngram == other #si les listes sont identiques return True
        return False

    def __hash__(self, ngram) -> int:
        """Redéfinition de la méthode de hachage d'un bigramme :
            - Doit utiliser les deux mots du bigramme

        Args :
            (void) : Toute l'information nécessaire (a et b) se trouve dans le bigramme

        Returns :
            (int) : Retourne la valeur de hachage
        """
        combo_string = "_".join(ngram)
        return hash(combo_string)

    @staticmethod
    def dot_product_dict(dict1: dict, dict2: dict, dict1_size: int, dict2_size: int) -> float:
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # on a le size donner en param mais on en a pas besoin??

        print("Methode du dot_product_dict")
        dot_prod = 0.0
        for hash_key in dict1.keys():  # Passe au travers de toutes les clés du dictionnaire
            #print(hash_key) #debug
            if hash_key in dict2:
                dot_prod += dict1[hash_key] * dict2[hash_key]
        print("dot_product_dict, valeur trouver: ", dot_prod)
        return dot_prod

    def dot_product_aut(self, auteur1: str, auteur2: str) -> float:
        """Calcule le produit scalaire normalisé entre les oeuvres de deux auteurs, en utilisant dot_product_dict()

        Args :
            auteur1 (str) : le nom du premier auteur
            auteur2 (str) : le nom du deuxième auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # Gerer par analyse:
        # Get les textes des auteurs
        # Extrait les ngram des textes
        # Ajoute les ngram au dicts
        # ainsi on assume que les deux dict sont deja bon
        print("Methode du dot_product_aut")
        dict_auteur1 = self.ngram_dict[auteur1]
        dict_auteur2 = self.ngram_dict[auteur2]

        # Fait le produit scalaire des deux dict
        dot_product = 0.0
        dot_product = self.dot_product_dict(dict_auteur1, dict_auteur2)
        print("dot_product_aut, valeur trouver: ", dot_product)
        return dot_product

    def dot_product_dict_aut(self, dict_oeuvre: dict, auteur: str) -> float:
        """Calcule le produit scalaire normalisé entre une oeuvre inconnue et les oeuvres d'un auteur,
           en utilisant dot_product_dict()

        Args :
            dict_oeuvre (dict) : la liste des n-grammes d'une oeuvre inconnue
            auteur (str) : le nom d'un auteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé des n-grammes de deux auteurs

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        print("Methode du dot_product_dict_aut")
        dot_product = 0.0

        dot_product = self.dot_product_dict(dict_oeuvre, self.ngram_dict[auteur])
        print("dot_product_dict_aut, valeur trouver: ", dot_product)

        return dot_product

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'oeuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            oeuvre (str) : Nom du fichier contenant l'oeuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """

        # La ligne suivante ne sert qu'à éliminer un avertissement.
        # Il faut la retirer lorsque le code est complété
        print("\tAuteurs: ", self.auteurs, "\n\tOeuvre: ", oeuvre)

        # Exemple du format des sorties
        resultats = [
            ("Premier_auteur", 0.1234),
            ("Deuxième_auteur", 0.1123),
        ]

        # Exemple de lecture du fichier oeuvre une ligne à la fois.  Modifier ou remplacer ce code par le vôtre.
        fichier_oeuvre = open(oeuvre, "r", encoding="utf8")
        lignes = fichier_oeuvre.readlines()
        plus_grande_ligne = ""
        for ligne in lignes:
            if len(ligne) > len(plus_grande_ligne):
                plus_grande_ligne = ligne
        print("\tPlus grande ligne: ", plus_grande_ligne.strip())

        # Ajouter votre code pour déterminer la proximité du fichier passé en paramètre avec chacun des auteurs
        # Retourner la liste des auteurs, chacun avec sa proximité au fichier inconnu
        # Plus la proximité est grande, plus proche l'oeuvre inconnue est des autres écrits d'un auteur
        #   Le produit scalaire entre le vecteur représentant les oeuvres d'un auteur
        #       et celui associé au texte inconnu pourrait s'avérer intéressant...
        #   Le produit scalaire devrait être normalisé avec la taille du vecteur associé au texte inconnu :
        #   proximité = (A dot product B) / (|A| |B|)   où A est le vecteur du texte inconnu et B est celui d'un auteur,
        #           "dot product" est le produit scalaire, et |X| est la norme (longueur) du vecteur X

        return resultats

    def get_ngram_occurrence(self, auteur: str, ngram: str) -> int:
        """Retourne le nombre d'occurrences du n-gramme pour cet auteur

        Args :
            auteur (string) : le nom de l'auteur
            ngram (objet de type ngram) : le n-gramme dont on désire la fréquence

        Returns :
            int : retourne le nombre d'occurrences du n-gramme pour l'auteur donné

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """
        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel
        print("\t", self.ngram_size, auteur, ngram)
        return 0

    def get_total_occurrences(self, auteur: str) -> int:
        """Retourne le nombre total d'occurrences de n-grammes pour cet auteur
            - Représente le total de n-grammes pour l'ensemble des oeuvres de cet auteur

        Args :
            auteur (string) : le nom de l'auteur

        Returns :
            int : retourne le nombre total d'occurrences pour l'auteur donné

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """
        # Les lignes qui suivent ne servent qu'à éliminer un avertissement.
        # Il faut les retirer et les remplacer par du code fonctionnel
        print("\t", self.ngram_size, auteur)
        return 1

    def gen_text_all(self, taille: int, to_file: io.TextIOWrapper) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques de l'ensemble des auteurs

        Args :
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """
        # Utilisez to_file pour y imprimer les mots générés, il s'agit d'un fichier vide, ouvert en écriture
        # Le print ne sert ici qu'à éliminer un avertissement. Il doit être adapté ou retiré
        print("\t", self.auteurs, taille, file=to_file)

        return

    def gen_text_auteur(self, auteur: str, taille: int, to_file: io.TextIOWrapper) -> None:
        """Après analyse des textes d'auteurs connus, produire un texte selon des statistiques d'un auteur

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            taille (int) : Taille du texte à générer
            textname (str) : Nom du fichier texte à générer.

        Returns :
            void : ne retourne rien, le texte produit doit être écrit dans le fichier "textname"
        """
        # Utilisez to_file pour y imprimer les mots générés, il s'agit d'un fichier vide, ouvert en écriture
        # Le print ne sert ici qu'à éliminer un avertissement. Il doit être adapté ou retiré
        print("\t", self.auteurs, auteur, taille, file=to_file)

        return

    def get_kth_element(self, auteur: str, k: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le k-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            k (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de listes de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """
        # Les lignes suivantes ne servent qu'à éliminer un avertissement.
        # Il faut les retirer lorsque le code est complété
        print("\t", self.auteurs, auteur, k)
        ngram = [["un", "roman"], ["le", "lac"], ["code", "est"]]  # Exemple du format de sortie pour trois bigrammes
        return ngram

    def generate_ngrams_from_lines(self, lines, punctuation=["!", "'", ";", ",", ".", "-", "?", "(", ")", "[", "]"]):
        """
        Generate n-grams from a list of lines, treating punctuation as individual words and preserving their order.

        Parameters:
            lines (list): A list of strings, where each string is a line of text.
            punctuation (list): List of punctuation characters to treat as words.

        Returns:
            list: A list of n-grams, where each n-gram is a list of `n` words.
        """
        # Define a regex pattern to split on spaces and treat punctuation as separate tokens
        pattern = r"(\s+|[" + re.escape("".join(punctuation)) + r"])"

        tokens = []  # Accumulate tokens from all lines

        for line in lines:
            # Normalize and split the line
            clean_line = line.strip()
            if not clean_line:  # Skip empty lines
                continue

            # Tokenize the line
            line_tokens = [token for token in re.split(pattern, clean_line) if token.strip()]
            tokens.extend(line_tokens)

        # Generate n-grams from the collected tokens
        ngrams=[]
        for i in range(0, len(tokens) - self.ngram_size + 1, self.ngram_size):
            ngram = tokens[i : (i + self.ngram_size)]
            ngrams.append(ngram)
        return ngrams

    def add_ngram(self, n_gram, auteur) -> None:
        """Méthode appelée pour ajouter un bigramme au dictionnaire fourni :

                Args :
                    n_gram (Any) : object (arbitraire) qui représente un n-gram et qui est utilisé comme clé

                Returns :
                    (void) : Le nouveau n-gram est ajouté au dictionnaire de n-gram fourni
                """
        # Ici, remplacez les prints par votre code.
        # Le tableau de hachage self.n_gram_dict devrait accumuler et compter les n-gram à mesure qu'on les ajoute.
        # On suppose qu'au départ, le tableau de hachage est vide

        hash_n_gram_rentrant = self.__hash__(n_gram)  # techniquement déjà handle par python
        if hash_n_gram_rentrant in self.ngram_dict[auteur]:
            if self.__eq__(n_gram, self.ngram_dict[auteur][hash_n_gram_rentrant]["n-gram"]):
                self.ngram_dict[auteur][hash_n_gram_rentrant]["fréquences"] += 1
            else:  # existe seulement pour vérifier s'il a eu plus que 2 fois le même Bigram
                test = True
                while test:
                    hash_n_gram_rentrant += 1
                    if hash_n_gram_rentrant in self.ngram_dict[auteur]:
                        if self.__eq__(n_gram, self.ngram_dict[auteur][hash_n_gram_rentrant]["n-gram"]):
                            self.ngram_dict[auteur][hash_n_gram_rentrant]["fréquences"] += 1
                            test = False
                    else:
                        self.ngram_dict[auteur][hash_n_gram_rentrant] = {"n-gram": n_gram, "fréquences": 1}
                        test = False
        else:
            self.ngram_dict[auteur][hash_n_gram_rentrant] = {"n-gram": n_gram, "fréquences": 1}
        #print(n_gram)
        #print(self.ngram_dict)
        return
    def analyze(self) -> None:
        """Fait l'analyse des textes fournis, en traitant chaque oeuvre de chaque auteur

        Args :
            void : toute l'information est contenue dans l'objet TextAn

        Returns :
            void : ne retourne rien, toute l'information extraite est conservée dans des structures internes
        """

        # Ajouter votre code ici pour traiter l'ensemble des oeuvres de l'ensemble des auteurs
        # Pour l'analyse : faire le calcul des fréquences de n-grammes pour l'ensemble des oeuvres
        #   d'un certain auteur, sans distinction des oeuvres individuelles,
        #       et recommencer ce calcul pour chacun des auteurs
        #   En procédant ainsi, les oeuvres comprenant plus de mots auront un impact plus grand sur
        #   les statistiques globales d'un auteur.
        # Il serait possible de considérer chacune des oeuvres d'un auteur comme ayant un poids identique.
        #   Pour ce faire, il faudrait faire les calculs de fréquence pour chacune des oeuvres
        #       de façon indépendante, pour ensuite les normaliser (diviser chaque vecteur par sa norme),
        #       avant de les additionner pour obtenir le vecteur complet d'un auteur
        #   De cette façon, les mots d'un court poème auraient une importance beaucoup plus grande que
        #   les mots d'une très longue oeuvre du même auteur. Ce n'est PAS ce qui vous est demandé ici.

        # Ces trois lignes ne servent qu'à éliminer un avertissement. Il faut les retirer lorsque le code est complété
        print("\t", self.auteurs)

        # Le code qui suit indique comment accéder aux noms des fichiers qui contiennent les oeuvres des auteurs.
        # Vous pouvez l'adapter pour effectuer l'analyse
        # for auteur in self.auteurs:
        #     for oeuvre in self.auteurs[auteur]:
        #         print(oeuvre)

        for auteur in self.auteurs:
            oeuvres = self.get_aut_files(auteur)
            self.ngram_dict[auteur]= {} #crée un dictionnaire vide pour chaque auteur
            for oeuvre in oeuvres:
                print("\t", oeuvre)
                #ici on doit mettre les textes dans une variable afin des analyser.
                with open(oeuvre, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
                    file_lines = file.readlines()  # List of lines
                    ngram_list = self.generate_ngrams_from_lines(file_lines)
                    for ngram in ngram_list:
                        self.add_ngram(ngram, auteur)
            print(self.ngram_dict[auteur])
        return

