#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Code pour explorer le troisième exercice du laboratoire - APP du cours GIF270

    L'exercice 3 touche les arbres AVL et l'élément suivant :
        - Redéfinition de la méthode rotate_right

    Note :
        - Le traitement des arguments a été inclus dans la classe ParsingClass3, qui est utilisée dans le code principal
        - Tous les arguments requis sont présents et accessibles dans ParsingClass3.args
        - Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments

    Copyright 2018-2025, Frédéric Mailhot et Université de Sherbrooke
"""
from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator


class TreeNode:
    """Création d'un noeud pour un arbre

    Code tiré des sections 6.13 à 6.17 du livre de référence
    Voir : <https://runestone.academy/ns/books/published/GIF270/Trees/SearchTreeImplementation.html>
    """

    def __init__(self, key: int, val: int, left: TreeNode =None, right: TreeNode =None, parent: TreeNode =None) -> None:
        """Initialisation d'un nouveau noeud d'un arbre

        Args :
            key (int) :

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        self.key = key
        self.payload = val
        self.left_child = left
        self.right_child = right
        self.parent = parent
        self.balance_factor = 0
        return

    def has_left_child(self) -> bool:
        """Indique si un noeud a un enfant à gauche

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (TreeNode) : Valeur de l'enfant à gauche, ou valeur nulle
        """
        return self.left_child

    def has_right_child(self) -> bool:
        """Indique si un noeud a un enfant à droite

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (TreeNode) : Valeur de l'enfant à droite, ou valeur nulle
        """
        return self.right_child

    def is_left_child(self) -> bool:
        """Indique si un noeud est l'enfant à gauche de son parent

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Vrai si le noeud a un parent dont il est l'enfant à gauche, Faux sinon
        """
        return self.parent and self.parent.left_child == self

    def is_right_child(self) -> bool:
        """Indique si un noeud est l'enfant à droite de son parent

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Vrai si le noeud a un parent dont il est l'enfant à droite, Faux sinon
        """
        return self.parent and self.parent.right_child == self

    def is_root(self) -> bool:
        """Indique si un noeud est la racine d'un arbre (dans ce cas, il n'a pas de parent)

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Faux si le noeud a un parent, Vrai sinon
        """
        return not self.parent

    def is_leaf(self) -> bool:
        """Indique si un noeud est une feuille d'un arbre

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Vrai si le noeud n'a pas d'enfant à gauche ni d'enfant à droite, Faux sinon
        """
        return not (self.right_child or self.left_child)

    def has_any_children(self) -> bool:
        """Indique si un noeud possède au moins un enfant

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Vrai si le noeud a un enfant à gauche, un enfant à droite, ou les deux, Faux sinon
        """
        return self.right_child or self.left_child

    def has_both_children(self) -> bool:
        """Indique si un noeud a deux enfants

        Args :
            (void) : On observe l'instance elle-même

        Returns :
            (bool) : Vrai si le noeud deux enfants, Faux sinon
        """
        return self.right_child and self.left_child

    def replaceNodeData(self, key: int, value: int, lc: TreeNode, rc: TreeNode) -> None:
        """Remplace toute l'information contenue dans un noeud

        Args :
            key (int) : Clé associée au noeud
            value (int) : Contenu associé à un noeud (peut être n'importe quel objet)
            lc (TreeNode) : Nouvel enfant à gauche
            rc (TreeNode) : Nouvel enfant à droite

        Returns :
            (void) : Les champs du noeud sont mis à jour, et il devient le parent de ses nouveaux noeuds enfants
        """
        self.key = key
        self.payload = value
        self.left_child = lc
        self.right_child = rc
        if self.has_left_child():
            self.left_child.parent = self
        if self.has_right_child():
            self.right_child.parent = self
        return


class BinarySearchTree:
    """Création d'un arbre binaire

    Code tiré de la section 6.13 du livre de référence
    Voir : <https://runestone.academy/ns/books/published/GIF270/Trees/SearchTreeImplementation.html>

    """

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance d'arbre  :

        Args :
            (void) : Ne fait que créer l'amorce d'un arbre vide

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        self.root: TreeNode = None
        self.size = 0
        return

    def length(self) -> int:
        """Retourne la taille (le nombre de noeuds) de l'arbre :

        Args :
            (void) : La taille de l'arbre est contenue dans l'objet de type BinarySearchTree

        Returns :
            (int) : Retourne le nombre de noeuds dans l'arbre
        """
        return self.size

    def __len__(self) -> int:
        """Retourne la taille (le nombre de noeuds) de l'arbre :

        Args :
            (void) : La taille de l'arbre est contenue dans l'objet de type BinarySearchTree

        Returns :
            (int) : Retourne le nombre de noeuds dans l'arbre
        """
        return self.size

    def __iter__(self) -> Iterator:
        """Retourne un itérateur sur le noeud :

        Args :
            (void) : On utilise le noeud racine de l'objet de type BinarySearchTree

        Returns :
            (Iterator) : Retourne l'itérateur par défaut du noeud racine de l'arbre binaire
        """
        return self.root.__iter__()

    def put(self, key: int, val: int) -> None:
        """Ajout d'une nouvelle valeur dans l'arbre binaire :

        Args :
            key (int) : La clé associée à la valeur à ajouter
            val (int) : La valeur à ajouter dans l'arbre

        Returns :
            (void) : Au retour, un nouveau noeud a été ajouté à l'arbre avec la valeur passée en paramètre
        """
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1
        return

    def _put(self, key: int, val: int, current_node: TreeNode) -> None:
        """Traverse l'arbre existant et ajoute le noeud au bon endroit :

        Args :
            key (int) : La clé associée à la valeur à ajouter
            val (int) : La valeur à ajouter dans l'arbre
            current_node (TreeNode) : le noeud courant, lors de la traversée de l'arbre

        Returns :
            (void) : Au retour, un nouveau noeud a été ajouté à l'arbre, au bon endroit
        """
        if key < current_node.key:
            if current_node.hasLeftChild():
                self._put(key, val, current_node.leftChild)
            else:
                current_node.leftChild = TreeNode(key, val, parent=current_node)
        else:
            if current_node.hasRightChild():
                self._put(key, val, current_node.rightChild)
            else:
                current_node.rightChild = TreeNode(key, val, parent=current_node)
        return

    def __setitem__(self, k: int, v: int) -> None:
        """Wrapper pour utiliser la méthode put d'ajout d'une nouvelle valeur dans l'arbre binaire :

        Args :
            k (int) : La clé associée à la valeur à ajouter
            v (int) : La valeur à ajouter dans l'arbre

        Returns :
            (void) : Au retour, un nouveau noeud a été ajouté à l'arbre avec la valeur passée en paramètre
        """
        self.put(k, v)
        return

    def get(self, key: int) -> TreeNode:
        """Retour du noeud associé à la clée dans l'arbre binaire :

        Args :
            key (int) : La clé associée à la valeur à trouver

        Returns :
            (TreeNode) : Le noeud associé à la clé (si elle existe dans l'arbre)
        """
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key: int, current_node: TreeNode) -> TreeNode:
        """Traverse l'arbre existant et retourne le noeud approprié :

        Args :
            key (int) : La clé associée à la valeur à ajouter
            current_node (TreeNode) : Le noeud courant (au départ, il s'agit de la racine de l'arbre)

        Returns :
            (TreeNode) : Le noeud associé à la clé (peut être l'objet None si la clé est absente de l'arbre)
        """
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.leftChild)
        else:
            return self._get(key, current_node.rightChild)

    def __getitem__(self, key: int) -> TreeNode:
        """Wrapper pour utiliser la méthode get de recherche d'un noeud avec une certaine valeur dans l'arbre binaire :

        Args :
            key (int) : La clé associée au noeud à trouver

        Returns :
            (TreeNode) : Au retour, le noeud avec la valeur recherchée (ou None s'il n'existe pas)
        """
        return self.get(key)

    def __contains__(self, key: int) -> bool:
        """Test logique (vrai ou faux) pour déterminer si une clé est présente dans l'arbre (ou non)

        Args :
            key (int) : La clé associée au noeud à trouver

        Returns :
            (bool) : Indique si la valeur se trouve dans l'orbre ou non
        """
        if self._get(key, self.root):
            return True
        else:
            return False


class AVLTreeCommon(BinarySearchTree) :
    def _put(self, key: int, value: int, current_node: TreeNode) -> None:
        """Redéfinition de la méthode _put de la classe BinarySearchTree pour inclure au besoin le rebalancement :

        Args :
            key (int) : La clé associée à la valeur à ajouter
            value (int) : La valeur à ajouter dans l'arbre
            current_node (TreeNoce) : Le noeud courant (au départ, c'est le noeud racine de l'arbre)

        Returns :
            (void) : Au retour, un nouveau noeud a été ajouté à l'arbre, au bon endroit
        """
        if key < current_node.key:
            if current_node.left_child:
                self._put(key, value, current_node.left_child)
            else:
                current_node.left_child = TreeNode(
                    key, value, 0, parent=current_node
                )
                self.update_balance(current_node.left_child)
        else:
            if current_node.right_child:
                self._put(key, value, current_node.right_child)
            else:
                current_node.right_child = TreeNode(
                    key, value, 0, parent=current_node
                )
                self.update_balance(current_node.right_child)
        return

    def update_balance(self, node: TreeNode) -> None:
        """À partir d'un certain noeud, rebalancer ses enfants immédiats et son parent, si nécessaire :

        Args :
            node (TreeNoce) : Le noeud courant

        Returns :
            (void) : Au retour, le noeud a été rebalancé, ainsi que ses parents (si nécessaire)
        """
        if self.do_rebal:
            if node.balance_factor > 1 or node.balance_factor < -1:
                self.rebalance(node)
                return
        if node.parent:
            if node.is_left_child():
                node.parent.balance_factor += 1
            elif node.is_right_child():
                node.parent.balance_factor -= 1

            if node.parent.balance_factor != 0:
                self.update_balance(node.parent)
        return

    def rebalance(self, node: TreeNode) -> None:
        """Rebalancer un noeud en utilisant des rotations sur ses enfants :

        Args :
            node (TreeNoce) : Le noeud courant

        Returns :
            (void) : Au retour, le noeud a été rebalancé
        """
        if node.balance_factor < 0:
            if node.right_child.balance_factor > 0:
                self.rotate_right(node.right_child)
                self.rotate_left(node)
            else:
                self.rotate_left(node)
        elif node.balance_factor > 0:
            if node.left_child.balance_factor < 0:
                self.rotate_left(node.left_child)
                self.rotate_right(node)
            else:
                self.rotate_right(node)
        return

    def rotate_left(self, rotation_root: TreeNode) -> None:
        """Rotation d'un sous-arbre vers la droite :

        Args :
            rotation_root (TreeNode) : Noeud sur lequel effectuer la rotation gauche

        Returns :
            (void) : Au retour, la rotation gauche a été effectuée et tous les noeuds ont été ajustés
        """
        new_root = rotation_root.right_child
        rotation_root.right_child = new_root.left_child
        if new_root.left_child:
            new_root.left_child.parent = rotation_root
        new_root.parent = rotation_root.parent
        if rotation_root.is_root():
            self.root = new_root
        else:
            if rotation_root.is_left_child():
                rotation_root.parent.left_child = new_root
            else:
                rotation_root.parent.right_child = new_root
        new_root.left_child = rotation_root
        rotation_root.parent = new_root
        rotation_root.balance_factor = (
                rotation_root.balance_factor + 1 - min(new_root.balance_factor, 0)
        )
        new_root.balance_factor = (
                new_root.balance_factor + 1 + max(rotation_root.balance_factor, 0)
        )
        return

    def rotate_right(self, rotation_root: TreeNode) -> None:
        """Rotation d'un sous-arbre vers la droite :

        Args :
            rotation_root (TreeNode) : Noeud sur lequel effectuer la rotation droite

        Returns :
            (void) : Au retour, la rotation droite a été effectuée et tous les noeuds ont été ajustés
        """
        # Code incomplet.  Doit être modifié dans la classe AVLTree, qui hérite de AVLTreeCommon.
        return

    def __init__(self, do_rebal: bool) -> None:
        """Initialisation d'un nouvel arbre AVL :
            - Le paramètre do_rebal permet de créer (et observer) un abre balancé (AVL) ou non

        Args :
            do_rebal (bool) : L'arbre doit être rebalancé dynamiquement (AVL) ou non (arbre binaire standard)

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()
        self.do_rebal = do_rebal
        return


class ParsingClass3:
    """Création d'un parser prédéfini pour lire les paramètres de la ligne de commande pour le troisième exercice

    """

    def setup_and_parse_cli(self) -> None:
        """Utilise le module argparse pour :
            - Enregistrer les commandes à reconnaître
            - Lire la ligne de commande et créer le champ self.args qui récupère la structure produite

        Returns :
            (void) : Au retour, toutes les commandes reconnues sont comprises dans self.args
        """

        parser = argparse.ArgumentParser(prog='Labo1:Exercice3.py')
        parser.add_argument('-f', required=True, help='Fichier contenant les nombres à ordonner')
        parser.add_argument('-v', action='store_true', help='Mode verbose')
        parser.add_argument('-nrb', action='store_true', help='Sans rebalancement')
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

    def read_one_file(self, filename: str, numbers: []) -> None:
        """Lecture d'un fichier de nombres et ajout dans le tableau fourni :

        Args :
            filename (str) : Nom du fichier à traiter
            numbers (array) : Tableau de nombres (vide au départ)

        Returns :
            (void) : Au retour, le tableau de nombre est rempli
        """
        file_lines = self.read_file_lines(filename)
        for one_line in file_lines:
            a = int(one_line)
            numbers.append(a)
        return

    def read_numbers(self) -> None:
        """Lecture du fichier nécessaire à l'exercice :

        Args :
            (void) : Tout se trouve déjà dans l'objet

        Returns :
            (void) : Au retour, la liste de nombre est complète
        """
        self.read_one_file(self.args.f, self.input_numbers)
        return

    def __init__(self) -> None:
        """Initialisation d'une nouvelle instance de ParsingClass3 :
            - Ajoute toutes les valeurs par défaut des paramètres utilisés
            - Modifie les valeurs redéfinies sur la ligne de commande

        Returns :
            (void) : Au retour, l'objet est initialisé, avec la liste de nombres dans le tableau input_numbers
        """
        self.input_numbers = []
        self.parser: argparse.ArgumentParser = None
        self.args: argparse.Namespace = None
        self.setup_and_parse_cli()
        self.read_numbers()

        # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
        if self.args and self.args.v:
            print("Mode verbose:")
            print("\tFichier de nombres: " + self.args.f)
            if self.args and self.args.nrb:
                print("\tArbre non rebalancé")
            else:
                print("\tArbre rebalancé")
        return


class LaboProb3Common(ParsingClass3):
    """Création de méthodes permettant de créer des arbres AVL
        - Classe hérite de ParsingClass3, qui lit les paramètres de la ligne de commande
    """

    def build_AVL(self) -> None:
        """Méthode qui crée l'arbre AVL à partir des nombres inclus dans le tableau self.input_numbers
            - Utilise la classe AVLTree définie dans l'objet
            - Cette classe peut être redéfinie lors de la création de l'objet (paramètre facultatif)
            - Si elle est redéfinie, cela permet d'utiliser une version différente de AVLTree
            - Par exemple, la version par défaut (AVLTreeCommon) ne contient pas le code pour la rotation droite

        Args :
            (void) : Tout se trouve dans l'objet

        Returns :
            (void) : Au retour, l'arbre AVL est créé
        """
        self.avl = self.AVLTreeClass(self.do_rebal)     # Création de l'arbre AVL à l'aide de la classe fournie
        for i in range(len(self.input_numbers)):        # Ajout des nombres de la liste dans l'arbre
            self.avl.put(self.input_numbers[i], i)
        return

    def print_one_node(self, node: TreeNode, depth: int, max_depth: int) -> int:
        """Imprime à l'écran les valeurs de chacun des noeuds de l'arbre AVL, dans l'ordre :
            - D'abord les enfants gauches
            - Ensuite la valeur dans le noeud lui-même
            - Enfin les enfants droits

        Args :
            node (TreeNode) : le noeud à traiter dans l'arbre AVL
            depth (int) :    la profondeur du noeud courant
            max_depth (int) : la plus grande profondeur observée jusqu'à maintenant

        Returns :
            max_depth (int) : la profondeur maximale observée (enfant gauche, noeud lui-même, enfant droit)
        """
        if node:
            if depth > max_depth:
                max_depth = depth
            max_depth_left = self.print_one_node(node.left_child, depth + 1, max_depth)
            if max_depth_left > max_depth:
                max_depth = max_depth_left
            print(depth, ":", node.key)
            max_depth_right = self.print_one_node(node.right_child, depth + 1, max_depth)
            if max_depth_right > max_depth:
                max_depth = max_depth_right
        return max_depth

    def print_AVL(self) -> None:
        """Imprime à l'écran les valeurs ordonnées dans l'arbre AVL.
            À la fin, indique la profondeur maximale de l'arbre

        Args :
            (void) : Tout se trouve dans l'objet

        Returns :
            (void) : Au retour, l'arbre AVL a été imprimé, ainsi que la profondeur maximale
        """
        max_depth = self.print_one_node(self.avl.root, 1, 0)
        if self.do_rebal:
            print("---> \"Vrai\" arbre AVL, avec rebalancement")
        else:
            print("---> \"Faux\" arbre AVL: sans rebalancement")
        print("Profondeur maximale:", max_depth)
        return

    def do_something(self) -> None:
        """Méthode appelée pour créer l'arbre AVL, imprimer la liste initiale de nombres, puis l'arbre AVL (ordonné)

        Args :
            (void) : Tout se trouve dans l'objet

        Returns :
            (void) : Au retour, l'arbre AVL est créé et a été imprimé
        """
        self.build_AVL()

        # Le premier print imprime la liste de nombres originale à l'écran (avec le rang dans la liste)
        # Le deuxième print imprime la liste ordonnée (à l'aide de l'arbre AVL
        print("Nombres en entrée: -----------------------------------------------")
        for i in range(len(self.input_numbers)):
            print(i + 1, ":", self.input_numbers[i])

        print("Arbre AVL: -----------------------------------------------")
        self.print_AVL()
        return

    def __init__(self, avltree_class=AVLTreeCommon) -> None:
        """Initialisation d'une nouvelle instance de LaboProb3 :
            - Utilise l'initialisation de la classe héritée par LaboProb3 (ParsingClass3)
            - Par défaut, utilise la classe AVLTreeCommon pour la création future des arbres AVL
            - Cependant, cette classe peut être redéfinie à la création de l'objet

        Returns :
            (void) : Au retour, l'objet est initialisé
        """
        super().__init__()
        self.AVLTreeClass = avltree_class
        self.avl: AVLTreeCommon = None
        self.do_rebal = True
        if self.args.nrb:
            self.do_rebal = False
        return
