import numpy as np
import random as rd

from copy import deepcopy

'''

C'est le jeu de la bataille navale, chaque adversaire possède deux
plateaux, celui du bas est l'océan du joueur, c'est ici que vont se
positionner ses bateaux et c'est ici qu'il indiquera les tirs de
l'adversaire 'o' lorsque qu'il s'agit de l'océan, 'x' si c'est un bateau.
Idem pour le plateau du haut sauf qu'il s'agit des tirs du joueurs et
de l'océan 'vide' de l'adversaire.

'''

bateau0 = np.array([['a', 'a']])
bateau1 = np.array([['b', 'b', 'b']])
bateau2 = np.array([['c', 'c', 'c']])
bateau3 = np.array([['d', 'd', 'd', 'd']])
bateau4 = np.array([['e', 'e', 'e', 'e', 'e']])

#Une case vide des deux plateaux
vide = '-'
#Tir nul
tir_r = 'o'
#Tir correct
tir_b = 'x'
#Le plateau du haut (là ou le joueur attaque)
plateauAtt = []
#Le plateau du bas (là ou le joueur place ses bateaux)
plateauJ = []
#Le plateau du bas (là ou l'ordinateur place ses bateaux)
plateauO = []
#Les bateaux: bateau 0: le plus petit; bateau 1: le sous-marin; bateau 2: normal; bateau 3: le moyen et bateau 4: le porte-avions.
bateaux = [bateau0, bateau1, bateau2, bateau3, bateau4]
bateaux_lettre = ['a','b','c','d','e']
#Cette liste sert de confirmation pour la position des bateaux du joueur
bateaux2 = []
#Cette liste sert au placement des bateaux de l'ordinateur
bateaux_Ordi = deepcopy(bateaux)
#Le bateau sélectionné par le joueur pour le placer sur le terrain
bateauSelec = bateau0
#Variable qui permet de jouer chacun son tour
pouvoirJouer = 0

# On définit les deux plateaux de jeu de 10*10 cases
def defPlateau():
	global plateauJ, plateauAtt, plateauO
	ligne = [[vide]*10]
	plateauJ = np.array(10*ligne)
	plateauAtt = deepcopy(plateauJ)
	plateauO = deepcopy(plateauJ)
   
# On défini l'événement 'rotation' pour effectuer une rotation des pièces lors de leur placement
def rotation(bat):
	global bateauSelec
	bateauSelec = np.rot90(bat)
	print("Le bateau sélectionné (bateau '" + bat[0][0] + "') a subit une rotation !\n")
	
def ArreterProg(event):
	socket.stop()
	sys.exit()
	
def RetirerBatSilent(bat):
	global plateauJ, bateaux, bateaux2, bateaux_lettre
	if bat[0][0] in plateauJ:
		if bat.shape[0]>1:
			bat=np.rot90(bat)
		bateaux.append(bat)
		removeArray(bateaux2,bat)
		bateaux_lettre.append(bat[0][0])
		bateaux_lettre.sort()
		bateaux = trierBateaux(bateaux)
		bateaux2 = trierBateaux(bateaux2,True)
		plateauJ = np.char.replace(plateauJ,bat[0][0],vide)
		bateauSelec=np.rot90(bat)

def compatible(x, y,plateau): # teste si la pièce est posable à l'emplacement (i,j)
	global bateauSelec, vide
	lg,col = bateauSelec.shape
	poser = (x+lg<=10) and (y+col<=10) # est-ce que la pièce tient sur le plateau ?
	i = 0
	while poser and i<lg:
		j = 0
		while poser and j<col:
			if (bateauSelec[i,j] != vide) and (plateau[x+i,y+j] != vide): 
				poser = False # pièce non posable
				print("Le bateau sélectionné (bateau '" + bateauSelec[0][0] + "') ne peut être placé.\n")
			j += 1
		i += 1
	if poser: # on pose la pièce sur un plateau temporaire
		tableau = plateau.copy()
		lg,col = bateauSelec.shape # Nombre de lignes et nombre de colonnes d'une pièce de jeu
		for i in range(lg):
			for j in range(col):
				if bateauSelec[i,j] != vide:
					tableau[x+i,y+j] = bateauSelec[i,j] #On met la pièce sur le plateau
		plateau = tableau
		print("Le bateau sélectionné (bateau '" + bateauSelec[0][0] + "') a bien été placé.\n")
	return plateau, poser
					
# Permet de poser nos bateau, si un bateau est déjà posé, alors on supprime l'ancien
def poserBateauSel(x,y,plateau):
	global bateauSelec,vide
	if bateauSelec[0][0] in plateau:
		plateau = np.char.replace(plateau,bateauSelec[0][0],vide)
	return compatible(x,y,plateau)
		
# Cette fonction est répétée plusieurs fois d'où sa présence ici, elle sert juste à poser des bateaux selon les indications du joueur
def demanderCoordonnees(confirmation=False):
	global bateaux, bateauSelec, bateaux2, plateauJ
	x=0
	y=0
	rep=''
	rep2=''
	rep3=''
	if confirmation==False:
		while rep not in bateaux_lettre:
			rep=input("Sélectionnez un bateau " + str(bateaux_lettre) + " : ")
			if rep in ['a','b','c','d','e'] and rep not in bateaux_lettre:
				rep2=input("Le bateau " + str(rep) + " à déjà été placé, voulez-vous le retirer ('o' (oui), 'n' (non)) ? ")
				if rep2=='o':
					RetirerBatSilent(bateaux2[[i for i in ['a','b','c','d','e'] if i not in bateaux_lettre].index(rep)])
		bateauSelec = bateaux[bateaux_lettre.index(rep)]
	else:
		rep=bateauSelec[0][0]
	while rep3 not in ['o', 'O', 'n', 'N']:
		rep3=input("Voulez-vous effectuer une rotation (dans le sens inverse des aiguilles d'une montre) à votre bateau ('o' (oui), 'n' (non)) ? ")
	if rep3 in ['o', 'O']:
		rotation(bateauSelec)
	while x not in ['1','2','3','4','5','6','7','8','9','10'] or y not in ['1','2','3','4','5','6','7','8','9','10']:
		x=input("Coordonnée X du bateau (coin à gauche): ")
		y=input("Coordonnée Y du bateau (coin à gauche): ")
		print(" ")
	x=int(x)
	y=int(y)
	plateauJ, b = poserBateauSel(x-1,y-1, plateauJ)
	if b==True:
		if bateauSelec.shape[0]>1:
			bateauSelec=np.rot90(bateauSelec)
		removeArray(bateaux,bateauSelec)
		bateaux2.append(bateauSelec)
		bateaux_lettre.remove(rep)
	printPlateau(plateauJ)

# Cette fonction va demander à l'utilisateur de placer tous ses bateaux puis une confirmation
def placerBateau():
	global bateaux, bateauSelec, bateaux2
	print("Placez vos bateaux !\n")
	while bateaux != []:
		bateaux_lettre.sort()
		bateaux = trierBateaux(bateaux)
		bateaux2 = trierBateaux(bateaux2,True)
		print("Sélectionnez vos bateaux.\n")
		print("Bateaux non placés: \n " + str(bateaux))
		demanderCoordonnees()
		bateaux_lettre.sort()
		bateaux = trierBateaux(bateaux)
		bateaux2 = trierBateaux(bateaux2,True)
		rep4=''
		while rep4 not in [i for i in ['a','b','c','d','e'] if i not in bateaux_lettre] and rep4!='n':
			rep4=input("Voulez-vous supprimer un bateau du plateau '" + str([i for i in ['a','b','c','d','e'] if i not in bateaux_lettre]) + ", 'n' (non)) ? ")
		if rep4!='n':
			RetirerBatSilent(bateaux2[[i for i in ['a','b','c','d','e'] if i not in bateaux_lettre].index(rep4)])
			print("Le bateau '" + str(rep4) + "' a bien été supprimé !")
	rep=''
	bateauxConf=bateaux2.copy()
	while bateauxConf != []:
		for i in bateauxConf.copy():
			rep=''
			bateauSelec=i
			while rep not in ['o', 'O', 'n', 'N']:
				rep=input("Confirmez la position du bateau: " + str(i) + " (bateau '" + bateauSelec[0][0] + "')" + " (O/N): ")
			if rep in ["N","n"]:
				RetirerBatSilent(bateauSelec)
				demanderCoordonnees(True)
			else:
				if i[0][0] in plateauJ:
					removeArray(bateauxConf,i)
					print("Bateau '" + str(i[0][0]) + "' prêt pour la bataille !\n")
				
def constructArray(array):
	chaine=[]
	string=''
	array=list(array)
	for i in array:
		string+=i
		if (array.index(i)+1)%10==0:
			chaine.append(string)
			string=''
		array[array.index(i)]='p'
	for i in range(0,len(chaine)):
		chaine[i]=list(chaine[i])
	return(chaine)
	
def printPlateau(plat):
	for i in range(0,10):
		if i==9:
			print(str(i + 1) + str(plat[i]))
		else:
			print(str(i + 1) + ' ' + str(plat[i]))
	print('    1   2   3   4   5   6   7   8   9   10')
	
def trierBateaux(batListe,bat2=False):
	bat=batListe.copy()
	if len(batListe)>1:
		for i in range(0,len(bat)):
			if bat2==False:
				nb=bateaux_lettre.index(batListe[i][0][0])
				batListe[nb],batListe[i] = batListe[i], batListe[nb]
			else:
				liste=[i for i in ['a','b','c','d','e'] if i not in bateaux_lettre]
				nb=liste.index(batListe[i][0][0])
				batListe[nb],batListe[i] = batListe[i], batListe[nb]
	return batListe

def removeArray(L,arr):
	ind = 0
	size = len(L)
	while ind != size and not np.array_equal(L[ind],arr):
		ind += 1
	if ind != size:
		L.pop(ind)
				
# Cette fonction gère l'ordinateur (placement de ses bateaux aléatoirement sur le terrain):
def Ordinateur():
	global plateauO, bateauSelec, bateaux_Ordi
	while bateaux_Ordi != []:
		for i in bateaux_Ordi:
			rand_rot=rd.randint(0,1)
			rand_x=rd.randint(1,10)
			rand_y=rd.randint(1,10)
			
			bateau=bateaux_Ordi[0]
			bateau=np.rot90(bateau,rand_rot)
			bateauSelec=i
			
			plateauO, b = poserBateauSel(rand_x-1,rand_y-1,plateauO)
			if b==True:
				if i.shape[0]==1:
					i=np.rot90(i)
				bateaux_Ordi=[ a for a in bateaux_Ordi if not (a==i).all()]

def Tirer():
	global plateauJ, plateauAtt, plateauO
	toucher_J=0
	toucher_O=0
	chars_J = ['a','b','c','d','e']
	chars_O = ['a','b','c','d','e']
	coord=(0,0)
	coords_list=[]
	double=False
	inverse=False
	while toucher_J<5 and toucher_O<5:
		''' Partie Joueur '''
		printPlateau(plateauAtt)
		print("-------------------------------------------")
		printPlateau(plateauJ)
		x=0
		y=0
		while (x<=0 or y<=0) or (x>=11 or y>=11) or plateauAtt[x-1][y-1] in ['o','x']:
			try:
				x=int(input("Coordonnée X du tir: "))
				y=int(input("Coordonnée Y du tir: "))
				print(" ")
			except:
				print("Entrée invalide ! Recommencez.")
				print(" ")
		if plateauO[x-1][y-1]==vide:
			print("Vous ne touchez rien !")
			plateauAtt[x-1][y-1]=tir_r
		else:
			print("Vous touchez un bateau ennemi !")
			plateauAtt[x-1][y-1]=tir_b
			plateauO[x-1][y-1]=vide
			for c in chars_J:
				if c not in plateauO:
					print("Vous avez coulé un bateau ennemi !")
					toucher_J+=1
					chars_J.remove(c)
		''' Partie Ordinateur '''
		rand_x=0
		rand_y=0
		while (rand_x<=0 or rand_y<=0) or (rand_x>=11 or rand_y>=11) or plateauJ[rand_x-1][rand_y-1] not in ['a','b','c','d','e','-']:
			if coord==(0,0) and double==False:
				inverse=False
				rand_x=rd.randint(1,10)
				rand_y=rd.randint(1,10)
			elif double==False:
				rand_x, rand_y = coords_list.pop()
			elif double==True:
				if plateauJ[coord[0]-1][coord[1]-1] == 'o':
					inverse=True
				for i in coords_list:
					if plateauJ[i[0]-1][i[1]-1]=='x':
						if coord[1]==i[1]:
							if inverse==False:
								rand_x=min(coord[0],i[0])-1
								rand_y=i[1]
							else:
								rand_x=max(coord[0],i[0])+1
								rand_y=i[1]
						elif coord[0]==i[0]:
							if inverse==False:
								rand_x=i[0]
								rand_y=min(coord[1],i[1])-1
							else:
								rand_x=i[0]
								rand_y=max(coord[1],i[1])+1
						coord=(rand_x, rand_y)
						coords_list=[(rand_x-1, rand_y),(rand_x, rand_y+1),(rand_x+1, rand_y),(rand_x, rand_y-1)]
						for i in coords_list.copy():
							if (i[0]<=0 or i[1]<=0) or (i[0]>=11 or i[1]>=11):
								coords_list.remove((i[0],i[1]))
				if (rand_x<=0 or rand_y<=0) or (rand_x>=11 or rand_y>=11):
					if inverse==True:
						double=False
						coord=(0,0)
						coords_list=[]
						inverse=False
					else:
						inverse=True
		if plateauJ[rand_x-1][rand_y-1]==vide:
			print("L'Ordinateur a raté son coup !")
			plateauJ[rand_x-1][rand_y-1]=tir_r
			if double==True:
				if inverse==True:
					double=False
					coord=(0,0)
					coords_list=[]
					inverse=False
				else:
					inverse=True
		else:
			print("L'Ordinateur a touché un de vos bateaux !")
			plateauJ[rand_x-1][rand_y-1]=tir_b
			if coord != (0,0):
				double=True
			coord=(rand_x, rand_y)
			coords_list=[(rand_x-1, rand_y),(rand_x, rand_y+1),(rand_x+1, rand_y),(rand_x, rand_y-1)]
			for i in coords_list.copy():
				if (i[0]<=0 or i[1]<=0) or (i[0]>=11 or i[1]>=11):
					coords_list.remove((i[0],i[1]))
			for c in chars_O:
				if c not in plateauJ:
					print("L'Ordinateur a coulé un de vos bateaux !")
					toucher_O+=1
					chars_O.remove(c)
					double=False
					coord=(0,0)
					coords_list=[]
					inverse=False
	gagnant = ['le Joueur', "l'Ordinateur"][[toucher_J, toucher_O].index(5)]
	return 'Bravo pour %s qui remporte la partie.' %gagnant

defPlateau()
printPlateau(plateauJ)
placerBateau()
p=plateauJ
Ordinateur()
plateauJ=p
print(Tirer())
