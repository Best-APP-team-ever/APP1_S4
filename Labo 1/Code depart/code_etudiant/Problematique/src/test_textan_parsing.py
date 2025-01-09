#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Code utilitaire pour lire et interpréter la ligne de commande pour test_textan.py

    Copyright 2018-2025 F. Mailhot et Université de Sherbrooke
"""
import argparse
import sys
import os
import timeit
from handle_unicode_common import HandleUnicodeCommon
import debug_handler_common


class ParsingClassTextAn:
    def parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            void : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        parser = argparse.ArgumentParser(prog="textan_CIP1_CIP2.py")

        parser.add_argument(
            "-d",
            default="TextesPourEtudiants",
            help="Répertoire contenant les sous-repertoires des auteurs \
                            (TextesPourEtudiants par défaut)",
        )
        parser.add_argument(
            "-a", help="Résultats à produire pour cet auteur spécifique"
        )
        parser.add_argument(
            "-f", help="Fichier inconnu pour lequel on recherche un auteur"
        )
        parser.add_argument(
            "-m",
            default=1,
            type=int,
            choices=range(1, 20),
            help="Mode (1 ou 2 ou 3 ou ... 20) - unigrammes ou digrammes ou trigrammes ou ... 20-grammes",
        )
        parser.add_argument(
            "-F",
            type=int,
            help="Indication du rang (en fréquence) du n-gramme a imprimer",
        )
        parser.add_argument(
            "-G",
            default=0,
            action="store_true",
            help="Génération de texte avec les statistiques de tous les auteurs",
        )
        parser.add_argument(
            "-g",
            default=0,
            action="store_true",
            help="Génération de texte avec les statistiques de l'auteur (identifié par -a)"
        )
        parser.add_argument(
            "-g_size", default=500, type=int, help="Taille du texte à générer"
        )
        parser.add_argument(
            "-g_base",
            default="Gen_text",
            help="Nom de base du fichier de texte à générer",
        )
        parser.add_argument(
            "-g_ext",
            default=".txt",
            help="Extension utilisée pour le fichier généré, .txt par défaut",
        )
        parser.add_argument(
            "-g_nocip",
            action="store_true",
            help="Ne pas utiliser les CIPs dans le nom du fichier généré",
        )
        parser.add_argument(
            "-g_noaut",
            action="store_true",
            help="Ne pas utiliser le nom de l'auteur dans le nom du fichier généré",
        )
        parser.add_argument(
            "-g_sep",
            default="_",
            help="Utiliser cette chaine de caractères comme séparateur dans le nom de fichier généré",
        )

        parser.add_argument("-v", action="store_true", help="Mode verbose")
        parser.add_argument(
            "-noPonc", action="store_true", help="Retirer la ponctuation"
        )
        parser.add_argument(
            "-rep_code",
            default=".",
            help="Répertoire contenant la liste des CIPs et leur code textan_CIP1_CIP2.py",
        )
        parser.add_argument(
            "-recursion", help="Récursion maximale permise (par défaut, 1000)"
        )
        parser.add_argument(
            "-golden",
            help="Compare les résultats avec la version 'golden' indiquée par ce paramètre",
        )
        parser.add_argument(
            "-fichier_res", help="Tous les prints seront faits dans ce fichier"
        )
        parser.add_argument(
            "-dir_res",
            help="Tous les résultats seront ajoutés dans ce répertoire (sous le répertoire courant)",
        )
        parser.add_argument(
            "-timeout",
            default=120,
            help="Temps maximum (secondes) pour l'exécution du système"
        )
        parser.add_argument(
            "-compare_auteurs",
            action="store_true",
            help="Indique les proximités des textes des différents auteurs",
        )
        parser.add_argument(
            "-not_pretty",
            action="store_true",
            help="Ne pas utiliser l'appel au système de reformattage des textes générés pour les rendre plus beaux",
        )

        self.parser = parser
        self.args = parser.parse_args()
        return

    def setup_after_parse(self) -> None:
        """Utilise le champ args pour :
            - Définir tous les champs modifiables par la ligne de commande
            - Ouvrir un fichier de résultats (si demandé) et y rediriger stdout

        Returns :
            void : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        if self.args.d:
            self.dir = self.args.d
        if self.args.noPonc:
            self.keep_punc = False
        if self.args.m:
            self.ngram_size = self.args.m
        if (self.args.G or self.args.g) and self.args.g_size > 0:
            self.gen_size = self.args.g_size
            self.gen_basename = self.args.g_base
            if self.args.g_ext:
                self.g_ext = self.args.g_ext
            if self.args.g_nocip:
                self.g_cip = False
            if self.args.g_noaut:
                self.g_aut = False
            if self.args.g_sep:
                self.g_sep = self.args.g_sep
            if self.args.g:
                self.gen_text = True
            if self.args.G:
                self.gen_text_all = True
        if self.args.a:
            self.auteur = HandleUnicodeCommon.normalize_string(self.args.a)
        if self.args.rep_code:
            self.rep_code = self.args.rep_code

        if self.args.f:
            self.oeuvre = self.args.f
            self.find_author = True
        if self.args.F:
            self.do_get_kth_ngram = True
            self.kth_ngram = self.args.F
        if self.args.timeout:
            self.timeout = int(self.args.timeout)
        if self.args.fichier_res:
            # https://stackoverflow.com/questions/5104957/how-do-i-create-a-file-at-a-specific-path
            cur_path = os.path.dirname(__file__)
            if self.args.dir_res:
                dir_res_path = os.path.join(str(cur_path), str(os.path.relpath(self.args.dir_res, cur_path)))
                try:  # https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory
                    os.mkdir(dir_res_path)
                except FileExistsError:
                    pass
            else:
                dir_res_path = cur_path
            output_file_path = os.path.join(dir_res_path, self.args.fichier_res)
            # Voir: https://stackoverflow.com/questions/4675728/redirect-stdout-to-a-file-in-python
            # et: https://stackoverflow.com/questions/3597480/how-to-make-python-3-print-utf8
            sys.stdout = open(output_file_path, "w", encoding="UTF-8", buffering=1)
            self.dir_res_path = dir_res_path
        if self.args.recursion:
            sys.setrecursionlimit(int(self.args.recursion))
        if self.oeuvre:
            real_path_file = os.path.realpath(self.oeuvre)
            try:
                # https://docs.python.org/3/library/os.path.html#os.path.realpath
                # https://www.tutorialspoint.com/python/os_readlink.htm
                if not os.path.isfile(real_path_file):
                    if os.path.isdir(real_path_file):
                        raise IsADirectoryError(real_path_file)
                    else:
                        raise FileNotFoundError()
                else:
                    self.oeuvre = real_path_file

            except FileNotFoundError:
                print("Le fichier", real_path_file, "n'existe pas (paramètre -f)")
                self.debug_handler.print_debug_info()
                sys.exit(1)
            except IsADirectoryError:
                print("Le nom", real_path_file, "correspond à un répertoire et non à un fichier")
                self.debug_handler.print_debug_info()
                sys.exit(1)

        if self.args.compare_auteurs:
            self.do_print_auteur_distance = True
        if self.args.not_pretty:
            self.beautify = False
        return

    def setup_and_parse_cli(self) -> None:
        """Initialise l'objet en interprétant la ligne de commande :
            - Lit la ligne de commande
            - Modifie tous les champs qui y sont définis

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """
        self.parse_cli()
        self.setup_after_parse()
        return

    def __init__(self) -> None:
        """Constructeur pour la classe TestTextAn.  Initialisation de l'ensemble des éléments requis

        Args :
            (void) : Le constructeur lit la ligne de commande et ajuste l'état de l'objet TestTextAn en conséquence

        Returns :
            (void) : Au retour, la nouvelle instance de test est prête à être utilisée
        """
        self.parser = None
        self.args = None
        self.textan_module = None
        self.golden_module = None

        self.dir = "."
        self.ngram_size = 1
        self.keep_punc = True
        self.gen_text = False
        self.gen_text_all = False
        self.gen_size = 0
        self.gen_basename = "Gen_text"
        self.cip = ""
        self.g_ext = ".txt"
        self.g_cip = True
        self.g_aut = True
        self.g_sep = "_"
        self.rep_code = "."
        self.auteur = ""
        self.oeuvre = ""
        self.find_author = False
        self.do_analyze = False
        self.do_get_kth_ngram = False
        self.kth_ngram = 1
        self.analysis_result = {}
        self.auteurs = []
        self.textan = None
        self.golden = None
        self.timeout = -1
        self.do_print_auteur_distance = False
        self.dir_res_path = "."

        self.start_time = timeit.default_timer()
        self.debug_handler = debug_handler_common.DebugHandler()

        self.setup_and_parse_cli()

        self.debug_handler.timeout = self.timeout
        self.cips = []
        self.init_modules = {}

        self.beautify = True

        return
