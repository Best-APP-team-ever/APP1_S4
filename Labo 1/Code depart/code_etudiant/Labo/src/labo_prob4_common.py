#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le quatrième exercice du laboratoire - APP du cours GIF270

    L'exercice 4 touche les graphes et les éléments suivants :
        - Redéfinition de la création du graphe de proximité

    Note :
        - Le traitement des arguments a été inclus dans la classe ParsingClass4, qui est utilisée dans le code principal
        - Tous les arguments requis sont présents et accessibles dans ParsingClass4.args
        - Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments

    Copyright 2018-2025, Frédéric Mailhot et Université de Sherbrooke

"""

import sys
import argparse
from pythonds3 import Vertex
from pythonds3 import Graph


class ParsingClass4:
    """Création d'un parser prédéfini pour lire les paramètres de la ligne de commande pour le quatrième exercice

    """

    def setup_and_parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """

        parser = argparse.ArgumentParser(prog='GIF270 Labo1:Exercice4.py')
        parser.add_argument('-f', required=True, help='Fichier contenant la liste de mots')
        parser.add_argument('-m', required=True, help='Mot de départ')
        parser.add_argument('-d', required=True, help='Distance du mot de départ')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        parser.add_argument('-wd', default=1, help='Nombre maximal de caractères différents entre les mots')
        parser.add_argument('-D', action='store_true', help='Permet des mots de taille différente')
        parser.add_argument('-max', default=10, help='Nombre maximal de listes à imprimer')
        self.parser: argparse.ArgumentParser = parser
        self.args: argparse.Namespace = self.parser.parse_args()

        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de ParsingClass4 :
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
            print("Fichier de mots utilisé: " + self.args.f)
            print("Mot de départ: " + self.args.m)
            print("Distance du mot de départ: " + self.args.d)
            print("Nombre maximal de caractères différencts entre les mots: " + str(self.args.wd))
            if self.args.D:
                print("Utilisation possible de mots de taille différente dans l'échelle de mots")
            else:
                print("Tous les mots de l'échelle de mots seront de même taille")
            print("Nombre maximal de listes de mots: " + str(self.args.max))
        return


class LaboProb4Common(ParsingClass4):
    """Classe de test pour valider le code de l'échelle de mots
        - Classe hérite de ParsingClass4, qui lit les paramètres de la ligne de commande
        - Plusieurs des méthodes définies ici sont incomplètes et doivent être redéfinies dans la classe LaboProb4
    """

    def addEdgesBetweenAdjacentWords(self) -> None:
        """Refactorisation du code tiré de la section 8.8, pour partager l'ajout d'arcs entre buildGraph et buildGraph2

        Args :
            (void) :  Les champs suivants sont utilisés, étant directement disponibles dans l'objet self

            g (Graph) : Graphe contenant les noeuds à traiter
            masks (dict) : Dictionnaire des clés utilisées (masques, par exemple : "_abc", "_bc", etc.)

        Returns :
            (void) : Les arcs sont ajoutés directement dans le graphe

        """
        # Ajouter un arc entre tous les mots qui se trouvent dans le même masque
        # Pour chaque paire de mots différents dans un certain masque, ajouter un arc :
        #       self.g.add_edge devrait être utile
        for mask in self.masks.keys():
            # Traiter toutes les paires de mots différents se trouvant dans un certain masque
            # Remplacer le print par le code approprié
            print(mask)
        return

    def addWordToMask(self, mask: str, word: str) -> None:
        """Refactorisation du code tiré de la section 8.8, pour partager l'ajout de mots dans les masques

        Args :

            mask (str) : Masque auquel ajouter un mot qui a produit ce masque
            word (str) : Mot à l'origine du masque

        Returns :
            (void) : Le mot est ajouté au masque, dans le dictionnaire

        """
        # Ajouter le mot au masque dérivé de ce mot
        # Remplacer les prints par le code approprié
        if mask in self.masks:
            print("Ajout d'un mot à un masque existant", mask, word)
        else:
            print("Ajout d'un mot à un nouveau masque", mask, word)
        return

    def buildGraph1(self, word_file: str) -> None:
        """Création du graphe de connectivité entre les mots

        Code tiré de la section 8.8 du livre de référence
        Voir : <https://runestone.academy/ns/books/published/GIF270/Graphs/BuildingtheWordLadderGraph.html>

        À adapter pour l'exercice :
            - ajouter un arc entre des mots qui ne sont pas de la même longueur,
                mais qui ne diffèrent que par une lettre
            - optionnel : permettre des arcs entre des mots qui diffèrent
                par 2, 3, 4, etc. lettres (indiqué sur la ligne de commande)

        Produit un graphe où les noeuds représentent des mots et les arcs lient des mots qui ne diffèrent entre eux
        que du nombre de caractères demandé

        Args :
            word_file (str) : Nom du fichier de mots à étudier

        Returns :
            (void) : L'objet comprend le graphe qui contient tous les mots, avec des arcs entre les mots qui sont liés
        """

        w_file = open(word_file, 'r')
        # create buckets of words that differ by one letter
        for line in w_file:
            word = line[:-1]
            for i in range(len(word)):
                mask = word[:i] + '_' + word[i + 1:]
                self.addWordToMask(mask, word)
        # Ajouter les noeuds et les arcs pour les mots qui apparaissent dans le même masque
        self.addEdgesBetweenAdjacentWords()

        return

    def getWordMask(self, word: str, distance: int, start_point, init_word) -> None:
        """Énumération de masques (de type *abc, a*bc, ab*c, abc*, *bc, a*c, ab*)

        Code adapté pour l'exercice :
            - ajout d'un arc entre des mots qui ne sont pas de la même longueur, mais qui ne diffèrent que par une lettre
            - ajout d'arcs entre des mots qui diffèrent par 2, 3, ... lettres (indiqué sur la ligne de commande)

        Produit (de façon récursive) tous les masques appropriés

        Args :
            word (str) : mot à traiter
            distance (int) : nombre maximum de caractères différents permis entre deux mots adjacents
            start_point () :
            init_word (str) :

        Returns :
            (void) : tous les masques nécessaires sont ajoutés aux structures passées en paramètres

        """
        if distance > len(
                word):  # Situation où la différence de caractères permise est plus grande que la taille du mot
            distance = len(word)
        if distance == 0:
            return
        for i in range(start_point, len(word)):
            mask = word[:i] + '_' + word[i + 1:]
            self.getWordMask(mask, distance - 1, i + 1, init_word)
            self.addWordToMask(mask, word)
        return

    def buildGraph2(self, word_file: str, word_distance: int, different_word_size: bool) -> None:
        """Création du graphe modifié de connectivité entre les mots

        Modification du code de la fonction buildGraph1() :
            - ajouter un arc entre des mots qui ne sont pas de la même longueur,
                mais qui ne diffèrent que par une lettre
            - ajouter un arc entre des mots qui diffèrent par 2, 3, ... lettres

        Doit produire un graphe où les noeuds représentent des mots et les arcs lient des mots qui ne diffèrent entre eux
        que du nombre de caractères demandé

        Args :
            wordFile (str) : Nom du fichier de mots à étudier
            wordDistance (int) : Nombre maximum de caractères différents permis entre 2 mots adjacents dans l'échelle
            different_word_size (bool) : Indique qu'on permet (ou non) des mots de tailles différentes

        Returns :
            (void) : Au retour, l'objet contient le nouveau graphe tous les mots,
                    avec des arcs entre les mots qui sont liés
        """

        w_file = open(word_file, 'r')
        # Pour cette méthode, vous pouvez vous inspirer du code de buildGraph() défini dans labo_prob4_common.py
        # Le code de buildGraph est directement adapté du code de la section 8.8 du livre de référence
        #
        # Créer des masques pour que les mots puissent différer de 1 à wordDistance caractères
        # Pour chacun des mots du fichier de mots à étudier :
        #   - Utiliser getWordMask pour générer tous les masques utiles :
        #       - mot d'origine où chacune des lettres est remplacée à tour de rôle par "_" (pour créer un masque)
        #       - mot étendu, où une "pseudo-lettre" est ajoutée au début ("_" ajouté avant le début du mot)
        #           et une "pseudo-lettre" est ajoutée à la fin ("_" ajouté après la fin du mot)
        #       - getWordMask est un appel récursif qui ajoute les mots dans les masques au fut et à mesure
        #   - Utiliser addWordToMask sur le mot étendu par les "pseudo-lettre" au début ou à la fin
        for line in w_file:
            word = line[:-1]
            # Ajouter le mot de départ dans un ensemble de masques (getWordMask pourrait être utile)
            # Remplacer le print par l'appel approprié
            print(word, word_distance)
            # Ajouter des entrées si des mots de taille différente sont permis :
            #   getWordMask et addWordToMask devraient être utiles
            # Remplacer le print par les appels appropriés
            if different_word_size:
                print('_' + word, word_distance)

        # Ajouter les arcs entre les mots qui apparaissent dans le même masque
        # Remplacer le print par le code approprié
        #   addEdgesBetweenAdjacentWords pourrait s'avérer utile
        print("Ajout des arcs entre les mots adjacents")

        return

    def buildGraph(self) -> None:
        if (self.args.wd == 1) and not self.args.D:
            self.buildGraph1(self.args.f)
            if self.args.v:
                print("Graphe créé")
        else:
            # Création du graphe de proximité avec des capacités étendues
            #       (mots de taille différente, plus d'un caractère de différent)
            self.buildGraph2(self.args.f, int(self.args.wd), self.args.D)
            if self.args.v:
                print("Graphe étendu créé")
        return

    def findWord(self, start_word: str) -> Vertex:
        """Retourne le noeud (vertex) qui correspond au mot passé en paramètre

        Args :
            start_word (str) : Mot de départ

        Returns :
            (Vertex) : Retourne le noeud recherché
        """
        return self.g.get_vertex(start_word)

    def SetMaxDistance(self) -> None:
        """Annotation de tous les noeuds avec la distance maximale. Utile avant d'établir la distance avec le mot de départ

        Args :
            (void) : Le graphe contenant tous les mots est contenu dans self.g

        Returns :
            (void) : Tous les noeuds du graphe sont annotés avec la distance maximale, mais rien n'est retourné
        """
        vertex_list = self.g.get_vertices()
        for v in vertex_list:
            self.g.get_vertex(v).set_distance(sys.maxsize)
        return

    def markPath(self, current_vertex: Vertex, current_depth: int, current_distance: int) -> None:
        """Annotation de tous les noeuds du graphe avec la distance la plus courte à partir du mot donné en paramètre :
                - Marquer le chemin (distance) à partir du noeud courant et de la distance courante
                - Si un noeud voisin obtient une distance plus petite, le mettre à jour et le traiter
                - Sinon (noeud voisin a déjà une distance assez petite), ne pas traiter ce noeud
                - Considérer la distance maximale permise (currentDepth), pour limiter l'exploration du graphe
                - Si la distance maximale permise est négative, cette méthode s'arrêtera lorsque tous les noeuds auront été traités

        Args :
            current_vertex (Vertex) : Noeud à traiter
            current_depth (int) : Distance maximale à étudier (cesser l'analyse lorsque ce nombre est à 0)
            current_distance (int) : Distance courante du noeud (mot) de départ

        Returns :
            (void) : Les noeuds du graphe sont annotés, mais rien n'est retourné

        """
        if current_vertex is None:  # Si ce noeud est nul (le mot utilisé n'a pas de voisin)
            return
        current_vertex.set_distance(current_distance)
        if current_depth == 0:
            return
        else:
            neighbor_list = current_vertex.get_neighbors()
            for v in neighbor_list:
                if v.get_distance() > current_distance + 1:
                    self.markPath(v, current_depth - 1, current_distance + 1)
        return

    def storeWordDistances(self) -> None:
        for word in self.g.get_vertices():
            v = self.findWord(word)
            distance = v.get_distance()
            if distance < sys.maxsize:
                if distance in self.wordDistanceDict:
                    self.wordDistanceDict[distance].append(v.key)
                else:
                    self.wordDistanceDict[distance] = [v.key]

        if self.args.v:
            print('Nombre de mots à une distance X du mot: ' + self.args.m)
            keys = list(self.wordDistanceDict)
            keys.sort()
            for key in keys:
                print(str(key) + ": " + str(len(self.wordDistanceDict[key])))

        return

    def printRecurWithPrev(self, v: Vertex) -> None:
        d = v.get_distance()
        if d == 0:
            print(v.key, " ", end='')
            return
        for prev in v.get_neighbors():
            if prev.get_distance() == (d - 1):
                self.printRecurWithPrev(prev)
                print(v.key, " ", end='')
                break
        return

    def printFromWordDistance(self) -> None:
        keys = list(self.wordDistanceDict)
        keys.sort()
        for key in keys:
            print("")
            print("Chaîne de longueur : " + str(key + 1))
            for word in self.wordDistanceDict[key]:
                self.printRecurWithPrev(self.findWord(word))
                break
        return

    # Imprimer tous les chemins de longueur currentDistance depuis le noeud current_vertex
    # Si max_distance est atteint, arrêter

    def printPath(self, current_vertex: Vertex, max_distance: int, vertex_list: list) -> None:
        """Impression à l'écran de l'ensemble des chemins ayant la distance requise (à partir du mot de départ)

        Args :
            current_vertex (Vertex) : Noeud à traiter
            max_distance (int) : Distance maximale à imprimer (cesser lorsque ce nombre est à 0)
            vertex_list (Liste[Vertex]) : liste des noeuds dans le chemin parcouru jusqu'ici

        Returns :
            (void) : Tout le travail est fait par la fonction récursive _prinPath()
        """

        print("")
        print("Séquence de mots à partir du mot de départ: " + self.args.m)
        self._printPath(current_vertex, max_distance, 0, vertex_list, 0)
        return

    def _printPath(self, current_vertex: Vertex, max_distance: int, current_distance: int,
                   vertex_list: list, how_many_produced: int) -> None:
        """ Fonction interne recursive pour l'impression à l'écran de l'ensemble des chemins
            ayant la distance requise (à partir du mot de départ)

        Args :
            current_vertex (Vertex) : Noeud à traiter
            max_distance (int) : Distance maximale à imprimer (cesser lorsque ce nombre est à 0)
            current_distance (int) : Distance courante du noeud (mot) de départ
            vertex_list (Liste[Vertex]) : liste des noeuds dans le chemin parcouru jusqu'ici
            how_many_produced (int) : Nombre de listes imprimées jusqu'à présent

        Returns :
            (void) : Les noeuds du graphe sont annotés, mais rien n'est retourné
        """
        if current_distance == max_distance:
            print(vertex_list)
            self.HowManyProduced += 1
            return
        else:
            if current_vertex is None:  # Si ce noeud est nul (le mot utilisé n'a pas de voisin)
                return
            neighbor_list = current_vertex.get_neighbors()
            for v in neighbor_list:
                if v.get_distance() == current_distance + 1:
                    vertex_recur_list = vertex_list + " " + v.key
                    self._printPath(v, max_distance, current_distance + 1, vertex_recur_list, how_many_produced)
                    if self.HowManyProduced >= self.nbre_max:
                        return
        return

    def testProb4(self) -> None:
        # Recherche du noeud (vertex v, qui est une chaîne de caractères) qui correspond au mot de départ
        v = self.findWord(self.args.m)

        # Annotation de tous les noeuds avec la distance maximale
        self.SetMaxDistance()

        # Annotation des noeuds adjacents au noeud de départ avec la distance minimale
        self.markPath(v, int(self.args.d) - 1, 0)

        # Ajout dans un dictionnaire de tous les mots se situant à une certaine distance
        self.storeWordDistances()

        # Impression des chemins (sequence de mots) à partir du mot de depart,
        #   jusqu'à la distance maximale (en paramètre)
        self.vertex_list = self.args.m
        self.printPath(v, int(self.args.d) - 1, self.vertex_list)
        self.printFromWordDistance()

        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de LaboProb4 :
            - Utilise l'initialisation de la classe héritée par LaboProb4Common (ParsingClass4)

        Returns :
            (void) : Au retour, l'objet est initialisé

        """
        super().__init__()

        self.nbre_max: int = self.args.max

        #  self.masks (dict) : Dictionnaire comprenant éventuellement tous les masques ("_abc", "xy_z", etc.)
        self.masks = {}

        self.vertex_list: str = None

        #  self.g (Graph) : Graphe avec les mots comme noeuds et les liens entre les mots adjacents comme arcs
        self.g: Graph = Graph()

        self.wordDistanceDict = {}
        self.HowManyProduced = 0
        return

