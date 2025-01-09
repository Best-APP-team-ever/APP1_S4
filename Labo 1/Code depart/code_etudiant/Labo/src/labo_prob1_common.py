#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
    Code de base pour explorer le premier exercice du laboratoire - APP du cours GIF270

    L'exercice 1 touche le débogage et les éléments suivants :
        - Utilisation de points d'arrêt (breakpoints) pour l'identification de problèmes d'exécution et de logique
        - Identification du code qui modifie une valeur
        - Interruption d'exécution sans fin
        - Gestion de chaînes de caractères en format utf-8
        - Détection et traitement des exceptions

    Note :
        - Le traitement des arguments a été inclus dans la classe ParsingClass1, qui est utilisée dans le code principal
        - Tous les arguments requis sont présents et accessibles dans ParsingClass1.args
        - Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
        - La classe SmartFormatter permet d'imprimer correctement la chaîne de caractère "help" lorsqu'elle
          débute par "R|"

    Copyright 2023-2025 Frédéric Mailhot et Université de Sherbrooke

"""

import argparse
import traceback
from smart_formatter_common import SmartFormatter
from handle_unicode_common import HandleUnicodeCommon
from debug_handler_common import DebugHandler


class ConfigData:
    def __init__(self, num: int) -> None:
        """Initialisation d'une nouvelle instance de ConfigData :
            - Ajoute trois champs avec leurs valeurs par défaut

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        self.number = num
        self.add: bool = True
        self.new: int = 0
        return


class ParsingClass1(HandleUnicodeCommon, DebugHandler):
    """Création d'un parser prédéfini pour lire les paramètres de la ligne de commande pour le premier exercice
"""

    def setup_and_parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog='Labo1:Exercice1.py', formatter_class=SmartFormatter)
        parser.add_argument('-p', default=1, type=int,
                            help="R|"
                                 "Type de problème à débugger (par défaut, 1):\n"
                                 "  1: factorielle,\n"
                                 "  2: problème d\'exécution,\n"
                                 "  3: long calcul,\n"
                                 "  4: comparaison de chaînes de caractères Unicode,\n"
                                 "  5: Exceptions\n"
                                 "      Par défaut: exceptions non traitées\n"
                                 "      Utiliser -e pour utiliser le code de traitement existant (mais incomplet)")
        parser.add_argument('-e', action='store_true',
                            help='Indique l\'utilisation de code de traitement des exceptions, \\'
                                 'à utiliser avec l\'option "-p 4"')
        parser.add_argument('-fact', default=30, type=int, help='Valeur de factorielle à calculer (par défaut, 30)')
        parser.add_argument('-fact_end', default=0, type=int,
                            help='Valeur de fin de récursion de la factorielle (par défaut, 0)')
        parser.add_argument('-val', default=30, type=int, help='Valeur à utiliser pour le long calcul (par défaut, 30)')
        parser.add_argument('-val_end', default=0, type=int, help='Valeur de fin du long calcul (par défaut, 0)')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        self.parser = parser
        self.args: argparse.Namespace = parser.parse_args()
        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de ParsingClass1 :
            - Ajoute toutes les valeurs par défaut des paramètres utilisés
            - Modifie les valeurs redéfinies sur la ligne de commande

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()
        self.parser: argparse.ArgumentParser = None
        self.args: argparse.Namespace = None
        self.config: ConfigData = None
        self.word1, self.word2 = self.get_strings()
        self.setup_and_parse_cli()
        self.config: ConfigData = ConfigData(42)

        # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
        if self.args.v:
            print("")
            print("Mode verbose:")
            print("Type de problème à déboguer: ", self.args.p)
            match self.args.p:
                case 1:
                    print("Calcul de factorielle:")
                    print("\tFactorielle de ", self.args.fact)
                case 2:
                    print("Exécution problématique d'une méthode")
                case 3:
                    print("Long calcul:")
                    print("\tSomme des entiers plus petits ou égaux à ", self.args.val)
                case 4:
                    print("En Unicode (utf-8): chaînes de caractères différentes ou égales?")
                case 5:
                    if self.args.e:
                        print("Utilisation du code de traitement des exceptions")
                    else:
                        print("N'utilise pas le code de traitement des exceptions")
                case _:
                    print("Type de problème à déboguer inconnu (doit être 1,2,3,4 ou 5)")
            print("")
        return


