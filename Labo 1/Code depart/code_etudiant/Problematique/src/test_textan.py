#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Programme python pour l'évaluation du code de détection des auteurs et de génération de textes

    Copyright 2018-2025 F. Mailhot et Université de Sherbrooke
"""
import copy
import importlib
import os.path
import sys
from typing import Any
from tabulate import tabulate

from test_textan_parsing import ParsingClassTextAn
from test_textan_command import *
from text_beautifier import TextBeautifier


class TestTextAn(ParsingClassTextAn):
    """Classe à utiliser pour valider la résolution de la problématique :

        - Contient tout le nécessaire pour tester la problématique.

    Pour valider la solution de la problématique, effectuer :
        - python test_textan.py -help
            + Indique tous les arguments et options disponibles

    Copyright 2018-2025, F. Mailhot et Université de Sherbrooke
    """

    @staticmethod
    def add_cwd_to_sys_path() -> None:
        """Ajoute le répertoire d'exécution local aux chemins utilisés par le système.
           Sinon, si test_textan.py est un lien symbolique, les fichiers textan_CIP1_CIP2.py ne sont pas trouvés

        Args :
            (void) : Utilisation des informations système

        Returns :
            (void) : Au retour, le répertoire d'exécution est ajouté au chemin système
        """
        sys.path.append(os.getcwd())
        return

    @staticmethod
    def sort_author_distance(author_res: [str, float]) -> float:
        """Retourne le deuxième élément du vecteur (auteur, proximité) (utilisé pour le tri de la liste des auteurs)

        Args :
            ([str, float]) : Liste des auteurs et valeur de proximité avec le texte inconnu
            (résultat du produit scalaire) pour chacun des auteurs

        Returns :
            (float) : Valeur de la proximité de l'auteur avec le texte inconnu
        """
        return author_res[1]

    # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    def print_params(self) -> None:
        """Mode verbose, imprime l'ensemble des paramètres utilisés pour ce test :
            - Valeur des paramètres par défaut s'ils n'ont pas été modifiés sur la ligne de commande
            - Ensemble des tests demandés

        Returns :
            (void) : Ne fait qu'imprimer les valeurs contenues dans self
        """
        if not self.args.v:
            return

        print("Mode verbose: ", self.cip)

        if self.args.f:
            print("\tFichier inconnu à étudier: " + self.args.f)
        if self.oeuvre:
            print(f"\tChemin complet de l'oeuvre inconnue: {self.oeuvre}")

        print("\tCalcul avec des " + str(self.args.m) + "-grammes")

        if self.args.F:
            if self.args.F == 1:
                print("\tLe premier ngramme le plus fréquent sera trouvé")
            else:
                print(
                    "\tLe "
                    + str(self.args.F)
                    + "e ngramme le plus fréquent sera trouvé"
                )

        if self.args.a:
            print("\tAuteur étudié: " + self.args.a)

        if self.args.noPonc:
            print("\tRetrait des signes de ponctuation")
        else:
            print("\tConservation des signes de ponctuation")

        if self.args.G:
            print(
                "\tGénération d'un texte de "
                + str(self.args.G)
                + " mots, pour l'auteur: ",
                self.auteur,
            )
            print("\tLe nom du fichier généré sera: " + self.get_gen_file_name())

        if self.args.recursion:
            print("\tRécursion maximale: ", sys.getrecursionlimit())
        print("\tTemps d'exécution maximal: ", self.timeout, " secondes")

        print("\tCalcul avec les auteurs du répertoire: " + self.args.d)
        print("\tListe des auteurs: ", end="")
        self.auteurs.sort()
        for a in self.auteurs:
            aut = a.split("/")
            print("    " + aut[-1], end=" ")
        print("")
        if self.args.compare_auteurs:
            print("\tLa proximité des textes de l'ensemble des auteurs sera calculée")

        return

    def setup_instance_param(self) -> None:
        """Définit les paramètres de l'instance (étudiante) à tester

        Returns :
            (void) : Rien n'est retourné
        """
        # Ajout de l'information nécessaire dans l'instance à tester de la classe TextAn sous étude
        self.textan.set_ngram_size(self.ngram_size)
        self.textan.set_aut_dir(self.dir)

        self.auteurs = self.textan.auteurs
        self.print_params()  # Imprime l'état de l'instance (si le mode verbose a été utilisé sur la ligne de commande)
        return

    def get_gen_file_name(self) -> str:
        """Définit le nom du fichier à générer

        Returns :
            name (str) : Nom du fichier à générer
        """
        name = self.gen_basename
        if self.g_cip:
            name = name + self.g_sep + self.cip
        if self.g_aut:
            name = name + self.g_sep + self.auteur
        if self.g_ext:
            name = name + self.g_ext
        return name

    def get_cips(self) -> None:
        """Lit le fichier etudiants.txt, trouve les CIPs, et retourne la liste
           Le CIP est obtenu du fichier etudiants.txt, dans le répertoire courant
            ou tel qu'indiqué en paramètre (option -rep_code)

        Returns :
            (void) : Au retour, tous les cips sont inclus dans la liste self.cips
        """
        cip_file = self.rep_code + "/etudiants.txt"
        cip_list = open(cip_file, "r")
        lines = cip_list.readlines()
        for line in lines:
            if "#" in line:
                continue
            if "%" in line:
                continue
            for student_cip in line.split():
                self.cips.append(student_cip)

        return

    def import_textan_cip(self, import_cip: str) -> None:
        """Importe le fichier textan_CIP1_CIP2.py, où "CIP1_CIP2" est passé dans le paramètre import_cip

        Args :
            import_cip (str) : Contient "CIP1_CIP2", les cips pour le code à tester

        Returns :
            (void) : Au retour, le module textan_CIP1_CIP2 est importé et remplace le précédent
        """

        if "init_module" in self.init_modules:
            # Deuxième appel (ou subséquents) : enlever tous les modules supplémentaires
            for m in sys.modules.keys():
                if m not in self.init_modules:
                    del sys.modules[m]
        else:
            # Premier appel : identifier tous les modules déjà présents
            self.init_modules = sys.modules.keys()

        self.cip = import_cip
        textan_name = "textan_" + import_cip
        self.textan_module = importlib.import_module(textan_name)
        return

    def check_and_setup_golden(self) -> None:
        """Vérifie si une version "golden" doit être conservée

        Args :
            (void) : Le nom de la version "golden" est disponible dans le champ self.args

        Returns :
            (void) : Au retour, le champ golden_module est initialisé (si nécessaire)
        """

        if self.args.golden:
            self.golden_module = importlib.import_module(self.args.golden)
        else:
            self.golden_module: Any = None
        return

    def check_something_to_do(self) -> None:
        """Vérifie que les paramètres d'entrée indiquent quelque chose à faire

        Args :
            (void) : Toute l'information nécessaire est présente dans l'objet

        Returns :
            (void) : Au retour, le champ something_to_do indique le statut.  S'il n'y a rien à faire, sortie
        """

        something_to_do = (
                self.gen_text_all | self.gen_text | self.find_author | self.do_get_kth_ngram
        )

        if not something_to_do:
            print("Aucune action à effectuer. Utiliser un paramètre pour:")
            print("\t - Générer un texte aléatoire (-a Auteur -g) ou (-G)")
            print("\t - Trouver l'auteur d'un texte inconnu (-f texte_inconnu.txt)")
            print("\t - Trouver le k-ième n-gramme le plus fréquent d'un auteur (-F k)")
            print("")
            self.parser.print_help()
            exit()
        return

    def load_cip_code(self, student_cip: str) -> None:
        """Charge le code étudiant en mémoire, initialise l'instance, initialise le débogage

        Args :
            student_cip (str) : Cips de l'ensemble des membres de l'équipe d'APP
        Returns :
            (void) : Rien n'est retourné : au retour, le code étudiant a été chargé en mémoire
        """
        self.import_textan_cip(
            student_cip
        )  # Chargement du code des étudiants identifiés par cip
        self.textan = self.textan_module.TextAn()
        self.setup_instance_param()
        #self.debug_handler.start_execution_timing()  # Permet de mesurer le temps d'exécution du code étudiant
        self.debug_handler.set_student_cip(
            student_cip
        )  # Indique le cip courant au gestionnaire de débogage
        return

    def analyze(self) -> None:
        """Effectue l'analyse des textes fournis (calcul des fréquences pour chacun des auteurs) avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, les textes des auteurs ont été analysés
        """
        self.textan.analyze()
        return

    def generate(self) -> None:
        """Effectue la génération d'un texte aléatoire suivant les statistiques d'un certain auteur (code étudiant)

        Returns :
            (void) : Rien n'est retourné : au retour, un texte aléatoire a été généré, basé sur les statistiques
                        d'un seul auteur, ou de l'ensemble des auteurs
        """

        filename = self.get_gen_file_name()
        filepath = os.path.join(self.dir_res_path, filename)
        to_file = open(filepath, 'w')
        print("")
        print("\tcip: ", self.cip, "- Création d\'un texte aléatoire:")

        if self.gen_text:
            print(f'\t\t--> {self.gen_size} mots, style:  {self.auteur}, nom du fichier: {filename}')
            self.textan.gen_text_auteur(self.auteur, self.gen_size, to_file)
        elif self.gen_text_all:
            print(f'\t\t--> {self.gen_size} mots, style : ensemble des auteurs, nom du fichier: {filename}')
            self.textan.gen_text_all(self.gen_size, to_file)
        to_file.close()

        if self.beautify:
            self.text_beautifier.prettify_file(filepath)
        return

    def find(self) -> None:
        """Calcule la proximité d'un certain texte inconnu avec le "style" de chacun des auteurs avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, le texte inconnu a été comparé aux textes des auteurs
        """
        if self.find_author:

            print("")
            print(f'\tcip: {self.cip} - Calcul des fréquences pour l\'oeuvre "{os.path.basename(self.oeuvre)}": ')

            self.analysis_result = self.textan.find_author(self.oeuvre)
            self.analysis_result.sort(key=self.sort_author_distance, reverse=True)

            print("\t\t--> ", end="")
            # https://stackoverflow.com/questions/493386/how-to-print-without-a-newline-or-space
            for item in self.analysis_result:
                print(f"{item[0]}:{item[1]:.4f} ", end="")
            print("")
        return

    def get_kth_ngram(self) -> None:
        """Obtient le k-ième plus fréquent n-gramme d'un certain auteur avec le code étudiant

        Returns :
            (void) : Rien n'est retourné : au retour, le k-ième n-gramme le plus fréquent a été imprimé
        """
        if self.do_get_kth_ngram:
            if self.auteur == "":
                print(
                    "\tPas d'auteur indiqué: impossible de donner le k-ième n-gramme.  Utiliser -a nom_de_l_auteur"
                )
                return

            print(f"\n\tcip: {self.cip} - Calcul du {self.kth_ngram}e n-gramme le plus fréquent", end="")
            print(f"de l'auteur: {self.auteur}:")

            kth_ngram = self.textan.get_kth_element(self.auteur, self.kth_ngram)
            if not kth_ngram:
                print(f"\tPas de {self.kth_ngram}e n-gramme")
                return

            total_frequency = self.textan.get_total_occurrences(self.auteur)
            frequency = 100 * self.textan.get_ngram_occurrence(self.auteur, kth_ngram[0]) / total_frequency
            mantissa, exponent_base10 = self.textan.convert_to_sci_base_10(frequency)
            print("\t\t--> "
                  f'{self.kth_ngram}e{"r"[:self.kth_ngram == 1]}'
                  f' n-gramme de {self.ngram_size} mot{"s"[:self.ngram_size > 1]}: {kth_ngram}'
                  f' (Fréquence: {mantissa:3.2f} X 10^{exponent_base10}%)')
        return

    def compare_auteurs(self) -> []:
        """Calcule la proximité entre chacun des auteurs (nombre entre 0 et 1) :
            - Effectue le produit scalaire normalisé entre les vecteurs des auteurs

        Returns :
            [] : Retourne un tableau prêt pour l'impression, avec les noms d'auteurs et les valeurs de comparaison
        """
        res_table = []
        auteur_list = []
        closest = [0.0, ("", "")]
        farthest = [1.0, ("", "")]
        res_table.append(auteur_list)  # La première ligne du tableau de résultats contiendra la liste des auteurs
        auteur_list.append("")
        res_buffer = {}   # Tampon pour conserver les valeurs de proximité d'auteurs déjà calculées
        for auteur1 in self.auteurs:
            auteur_res = []
            res_table.append(auteur_res)
            auteur_list.append(auteur1)
            auteur_res.append(auteur1)
            for auteur2 in self.auteurs:
                auteurs_key = tuple(sorted((auteur1, auteur2)))  # Conserver la valeur pour éviter de refaire le calcul
                if auteurs_key in res_buffer:
                    distance = res_buffer[auteurs_key]
                else:
                    distance = self.textan.dot_product_aut(auteur1, auteur2)
                    res_buffer[auteurs_key] = distance
                    if distance < farthest[0]:
                        farthest[0] = distance
                        farthest[1] = auteurs_key
                    if (distance > closest[0]) and auteur1 != auteur2:
                        closest[0] = distance
                        closest[1] = auteurs_key
                auteur_res.append(distance)
        return res_table, closest, farthest

    def print_auteur_distance(self) -> None:
        """Calcule et imprime la proximité entre chacun des auteurs (nombre entre 0 et 1)

        Returns :
            void : Rien n'est retourné : au retour, la distance entre les différents auteurs a été imprimée
        """
        if not self.do_print_auteur_distance:  # Par défaut ce calcul n'est pas fait.  Utiliser -compare_auteurs
            return

        print("\n\tcip:", self.cip, "- Comparaison des auteurs:")

        res_table, closest, farthest = self.compare_auteurs()

        # https://learnpython.com/blog/print-table-in-python/
        res_string = tabulate(res_table, headers="firstrow", tablefmt="fancy_grid")
        res_string = "\t" + res_string
        new_string = '\n\t'.join(res_string.splitlines())  # Add tab at beginning of table (shift table right)
        print(new_string)
        print(f"\tAuteurs les plus proches ({closest[0]:4.3f}): {closest[1][0]}, {closest[1][1]}")
        print(f"\tAuteurs les plus lointains ({farthest[0]:4.3f}): {farthest[1][0]}, {farthest[1][1]}")
        return

    def register_operations(self):
        """Enregistre l'ensemble des méthodes à exécuter pour vérifier le code.
            Les différentes méthodes doivent être enregistrées dans l'ordre où leur exécution doit s'effectuer

        Args :
            void : L'enregistrement se fait avec les méthodes définies dans l'objet

        Returns :
            void : Rien n'est retourné : au retour, toutes les méthodes ont été enregistrées
        """
        exec_pre_print_banner = ">>>------------>>> " + ExecOperation.REPLACE_CIP + " <<<----------------<<<\n"
        exec_pre_print_banner += "\tTentative de chargement du code textan_" + ExecOperation.REPLACE_CIP + ".py"
        self.command.register_one_operation(True,
                                            exec_pre_print_banner,
                                            self.load_cip_code,
                                            True,
                                            "\tChargement réussi")

        # Analyse des textes des auteurs (code étudiant)
        self.command.register_one_operation(True,
                                            "\n\tAppel de la méthode Textan.analyze()",
                                            self.analyze,
                                            False,
                                            "\tAnalyse terminée")

        # Produit un texte aléatoire avec les statistiques de l'auteur choisi
        self.command.register_one_operation(self.gen_text,
                                            "",
                                            self.generate,
                                            False,
                                            "\tGénération de texte terminée")

        # Calcul de proximité entre un texte inconnu et l'ensemble des auteurs (code étudiant),
        self.command.register_one_operation(self.find_author,
                                            "",
                                            self.find,
                                            False,
                                            "\tFin du calcul de proximité")

        # Trouve le k-ième n-gramme le plus fréquent d'un certain auteur (code étudiant)
        self.command.register_one_operation(self.do_get_kth_ngram,
                                            "",
                                            self.get_kth_ngram,
                                            False,
                                            "\tFin du calcul du k-ième ngramme le plus fréquent")

        # Calcule la distance entre les auteurs
        self.command.register_one_operation(self.do_print_auteur_distance,
                                            "",
                                            self.print_auteur_distance,
                                            False,
                                            "\tFin du calcul de proximité entre les auteurs")
        return

    def __init__(self) -> None:
        """Constructeur pour la classe TestTextAn.  Initialisation de l'ensemble des éléments requis :

            - Au besoin, création d'une instance "golden" de TextAn, pour la vérification et la correction
            - Lecture des cips des équipes d'étudiants
            - Mise en mémoire du répertoire de démarrage
            - Validation que la ligne de commande indique au moins une action à effectuer

            - Création d'une instance de CommandTextan, pour enregistrer puis exécuter une série de méthodes
                - Utilise le patron de conception (design pattern) "command"
            - Enregistre la séquence d'opérations à exécuter avec le code TextAn :
                - Charger le code fourni par l'équipe
                - Invoquer la méthode d'analyse de texte de l'équipe
                - Invoquer la méthode de génération de texte aléatoire
                - Calculer la proximité d'un texte aléatoire avec les textes des auteurs fournis
                - Trouver le n-ième ngramme le plus fréquent pour un certain auteur
                - Trouver la distance entre les oeuvres des différents auteurs

            - Création d'une instance de TextBeautifier, qui permet d'améliorer le format des textes générés

        Args :
            (void) : Le constructeur lit la ligne de commande et ajuste l'état de l'objet TestTextAn en conséquence

        Returns :
            (void) : Au retour, la nouvelle instance de test est prête à être utilisée
        """

        super().__init__()

        self.check_and_setup_golden()
        self.get_cips()
        self.add_cwd_to_sys_path()
        self.check_something_to_do()

        self.command = CommandTextan()
        self.register_operations()

        self.text_beautifier = TextBeautifier()

        return


def main() -> None:
    """Démarrage de l'exécution du code de la problématique, pour l'ensemble des équipes :
        - Initialiser une instance de test
        - Pour chaque équipe (séquence de cips) :
            - Faire une copie fraiche de l'instance de test
            - Exécuter la série de commandes préparées à l'aide du patron de conception "command" :
                - Préparation effectuée dans le constructeur TestTextAn
        - Si l'ensemble du code est trop long à s'exécuter (par défaut, 2 minutes), interrompre l'exécution
        - Attraper toutes les exceptions non-traitées dans le code étudiant

    Args :
        (void) : Tout ce qui est nécessaire est défini à l'intérieur de la méthode

    Returns :
        (void) : Au retour, l'exécution est terminée
    """
    golden_tta = TestTextAn()  # Initialisation de l'instance de test

    for cip in golden_tta.cips:  # Permet de tester le code d'une ou plusieurs équipes, à tour de rôle
        tta = copy.deepcopy(
            golden_tta
        )  # Copie fraiche de l'objet, pour isoler les instances des étudiants

        try:
            tta.command.exec_operations(cip)

        # Si le code étudiant est trop lent (120 secondes par défaut), interrompre
        except debug_handler_common.DebugHandlerTimeOutException:
            tta.debug_handler.print_timeout_exception()

        # Mauvaise pratique (attraper toutes les exceptions), mais nécessaire ici, pour du code étudiant inconnu
        except Exception:
            tta.debug_handler.print_general_exception()

        total_run_time = tta.debug_handler.stop_execution_timing()  # Mesure le temps d'exécution du code étudiant
        print(f"\tcip: {cip} - Temps d'exécution total: {total_run_time:.2f} secondes\n")

    if golden_tta.args.fichier_res:  # stdout a été redirigé vers un fichier ; le fermer pour ne rien perdre
        sys.stdout.close()
    return


if __name__ == "__main__":
    main()
