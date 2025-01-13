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
import os
import math  # Au besoin, retirer le commentaire de cette ligne
import random # Au besoin, retirer le commentaire de cette ligne
from textan_common import TextAnCommon
import re

# ANSI color codes for console output
RESET = "\033[0m"  # Resets color
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

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
        self.rep_inconnues = ""
        self.oeuvres_inconnues = []
        self.oeuvre_inconnues = ""

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

    def get_inconnues_directory(self, inconnues_dir):
        cwd = os.getcwd()
        if os.path.isabs(inconnues_dir):
            self.rep_inconnues = inconnues_dir
        else:
            self.rep_inconnues = os.path.join(cwd, inconnues_dir)
        self.rep_inconnues = os.path.normpath(self.rep_inconnues)
        #self.oeuvres_inconnues = [f.path for f in os.scandir(self.rep_inconnues)
        #           if f.is_file() and f.name.endswith('.txt')]
        return

    @staticmethod
    def dot_product_dict(dict1: dict, dict2: dict) -> float:   # , dict1_size: int, dict2_size: int
        """Calcule le produit scalaire NORMALISÉ de deux vecteurs représentés par des dictionnaires

        Args :
            dict1 (dict) : le premier vecteur
            dict2 (dict) : le deuxième vecteur

        Returns :
            dot_product (float) : Le produit scalaire normalisé de deux vecteurs

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """

        # on a le size donner en param mais on en a pas besoin??

        #print("Methode du dot_product_dict")
        dot_prod = 0.0
        for hash_key in dict1.keys():  # Passe au travers de toutes les clés du dictionnaire
            #print(hash_key) #debug
            if hash_key in dict2:
                dot_prod += dict1[hash_key]['fréquences'] * dict2[hash_key]['fréquences']
        #print("dot_product_dict, valeur trouver: ", dot_prod)
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
        #print("Methode du dot_product_aut")
        dict_auteur1 = self.ngram_dict[auteur1]
        dict_auteur2 = self.ngram_dict[auteur2]

        # Fait le produit scalaire des deux dict
        dot_product = self.dot_product_dict(dict_auteur1, dict_auteur2)
        #print("dot_product_aut, valeur trouver: ", dot_product)
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

        #print("Methode du dot_product_dict_aut")

        dot_product = self.dot_product_dict(dict_oeuvre, self.ngram_dict[auteur])
        #print("dot_product_dict_aut, valeur trouver: ", dot_product)

        return dot_product

    def vector_size(self, vector: dict) -> float:
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
        #print("Methode vector_size")
        size = self.dot_product_dict(vector, vector)
        size = math.sqrt(size)
        #print("calcul vector_size:", size)
        return size

    def cosine(self, vector1: dict, vector2: dict) -> float:
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

        # Cosinus de l'angle c'est le produit scalaire de A & B diviser par la norme de A * norme de B
        #
        #print('Methode de cosine')
        #print("vector size:", self.vector_size(vector1))

        #print("vector size:", self.vector_size(vector2))
        #print(vector1, vector2, , )
        angle_cos = self.dot_product_dict(vector1, vector2) / (self.vector_size(vector1) * self.vector_size(vector2))
        #print('Angle de cosine trouver:', angle_cos)
        return angle_cos

    def find_author(self, oeuvre: str) -> []:
        """Après analyse des textes d'auteurs connus, retourner la liste d'auteurs
            et le niveau de proximité (un nombre entre 0 et 1) de l'œuvre inconnue
            avec les écrits de chacun d'entre eux

        Args :
            œuvre (str) : Nom du fichier contenant l'œuvre d'un auteur inconnu

        Returns :
            resultats (Liste[(string, float)]) : Liste de tuples (auteurs, niveau de proximité),
            où la proximité est un nombre entre 0 et 1)
        """
        self.get_inconnues_directory("")
        #print("Methode find_author")

        # Ouverture de l'oeuvre a tester
        print("ouverture de : ", oeuvre)

        self.oeuvre_inconnues = os.path.join(self.rep_inconnues, oeuvre)
        self.oeuvre_inconnues = os.path.normpath(self.oeuvre_inconnues)
        try:
            fichier_oeuvre = open(self.oeuvre_inconnues, "r", encoding="utf8")
        except Exception as e:  # si l'ouverture marche pas prend premier fichier du premier auteur juste pour tester
            print(f"Erreur lors de l'ouverture de {oeuvre}: {e}")
            oeuvre = self.get_aut_files(self.auteurs[0])[0]
            fichier_oeuvre = open(oeuvre, "r", encoding="utf8")

        lignes = fichier_oeuvre.readlines()
        ngram_list = self.generate_ngrams_from_lines(lignes)
        dict_inconnu = {"Mystère" : {} } #dict_inconnu = {"Mystère" : {} }

        for ngram in ngram_list:
            #print(dict_inconnu, ngram, "Mystère")
            self.add_ngram(dict_inconnu, ngram, "Mystère")
        fichier_oeuvre.close()


        # Calcul du cosine
        Auteur_Cosine = []

        #print("Liste d'auteurs : ",self.auteurs)
        for auteur in self.auteurs:
            #print("Comparaison avec auteur :", auteur)
            # calcul le cosinus
            # if auteur in self.ngram_dict:
            #     print("auteur is in dictionnary") #debug cad
            # else:
            #     print("auteur is not in dictionnary") #debug cad

            cosine_auteur = self.cosine(self.ngram_dict[auteur], dict_inconnu["Mystère"])

            # met les infos dans un tuple et append le tuple a la liste
            Auteur_Cosine.append((auteur, cosine_auteur))

        resultats = Auteur_Cosine

        # Affichage des resultats
        #print("liste des auteurs avec leurs cosine:")
        #for auteur, cosine_value in resultats:
        #    print(f"\t\t\t\t\t\t\t\t\t\t{auteur}: {cosine_value}")

        return resultats

    def get_ngram_occurrence(self, auteur: str, ngram) -> int:
        """Retourne le nombre d'occurrences du n-gramme pour cet auteur

        Args :
            auteur (string) : le nom de l'auteur
            ngram (objet de type ngram) : le n-gramme dont on désire la fréquence

        Returns :
            int : retourne le nombre d'occurrences du n-gramme pour l'auteur donné

        Copyright 2024-2025, F. Mailhot et Université de Sherbrooke
        """
        #print(ngram)
        ocurence = 0
        #list_ngram = ngram.split()
        for entry in self.ngram_dict[auteur]:
            if ngram == self.ngram_dict[auteur][entry]["n-gram"]:
                ocurence = self.ngram_dict[auteur][entry]["fréquences"]
                break
        #print("\t", self.ngram_size, auteur, ngram)
        return ocurence

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
        # print("\t", self.auteurs, auteur, taille, file=to_file)


        # chapitre 3 generation de texte et chaines de markov pour generation texte dans the practice of programming

        # liste de mots trier du plus au moins fréquent
        combined_ngram_dict = self.combine_ngram_ocurence(auteur)
        sorted_list = self.quicksort_dict(combined_ngram_dict)

        # choisir un mot de départ aléatoire
        starting_word = random.choice(sorted_list)[1] #il va falloir refaire la liste pour que ca soit du plus frequant au moins frequant car ca affecte les probabilie de random
        generated_text = starting_word

        # generation du texte en utilisant une chaine de markov (générée des mots jusqu'a atteindre le target de mot)

        # Chercher les n-grammes qui peuvent suivre le dernier mot (si possible)

        # Choisir un mot suivant de manière aléatoire
        next_word = " " #random.choice(next_ngram_candidates)
        generated_text.append(next_word)

        # Beautifier


        # Écrire le texte généré dans le fichier
        print(" ".join(generated_text), file=to_file)


        return

    def combine_ngram_ocurence(self, auteur: str)-> dict:
        combined_ngram_dict={}
        for hash_key in self.ngram_dict[auteur]:
            if self.ngram_dict[auteur][hash_key]["fréquences"] in combined_ngram_dict:
                combined_ngram_dict[self.ngram_dict[auteur][hash_key]["fréquences"]].append(self.ngram_dict[auteur][hash_key]["n-gram"])
                # ajoute élément à la fin de la liste
            else:
                combined_ngram_dict[self.ngram_dict[auteur][hash_key]["fréquences"]] = [] #crée une liste vide
                combined_ngram_dict[self.ngram_dict[auteur][hash_key]["fréquences"]].append(self.ngram_dict[auteur][hash_key]["n-gram"])
                #ajoute élément à la fin de la liste
        #print(combined_ngram_dict)
        return combined_ngram_dict

    # Function to find the partition position
    def partition(self, array, low, high):
        pivot = array[high]

        # pointer for greater element
        i = low - 1

        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if array[j] <= pivot:
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1

                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])

        # Swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])

        # Return the position from where partition is done
        return i + 1

    def quickSort(self, array, low, high):
        if low < high:
            # Find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = self.partition(array, low, high)

            # Recursive call on the left of pivot
            self.quickSort(array, low, pi - 1)

            # Recursive call on the right of pivot
            self.quickSort(array, pi + 1, high)

    def quicksort_dict(self, combined_dict: dict)-> dict:
        list_of_dict = list(combined_dict.items())
        # list[index][0] = fréquence
        # list[index][1] = ngrams de fréquence
        # print(list_of_dict)
        length = len(list_of_dict)
        self.quickSort(list_of_dict, 0, length - 1)
        return list_of_dict


    def get_kth_element(self, auteur: str, k: int) -> [[str]]:
        """Après analyse des textes d'auteurs connus, retourner le k-ième plus fréquent n-gramme de l'auteur indiqué

        Args :
            auteur (str) : Nom de l'auteur à utiliser
            k (int) : Indice du n-gramme à retourner

        Returns :
            ngram (List[Liste[string]]) : Liste de listes de mots composant le n-gramme recherché
            (il est possible qu'il y ait plus d'un n-gramme au même rang)
        """


        combined_ngram_dict = self.combine_ngram_ocurence(auteur)
        sorted_list = self.quicksort_dict(combined_ngram_dict)
        # print(sorted_list)
        # print("\t", self.auteurs, auteur, k)
        ngram = sorted_list[len(sorted_list) - k][1]  # Exemple du format de sortie pour trois bigrammes
        return ngram

    def generate_ngrams_from_lines(self, lines, punctuation=("!", "'", ";", ",", ".", "-", "?", "(", ")", "[", "]")):
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

    def add_ngram(self, ngram_dict: dict, n_gram, auteur) -> None:
        """Méthode appelée pour ajouter un bigramme au dictionnaire fourni :

                Args :
                    n_gram (Any) : object (arbitraire) qui représente un n-gram et qui est utilisé comme clé

                Returns :
                    (void) : Le nouveau n-gram est ajouté au dictionnaire de n-gram fourni
                """
        # if auteur == "Mystère":
        #     print(n_gram, auteur) #debug cad
        hash_n_gram_rentrant = self.__hash__(n_gram)  # techniquement déjà handle par python
        if hash_n_gram_rentrant in ngram_dict[auteur]:
            if self.__eq__(n_gram, ngram_dict[auteur][hash_n_gram_rentrant]["n-gram"]):
                ngram_dict[auteur][hash_n_gram_rentrant]["fréquences"] += 1
            else:  # existe seulement pour vérifier s'il a eu plus que 2 fois le même Bigram
                test = True
                while test:
                    hash_n_gram_rentrant += 1
                    if hash_n_gram_rentrant in ngram_dict[auteur]:
                        if self.__eq__(n_gram, ngram_dict[auteur][hash_n_gram_rentrant]["n-gram"]):
                            ngram_dict[auteur][hash_n_gram_rentrant]["fréquences"] += 1
                            test = False
                    else:
                        ngram_dict[auteur][hash_n_gram_rentrant] = {"n-gram": n_gram, "fréquences": 1}
                        test = False
        else:
            ngram_dict[auteur][hash_n_gram_rentrant] = {"n-gram": n_gram, "fréquences": 1}
        # print(n_gram)
        # print(self.ngram_dict)
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

        for auteur in self.auteurs:
            print(GREEN,"\t Ajout de ",CYAN, auteur,GREEN, "au dictionnaire 'ngram_dict'.",RESET)
            oeuvres = self.get_aut_files(auteur)
            self.ngram_dict[auteur]= {} #crée un dictionnaire vide pour chaque auteur
            for oeuvre in oeuvres:
                #ici on doit mettre les textes dans une variable afin des analyser.
                with open(oeuvre, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding

                    file_lines = file.readlines()  # List of lines
                    ngram_list = self.generate_ngrams_from_lines(file_lines)
                    for ngram in ngram_list:
                        self.add_ngram(self.ngram_dict, ngram, auteur)
            file.close()

            #print("dict complet: ", self.ngram_dict)

        # section pour test cad
        #print("Start test cad")
        #self.find_author("Gen_text_sol_1.txt") #ici il faudrait mettre le path d<un fichier d<auteur en param pour bien tester

        return

