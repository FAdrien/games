#!/usr/bin/python3
# -*- coding: utf-8 -*-


# -------------------------------- Importation --------------------------------
import sys

from time import time

from random import randint

from cmath import sin, cos, exp, pi

import matplotlib.pyplot as plot
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon, Arc, Wedge

# -----------------------------------------------------------------------------


# -------------------------------- Variables --------------------------------
# Le menu qui s'affiche à chaque exécution du programme.
menu = r'''Pavages apériodiques (F_Adrien)
-------------------------------------------------
Choisissez une option (tapez le numéro/la lettre) :
     1 - pavage de Truchet aléatoire (motif jaune/rouge).
     2 - pavage de Truchet aléatoire (motif bleu/vert).
     3 - pavage de Truchet aléatoire (motif jaune/marron).
     4 - pavage de Penrose (méthode Kite-Dart).
     5 - pavage de Penrose (méthode Rhomb).

     q - sortir du programme.
-------------------------------------------------
'''

# Un dictionnaire permettant de lier les différentes options du menu avec une fonction qui sera appelée lorsque l'utilisateur choisira une option valide.
choix_menu = {'1' : lambda: pavageTruchetAleatoire('1'),											# Pavage de Truchet aléatoire (example 1).
			  '2' : lambda: pavageTruchetAleatoire('2'),											# Pavage de Truchet aléatoire (example 2).
			  '3' : lambda: pavageTruchetAleatoire('3'),											# Pavage de Truchet aléatoire (example 3)
			  '4' : lambda: pavagePenrose('1'),														# Pavage de Penrose méthode Kite-Dart (example 1).
			  '5' : lambda: pavagePenrose('2'),
			  'q' : sys.exit																		# Pour quitter le programme.
			 }

axes = None

# ---------------------------------------------------------------------------


# -------------------------------- Fonctions --------------------------------
def preparerFigure(titre, taille = (8, 4), marges = (0, 0, 1, 1)):
	global axes

	figure = plot.figure(titre, figsize = taille)													# On fixe la taille de la figure.
	plot.subplots_adjust(*marges)																	# On fixe les nouvelles marges de la figure.

	axes = figure.add_subplot(111, aspect = "equal")												# On définit une sous-figure et on se place dans un repère orthonormé.
	axes.set_axis_off()																				# On cache les axes du repère (qui, par défaut, sont dessinés).


def pavageTruchetAleatoire(typePavage, colonnes = 20, lignes = 10):
	'''
		Cette fonction se charge de dessiner les trois types de pavage de Truchet 
		aléatoire.

		---------------- Paramètre(s) ----------------
			'typePavage' : un entier (1, 2 ou 3) qui représente le type de pavage de Truchet à réaliser (voir l'énoncé).
			'colonnes' (optionnel, défaut : 8) : un entier positif qui représente le nombre de colonnes à paver.
			'lignes' (optionnel, défaut : 4) : un entier positif qui représente le nombre de lignes à paver.
		----------------------------------------------
	'''

	preparerFigure("Pavage de Truchet aléatoire exemple " + typePavage)								# Préparation de la fenêtre matplotlib (affichage du titre et affectation de la zone de dessin).
	axes.set_xlim([0, colonnes])																	# On adapte la longueur de la fenêtre à la zone pavée.
	axes.set_ylim([0, lignes])																		# On adapte la largeur de la fenêtre à la zone pavée.

	tuile_precedente = 0																			# Cette variable sert à stocker le numéro de la tuile précédente.

	def dessinerTuile(typePavage, numero, colonne, ligne):
		'''
			Cette fonction permet de dessiner une tuile selon le type de pavage 
			de Truchet considéré.
	
			---------------- Paramètre(s) ----------------
				'typePavage' : un entier (1, 2 ou 3) qui représente le type de pavage de Truchet à réaliser (voir l'énoncé).
				'numero' : un entier (0, 1, 2 ou 3) qui représente le numéro de la tuile à dessiner.
				'colonne' : un entier positif qui représente la colonne où dessiner la tuile.
				'ligne' : un entier positif qui représente la ligne où dessiner la tuile.
			----------------------------------------------
		'''
	
		d = numero // 2																				# On va utiliser avantageusement la symétrie des tuiles afin de réduire le nombre d'instructions de dessin.
	
		if typePavage == '1':																		# Si on a affaire au premier exemple de pavage de Truchet aléatoire.
			couleur = ('yellow', 'red')	if 0 < numero < 3 else ('red', 'yellow')					# On fixe les couleurs à utiliser selon le numéro de la tuile.
	
			axes.add_patch(Polygon([(colonne + d, ligne + 1/2), (colonne + d, ligne + 1), (colonne + 1/2, ligne + 1)], facecolor = couleur[0]))
			axes.add_patch(Polygon([(colonne + 1/2, ligne), (colonne + 1 - d, ligne), (colonne + 1 - d, ligne + 1/2)], facecolor = couleur[0]))
			axes.add_patch(Polygon([(colonne + d, ligne), (colonne + 1/2, ligne), (colonne + 1 - d, ligne + 1/2), (colonne + 1 - d, ligne + 1), (colonne + 1/2, ligne + 1), (colonne + d, ligne + 1/2)], facecolor = couleur[1]))
			axes.add_line(Line2D([colonne + d, colonne + 1/2], [ligne + 1/2, ligne + 1], color = 'k'))
			axes.add_line(Line2D([colonne + 1/2, colonne + 1 - d], [ligne, ligne + 1/2], color = 'k'))
	
		elif typePavage == '2':																		# Si on a affaire au second exemple de pavage de Truchet aléatoire.
			couleur = ('lime', 'cyan') if 0 < numero < 3 else ('cyan', 'lime')						# On fixe les couleurs à utiliser selon le numéro de la tuile.
	
			axes.add_patch(Polygon([(colonne + 1 - d, ligne), (colonne + 1 - d, ligne + 1/2), (colonne + 1/2, ligne + 1), (colonne + d, ligne + 1), (colonne + d, ligne + 1/2), (colonne + 1/2, ligne)], facecolor = couleur[0]))
			axes.add_patch(Wedge((colonne + d, ligne), 1/2, theta1 = 90 * d, theta2 = 90 * (1 + d), facecolor = couleur[1]))
			axes.add_patch(Wedge((colonne + 1 - d, ligne + 1), 1/2, theta1 = 90 * (2 + d), theta2 = 270 * (1 - d), facecolor = couleur[1]))
			axes.add_patch(Arc((colonne + d, ligne), 1, 1, theta1 = 90 * d, theta2 = 90 * (1 + d), color = 'w'))
			axes.add_patch(Arc((colonne + 1 - d, ligne + 1), 1, 1, theta1 = 90 * (2 + d), theta2 = 270 * (1 - d), color = 'w'))
	
		elif typePavage == '3':																		# Si on a affaire au troisième exemple de pavage de Truchet aléatoire.
			couleur = ('gold', 'darkred') if 0 < numero < 3 else ('darkred', 'gold')				# On fixe les couleurs à utiliser selon le numéro de la tuile.
	
			axes.add_patch(Polygon([(colonne + 1 - d, ligne), (colonne + 1 - d, ligne + 1/4), (colonne + d / 2 + 1/4, ligne + 1), (colonne + d, ligne + 1), (colonne + d, ligne + 3/4), (colonne + 3/4 - d / 2, ligne)], facecolor = couleur[0]))
			axes.add_patch(Polygon([(colonne + 3/4 - d / 2, ligne), (colonne + d, ligne + 3/4)], edgecolor = 'k'))
			axes.add_patch(Polygon([(colonne + 1 - d, ligne + 1/4), (colonne + d / 2 + 1/4, ligne + 1)], edgecolor = 'k'))
			axes.add_patch(Polygon([(colonne + d, ligne), (colonne + d / 2 + 1/4, ligne), (colonne + 1 - d, ligne + 3/4), (colonne + 1 - d, ligne + 1), (colonne + 3/4 - d / 2, ligne + 1), (colonne + d, ligne + 1/4)], facecolor = couleur[1]))
			axes.add_patch(Polygon([(colonne + d / 2 + 1/4, ligne), (colonne + 1 - d, ligne + 3/4)], edgecolor = 'k'))
			axes.add_patch(Polygon([(colonne + d, ligne + 1/4), (colonne + 3/4 - d / 2, ligne + 1)], edgecolor = 'k'))


	for ligne in range(lignes):																		# On parcours les lignes de la grille à paver.
		Colonnes = range(colonnes) if ligne % 2 == 0 else range(colonnes - 1, -1, -1)				# On parcours la grille de manière continue (en 'serpent') pour ne pas repartir au début de chaque colonne (afin éviter de stocker un second numéro de tuile).
		for colonne in Colonnes:																	# On parcours les colonnes
			dessinerTuile(typePavage, tuile_precedente, colonne, ligne)								# On dessine alors la tuile choisie comme voisine.
			tuile_precedente = (tuile_precedente + 2*randint(0, 1) - 1) % 4							# Cette instruction permet de choisir aléatoirement une tuile voisine de la tuile précédente (elle met aussi à jour le numéro de la tuile précédente).


def pavagePenrose(typePavage, longueur = 20, largeur = 10):
	'''
		Cette fonction se charge de dessiner les deux types de pavage de Penrose.

		---------------- Paramètre(s) ----------------
			'typePavage' : un entier (1, 2 ou 3) qui représente le type de pavage de Truchet à réaliser (voir l'énoncé).
			'longueur' (optionnel, défaut : 8) : un entier positif qui représente la longueur de la zone à paver.
			'largeur' (optionnel, défaut : 4) : un entier positif qui représente la largeur de la zone à paver.
		----------------------------------------------
	'''

	preparerFigure("Pavage de Penrose aléatoire exemple " + typePavage)								# Préparation de la fenêtre matplotlib (affichage du titre et affectation de la zone de dessin).
	axes.set_xlim([0, longueur])																	# On adapte la longueur de la fenêtre à la zone pavée.
	axes.set_ylim([0, largeur])																		# On adapte la largeur de la fenêtre à la zone pavée.

	def rotation(centre, point, angle):
		'''
			Cette fonction se charge de renvoyer l'affixe de l'image du point 'point' par 
			la rotation de centre d'affixe 'centre' et d'angle 'angle' en radian.

			---------------- Paramètre(s) ----------------
				'centre' : l'affixe du centre de la rotation.
				'point' : l'affixe du point dont on cherche l'image par la rotation considérée.
				'angle' : l'angle de la rotation en radian (dans le sens trigonométrique).
			----------------------------------------------
		'''

		return (point - centre) * exp(1j * angle) + centre


	def homothetie(centre, point, rapport):
		'''
			Cette fonction se charge de renvoyer l'affixe de l'image du point 'point' par 
			l'homothétie de centre d'affixe 'centre' et de rapport 'rapport'.

			---------------- Paramètre(s) ----------------
				'centre' : l'affixe du centre de la rotation.
				'point' : l'affixe du point dont on cherche l'image par la rotation considérée.
				'rapport' : le rapport de l'homothétie.
			----------------------------------------------
		'''

		return (point - centre) * rapport + centre


	def cartesienne(point):
		'''
			Cette fonction se charge de renvoyer les coordonnées cartésiennes du point d'affixe 
			'point'.

			---------------- Paramètre(s) ----------------
				'point' : l'affixe du point dont on cherche les coordonnées cartésiennes.
			----------------------------------------------
		'''

		return (point.real, point.imag)


	def substitutionKite(A, C):
		'''
			Cette fonction se charge de renvoyer une liste contenant certaines affixes des sommets 
			et des numéros concernant la nature des polygones à substituer.

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Kite (cerf-volant).
				'C' : l'affixe d'un des quatre points du Kite (cerf-volant).
			----------------------------------------------
		'''

		B, D = rotation(A, C, -pi / 5), rotation(A, C, pi / 5)										# Calcul des affixes des deux points manquants du Kite (cerf-volant).
		C1 = rotation(B, C, pi / 5)																	# Calcul de l'affixe du symétrique de C par rapport à la droite (BD).
		C2 = rotation(A, C1, 2 * -pi / 5)															# Calcul de l'affixe du symétrique de C1 par rapport à la droite (AB).
		return [(0, B, C1), (0, D, C1), (1, A, C1), (1, A, C2)]


	def substitutionDart(A, B):
		'''
			Cette fonction se charge de renvoyer une liste contenant certaines affixes des sommets 
			et des numéros concernant la nature des polygones à substituer.

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Dart (flèche).
				'B' : l'affixe d'un des quatre points du Dart (flèche).
			----------------------------------------------
		'''

		C1, D = rotation(A, B, pi / 5), rotation(A, B, 2 * pi / 5)									# Calcul des affixes d'un des deux points manquants du Dart (flèche) et du point "C" du Kite (cerf-volant).
		C = rotation(B, C1, pi / 5)																	# Calcul de l'affixe du symétrique de C1 par rapport à la droite (BD), c'est le point "C" du Dart (flèche).
		C2 = rotation(D, C, 2 * -pi / 5)															# Calcul de l'affixe du symétrique de C par rapport à la droite (AD)
		return [(0, A, C), (1, B, C), (1, D, C2)]


	def dessinerKite(A, C):
		'''
			Cette fonction se charge de dessiner un Kite (cerf-volant).

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Kite (cerf-volant).
				'C' : l'affixe d'un des quatre points du Kite (cerf-volant).
			----------------------------------------------
		'''

		B, D = rotation(A, C, -pi / 5), rotation(A, C, pi / 5)										# Calcul des affixes des deux points manquants du Kite (cerf-volant).
		axes.add_patch(Polygon([cartesienne(A), cartesienne(B), cartesienne(C), cartesienne(D)], lw = 1, edgecolor = 'black', facecolor = 'purple'))


	def dessinerDart(A, B):
		'''
			Cette fonction se charge de dessiner un Dart (flèche).

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Dart (flèche).
				'B' : l'affixe d'un des quatre points du Dart (flèche).
			----------------------------------------------
		'''

		C1, D = rotation(A, B, pi / 5), rotation(A, B, 2 * pi / 5)									# Calcul des affixes des deux points manquants du Dart (flèche).
		C = rotation(B, C1, pi / 5)																	# Calcul de l'affixe du symétrique de C1 par rapport à la droite (BD), c'est le point "C" du Dart (flèche).
		axes.add_patch(Polygon([cartesienne(A), cartesienne(B), cartesienne(C), cartesienne(D)], lw = 1, edgecolor = 'black', facecolor = 'blue'))


	def substitutionRhombe1(A, C):
		'''
			Cette fonction se charge de renvoyer une liste contenant certaines affixes des sommets 
			et des numéros concernant la nature des polygones à substituer.

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Rhomb 1 (quadrilatère 1).
				'C' : l'affixe d'un des quatre points du Rhomb 1 (quadrilatère 2).
			----------------------------------------------
		'''

		B = (C - A * exp(2 * 1j * -pi / 5)) / (1 - exp(2 * 1j * -pi / 5))
		X = rotation(B, C, pi / 5)
		A1 = rotation(X, A, pi / 5)																	# Calcul de l'affixe du symétrique de C par rapport à la droite (BD).
		C1 = rotation(X, C, -pi / 5)																# Calcul de l'affixe du symétrique de C1 par rapport à la droite (AB).
		return [(0, rotation(C, X, 2 * -pi / 5), X), (0, X, rotation(A, X, 2 * pi / 5)), (0, C1, A1), (1, A, A1), (1, C, C1)]


	def substitutionRhombe2(A, C):
		'''
			Cette fonction se charge de renvoyer une liste contenant certaines affixes des sommets 
			et des numéros concernant la nature des polygones à substituer.

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Rhomb 2 (quadrilatère 2).
				'C' : l'affixe d'un des quatre points du Rhomb 2 (quadrilatère 2).
			----------------------------------------------
		'''

		C1, C2 = rotation(A, C, -pi / 5), rotation(A, C, pi / 5)
		return [(0, C1, rotation(A, C, 3 * -pi / 5)), (0, rotation(A, C, 3 * pi / 5), C2), (1, C, C1), (1, C, C2)]


	def dessinerRhombe1(A, C):
		'''
			Cette fonction se charge de dessiner le Rhombe 1 (quadrilatère 1).

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Rhomb 1 (quadrilatère 1).
				'C' : l'affixe d'un des quatre points du Rhomb 1 (quadrilatère 2).
			----------------------------------------------
		'''

		B, D = (C - A * exp(2 * 1j * -pi / 5)) / (1 - exp(2 * 1j * -pi / 5)), (C - A * exp(2 * 1j * pi / 5)) / (1 - exp(2 * 1j * pi / 5))
		axes.add_patch(Polygon([cartesienne(A), cartesienne(B), cartesienne(C), cartesienne(D)], lw = 1, edgecolor = 'black', facecolor = 'pink'))


	def dessinerRhombe2(A, C):
		'''
			Cette fonction se charge de dessiner le Rhombe 2 (quadrilatère 2).

			---------------- Paramètre(s) ----------------
				'A' : l'affixe d'un des quatre points du Rhomb 2 (quadrilatère 2).
				'C' : l'affixe d'un des quatre points du Rhomb 2 (quadrilatère 2).
			----------------------------------------------
		'''

		B, D = (C - A * exp(1j * -pi / 5)) / (1 - exp(1j * -pi / 5)), (C - A * exp(1j * pi / 5)) / (1 - exp(1j * pi / 5))
		axes.add_patch(Polygon([cartesienne(A), cartesienne(B), cartesienne(C), cartesienne(D)], lw = 1, edgecolor = 'black', facecolor = 'red'))


	zoneEstPavee = 0
	centre = (longueur + 1j * largeur) / 2														# L'affixe du centre de la zone à paver.
	rapport = 1																					# Le rapport d'agrandissement à opérer à la fin du pavage (car les tuiles sont de plus en plus petites à mesure des substitutions).
	liste = [(0, centre - 1j / 2, centre + 1j / 2)]												# La liste initiale ne contient qu'une seule tuile : un Kite (cerf-volant) centré à l'origine.
	while zoneEstPavee < 7:
		rapport /= 2 * sin(pi / 10) if typePavage == '1' else 1 / (2 * cos(pi / 5))				# À chaque nouvelle série de substitutions, on modifie le rapport d'agrandissement.
		for tuile in liste:																		# Pour chaque tuile dans la liste.
			if tuile[0] == 0:																	# Si la tuile est un Kite (cerf-volant).
				if typePavage == '1':
					liste = liste[:liste.index(tuile)] + substitutionKite(*tuile[1:]) + liste[liste.index(tuile) + 1:]	# Alors on remplace cette tuile par 4 autres tuiles selon la règle de substitution du Kite (cerf-volant).
				else:
					liste = liste[:liste.index(tuile)] + substitutionRhombe1(*tuile[1:]) + liste[liste.index(tuile) + 1:]# Alors on remplace cette tuile par 4 autres tuiles selon la règle de substitution du Kite (cerf-volant).
			else:																				# Sinon (si la tuile est un Dart (flèche)).
				if typePavage == '1':
					liste = liste[:liste.index(tuile)] + substitutionDart(*tuile[1:]) + liste[liste.index(tuile) + 1:]		# Alors on remplace cette tuile par 3 autres tuiles selon la règle de substitution du Dart (flèche).
				else:
					liste = liste[:liste.index(tuile)] + substitutionRhombe2(*tuile[1:]) + liste[liste.index(tuile) + 1:]	# Alors on remplace cette tuile par 3 autres tuiles selon la règle de substitution du Dart (flèche).
		zoneEstPavee += 1

	for tuile in liste:
		if tuile[0] == 0:
			if typePavage == '1':
				dessinerKite(homothetie(centre, tuile[1], rapport), homothetie(centre, tuile[2], rapport))
			else:
				dessinerRhombe1(homothetie(centre, tuile[1], rapport), homothetie(centre, tuile[2], rapport))
		else:
			if typePavage == '1':
				dessinerDart(homothetie(centre, tuile[1], rapport), homothetie(centre, tuile[2], rapport))
			else:
				dessinerRhombe2(homothetie(centre, tuile[1], rapport), homothetie(centre, tuile[2], rapport))


# ---------------------------------------------------------------------------


# -------------------------------- Main --------------------------------
if __name__ == '__main__':																			# La boucle principale (là où commence le programme).
	print(menu)																						# On affiche le menu dans la console.

	option = None																					# Cette variable permet de savoir si l'entrée du l'utilisateur est valide ou non. Dans le dernier cas, on redemande une entrée utilisateur.
	while option == None:																			# Tant que l'utilisateur entre une option invalide.
		option = choix_menu.get(input("Option à choisir : "))										# On demande à l'utilisateur de choisir l'une des options proposées et on va chercher dans le dictionnaire si l'option choisie existe ou pas.
		if option != None:																			# Si l'option existe.
			option()																				# Si l'utilisateur a entrée une option valide alors on exécute la fonction associée à l'option choisie.
			plot.show()																				# On affiche la figure dans une fenêtre avec matplotlib.
			option = None



# ----------------------------------------------------------------------

