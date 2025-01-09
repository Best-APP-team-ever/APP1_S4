#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le premier exercice du laboratoire - APP du cours GIF270

    L'exercice 1 touche le débogage et les éléments suivants :
        - Utilisation de points d'arrêt (breakpoints) pour l'identification de problèmes d'exécution et de logique
        - Interruption d'exécution sans fin
        - Détection et traitement des exceptions

    Copyright 2023-2025 Frédéric Mailhot et Université de Sherbrooke

"""
from labo_prob1_common import ParsingClass1, ConfigData
from watchpoints import watch


class LaboProb1(ParsingClass1):
    """Création d'un ensemble de méthodes qui ont des comportements problématiques
        - Classe hérite de ParsingClass1, qui lit les paramètres de la ligne de commande
        - Les paramètres sont accessibles dans mp.args
        - Méthodes incluses : factorielle, times2, long_calcul, compare_strings, exceptions
    """

    def factorielle(self, n: int) -> int:
        """Calcul de factorielle :
            - Appel récursif (sur n, n-1, n-2, ...)
            - La fin de la récursion est déterminée par le champ fact_end

        Args :
            n (int) : Le nombre pour lequel on cherche la factorielle

        Returns :
            (long) : La valeur de (n!)
        """
        if n > self.args.fact_end: #changement fait >= à >
            fact = n * self.factorielle(n - 1)
            return fact
        return 1

    def times2(self) -> int:
        """Calcul du double de la valeur self.args.val :
            - Compare à la valeur contenue dans la structure de configuration, mise à jour au besoin

        Args :
            (void) : Pas de paramètre en entrée

        Returns :
            (long) : La valeur de (2 * self.args.val)
        """
        #if self.config.number != self.args.val:
            #self.config.number = self.args.val
        return 2 * self.args.val

    def prepare(self) -> None:
        """Préparation de l'objet de type LaboProb1 :
            - Retrait du champ config

        Args :
            (void) : Aucun paramètre en entrée, on utilise l'objet lui-même

        Returns :
            (void) : Aucune valeur de retour
        """
        self.config: ConfigData = None
        return

    def long_calcul(self) -> int:
        """Long calcul :
            - Calcule val + (val-1) + (val-2) + ... + 1
            - val est tirée de l'objet lui-même (self.args.val)

        Args :
            (void) : La valeur utilisée provient de l'objet lui-même

        Returns :
            (long) : Le résultat du calcul
        """
        a: int = self.args.val
        a2 = a
        res = 0
        while a > self.args.val_end:
            res += a
            a -= 1
        res = int((a2*(a2-1))/2)+a2
        return res

    def compare_strings(self):
        """Comparaison de chaînes de caractères utf-8 :
            - Deux chaînes de caractères sont d'apparence identique (lorsqu'on les utilise dans un print()),
              mais leur comparaison indique qu'elles ne le sont pas

       Args :
           (void) : Les chaînes de caractères proviennent de l'objet lui-même

       Returns :
           (void) : Aucun résultat à retourner
       """

        if self.word1 == self.word2:
            print("Les chaînes de caractères \"", self.word1, "\" et \"", self.word2, "\" sont égales.", flush=True, sep="")
        else:
            print("Les chaînes de caractères \"", self.word1, "\" et \"", self.word2, "\" ne sont PAS égales!", flush=True, sep="")
        return

    def exceptions(self) -> None:
        """Exploration de diverses exceptions :
            - Par défaut, aucun traitement des exceptions
            - Si le paramètre -e est donné en ligne de commande, utiliser les (try/except) pour traiter les exceptions
            - Les (try/except) utilisés ne sont pas associés aux bonnes exceptions. Vous devez les corriger

        Args :
            (void) : Tous les calculs sont faits à partir de valeurs locales

        Returns :
            (void) : Aucune valeur de retour
        """
        a: int = 5
        b: int = 0
        c: str = str(b)
        ma_liste = [0, 1, 2, 3]

        if self.args.e is None:
            x = a / b
            print("x = ", x)
            print("Liste[5]", ma_liste[5])
            filename = "mon_fichier.txt"
            mon_fichier = open(filename, "r")
            print(mon_fichier.read())
            return

        try:
            x = a / b
            print(x)
        except ZeroDivisionError:
            print("Problème dans la division de a/b: a =", a, ", b =", b)
            self.print_debug_info()

        try:
            print("y = ", y)
        except NameError:
            print("Variable y non définie")
            self.print_debug_info()

        try:
            print("y = ", a + c)
        except TypeError:
            print("Erreur de type: impossible d'additionner un entier et une chaîne de caractères")
            self.print_debug_info()

        try:
            print("Liste[5]", ma_liste[5])
        except IndexError:
            print("Index trop grand")
            self.print_debug_info()

        filename = "mon_fichier.txt"
        try:
            mon_fichier = open(filename, "r")
            print(mon_fichier.read())
        except FileNotFoundError:
            print("Fichier", filename, "inexistant")
            self.print_debug_info()
        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de LaboProb1 :
            - Utilise l'initialisation de la classe héritée par LaboProb1 (ParsingClass1)

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        self.config: ConfigData = None
        super().__init__()
        return


def main() -> None:
    """Démarrage de l'exercice 1 du labo :
        - Crée une instance de la classe LaboProb1, utilisée pour présenter différents problèmes à déboguer
        - Utiliser le paramètre -p (1, 2, 3, 4 ou 5) pour déterminer quel problème observer
        - Utiliser le paramètre -e de concert avec -p 5
                pour démarrer le traitement des exceptions inclus (mais à corriger)

    Returns :
        (void) : Au retour, l'exécution est terminée
    """
    p1 = LaboProb1()
    #watch(p1)
    #watch(p1.config)
    p1.word1 = p1.normalize_string(p1.word1)
    p1.word2 = p1.normalize_string(p1.word2)
    match p1.args.p:
        case 1:
            print("Exercice 1, 1er test: est-ce que le résultat du calcul de la factorielle est valide?", flush=True)
            print(p1.args.fact, "! = ", p1.factorielle(p1.args.fact), sep='')
        case 2:
            p1.prepare()
            print("Exercice 1, 2e test: Est-ce que l'exécution de la méthode est un succès?", flush=True)
            print(p1.args.val, "fois 2 = ", p1.times2())
        case 3:
            print("Exercice 1, 3e test: Est-ce que le long calcul se terminera un jour?", flush=True)
            print("Résultat du long calcul = ", p1.long_calcul())
        case 4:
            print("Exercice 1, 4e test: Est-ce que les chaînes de caractères sont égales ou différentes?")
            p1.compare_strings()
        case 5:
            print("Exercice 1, 5e test: Pouvez-vous identifier ", end="")
            print("les exceptions pour qu'elles soient traitées adéquatement?", flush=True)
            p1.exceptions()
        case _:
            print("Exercice 1, type de problème à déboguer inconnu (doit être 1,2,3,4 ou 5)")
    return


if __name__ == "__main__":
    main()
