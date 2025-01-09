#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le quatrième exercice du laboratoire - APP du cours GIF270

    L'exercice 4 touche les graphes et les éléments suivants :
        - Redéfinition de la création du graphe de proximité aux propriétés étendues
        - Redéfinition de l'ajout d'arcs entre les mots (noeuds) qui ne diffèrent que par le nombre donné de lettres
        - Redéfinition de l'ajout de mots aux masques dérivés

    Note :
        - Le traitement des arguments a été inclus dans la classe ParsingClass4, qui est utilisée dans le code principal
        - Tous les arguments requis sont présents et accessibles dans ParsingClass4.args
        - Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments

    Tests à effectuer avec le fichier fourni pour le laboratoire (mots-francais-sans-accent.txt) :

        1. Utiliser "barre" comme mot de départ et une distance de 29.

            - Utiliser les paramètres de ligne de commande suivants :
                -f mots-francais-sans-accent.txt -m barre -d 29

            - On observe alors un chemin entre "barre" et "eclat", qui est :

                (barre marre maire faire frire frere frene arene amene amere
                avere avare avale ovale orale orage otage etage etaie etais
                epais epris ecris ecrus echus echos eclos eclot eclat)

        2. Utiliser "barre" comme mot de départ, en permettant des mots de tailles différentes,
            et avec une distance de 29.

            - Utiliser les paramètres de ligne de commande suivants :
                -f mots-francais-sans-accent.txt -m barre -d 29 -D

            - On observe alors un chemin entre "barre" et "debrayait", qui est :

                (barre  marre  maree  mare  pare  paie  paien  paient  raient  iraient  riraient  friraient
                frisaient  faisaient  taisaient  tassaient  passaient  pansaient  pensaient  pendaient  rendaient
                reniaient  deniaient  defiaient  defraient  defrayent  defrayant  defrayait  debrayait)

        3. Utiliser "barre" comme mot de départ, en permettant une différence de 2 caractères entre les mots,
            et avec une distance de 29.

            - Utiliser les paramètres de ligne de commande suivants :
                -f mots-francais-sans-accent.txt -m barre -d 29 -wd 2

    Copyright 2018-2025, Frédéric Mailhot et Université de Sherbrooke

"""

from labo_prob4_common import LaboProb4Common


class LaboProb4(LaboProb4Common):
    """Classe à utiliser pour le quatrième exercice de laboratoire :

        - Contient le code pour créer le graphe de mots, tel qu'il apparaît dans le livre de référence
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

    def buildGraph2(self, word_file: str, word_distance: int, different_word_size: bool) -> None:
        """Création du graphe modifié de connectivité entre les mots

        Modification du code de la fonction buildGraph1() :
            - ajouter un arc entre des mots qui ne sont pas de la même longueur,
                mais qui ne diffèrent que par une lettre
            - ajouter un arc entre des mots qui diffèrent par 2, 3, ... lettres

        Doit produire un graphe où les noeuds représentent des mots et les arcs lient des mots
        qui ne diffèrent entre eux que du nombre de caractères demandé

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

    def __init__(self):
        """Initialisation d'une nouvelle instance de LaboProb4 :
            - Utilise l'initialisation de la classe héritée par LaboProb4 (ParsingClass4)

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()

        # Ajouter d'autres initialisations si nécessaire
        return


def main() -> None:
    """Démarrage de l'exercice 4 du labo :
        - Crée une instance de la classe LaboProb4, utilisée pour créer le graphe de mots
        - Crée le graphe de proximité à l'aide de la liste de mots
        - Effectue le test du code :
            - Trouve le mot passé en paramètre
            - Suit les chemins possibles à partir du mot de départ
            - Imprime la liste de mots adjacents à partir du mot de départ

    La méthode main() est déjà fonctionnelle et ne doit pas être modifiée

    Returns :
        (void) : Au retour, l'exécution est terminée
    """
    # Création de l'objet p4, qui contient la classe avec les fonctions nécessaires à l'exercice 4
    p4 = LaboProb4()

    # Création du graphe de proximité, en utilisant le fichier de mots passé en paramètre
    p4.buildGraph()
    print("Graph built")

    # Test des résultats obtenus à l'aide du graphe
    p4.testProb4()

    return


# Main : lecture des paramètres et appel des méthodes appropriées
if __name__ == "__main__":
    main()
