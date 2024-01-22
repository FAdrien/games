import numpy as np
from time import time
# le fichier Katamino12.txt contient les 1010 solutions avec les 12 penta, il a fallu environ 5h de calculs
#Les 12 pentaminos
penta0 = np.array([['a'],['a'],['a'],['a'],['a']])
penta1 = np.array([['b','-'],['b','-'],['b','-'],['b','b']])
penta2 = np.array([['-','c'],['c','c'],['-','c'],['-','c']])
penta3 = np.array([['-','d'],['-','d'],['d','d'],['d','-']])
penta4 = np.array([['-','-','e'],['-','-','e'],['e','e','e']])
penta5 = np.array([['f','f'],['f','f'],['f','-']])
penta6 = np.array([['g','-','g'],['g','g','g']])
penta7 = np.array([['h','h','-'],['-','h','-'],['-','h','h']])
penta8 = np.array([['-','i','i'],['i','i','-'],['-','i','-']])
penta9 = np.array([['j','j','j'],['-','j','-'],['-','j','-']])
penta10 = np.array([['-','-','k'],['-','k','k'],['k','k','-']])
penta11 = np.array([['-','l','-'],['l','l','l'],['-','l','-']])
penta12 = np.array([['m','-','m'],['-','m','-'],['m','-','m']])
#La liste de tous les pentaminos, dans l'ordre croissant (NB: toutes les pièces de jeu ont 5 blocs solides)
pentaminos = [penta0,penta1,penta2,penta3,penta4,penta5,penta6,penta7,penta8,penta9,penta10,penta11,penta12]
# liste des pentaminos avec leurs rotations et symétries (listes de listes), elle sera construite automatiquement
Pentaminos = [] 
# lettres associées aux pentaminos
piecesconstituants = ['a','b','c','d','e','f','g','h','i','j','k','l','m']
# Une case vide du plateau de jeu
vide = '-'
# variables globales
Niveau = 0
plateau = [] #Le plateau de jeu
piecesAplacer = [] #numéros des pièces à placer en fonction du niveau du jeu
OK = False # pour s'arrêter dès qu'on a trouvé
essais = 0 # compteur d'essais effectués
Solutions = [] # pour la recherche exhaustive
visites = []

def CreerPentaminos(): # créer la liste des copies des pentaminos
    global Pentaminos
    nbRot = [2,4,4,4,4,4,4,2,4,4,4,1,0] # nb de rotations à faire par penta
    nbSym = [0,1,1,1,0,1,0,1,1,0,0,0,0] # nb sym à faire par penta
    for k in range(13):
        piece = pentaminos[k] # piece d'origine
        Penta = [ np.rot90(piece,k) for k in range(nbRot[k]) ] #copies par rotations
        if nbSym[k] == 1:
            aux = np.transpose(piece) # symétrique d l'origine
            Penta += [ np.rot90(aux,k) for k in range(nbRot[k]) ] #copies par rotations
        Pentaminos.append(Penta)

CreerPentaminos() # créer la liste des pentaminos avec leurs copies

def defPlateau(Aplacer): # créer le plateau de jeu en fonction des pièces à placer
    global plateau
    global Niveau
    global piecesAplacer
    global OK
    OK = False
    essais = 0
    Niveau = len(Aplacer)
    ligne = [vide]*Niveau, #on crée les lignes du tableau (il y a "niveau" fois le nombre de cases)
    plateau = np.array(5*ligne) #on crée le plateau de jeu en créant 5 lignes
    piecesAplacer = Aplacer
    piecesAplacer.sort() # on trie les numéros des pièces à placer
    
def placerPenta(pantaNum, x, y, k):
    piece = Pentaminos[pantaNum-1][k]
    return compatible(piece, x, y)
    
def enleverPiece(pantaNum):
    global plateau
    plateau = np.char.replace(plateau, piecesconstituants[pantaNum-1], vide) # on remplace la lettre du penta par du vide
    
def longBloc(tableau,i,j,Long, vues) :# calcule si (i,j) est dans un bloc de longueur Long, renvoie la longueur trouvée (au plus Long)
    global Niveau, visites
    rep = 1
    vues  += [(i,j)]
    visites += [(i,j)]
    if Long > 1 :
        if i>0 and tableau[i-1,j]==vide and not((i-1,j) in vues):
            rep +=  longBloc(tableau,i-1,j,Long-rep,vues) # on cherche à gauche
        if (rep<Long) and i<4 and tableau[i+1,j]==vide and not((i+1,j) in vues):
            rep += longBloc(tableau,i+1,j,Long-rep,vues) # on cherche à droite
        if (rep<Long) and j>0 and tableau[i,j-1]==vide and not((i,j-1) in vues):
            rep += longBloc(tableau,i,j-1,Long-rep,vues) # on cherche en haut
        if (rep<Long) and j<Niveau-1 and tableau[i,j+1]==vide and not((i,j+1) in vues):
            rep += longBloc(tableau,i,j+1,Long-rep,vues) # on cherche en bas
    return rep 
          
def compatible(piece, x, y): # teste si la pièce est posable à l'emplacement (i,j)
    global Niveau,plateau, visites
    lg,col = piece.shape
    poser = (x+lg<=5) and (y+col<=Niveau) # est-ce que la pièce tient sur le plateau ?
    i = 0
    while poser and i<lg:
        j = 0
        while poser and j<col:
            if (piece[i,j] != vide) and (plateau[x+i,y+j] != vide): 
                poser = False # pièce non posable
            j += 1
        i += 1
    if poser: # on pose la pièce sur un plateau temporaire
        tableau = plateau.copy()
        lg,col = piece.shape # Nombre de lignes et nombre de colonnes d'une pièce de jeu
        for i in range(lg):
            for j in range(col):
                if piece[i,j] != vide:
                    tableau[x+i,y+j] = piece[i,j] #On met la pièce sur le plateau
        i = -1  # on va tester s'il n'y a pas de blocs de moins de cinq cases vides contigues autour de la pièce
        visites = []
        while poser and i<lg+1:
            j = -1
            a = x+i
            while poser and j<col+1:
                b = y+j
                vues2=[]
                if (-1<a<5) and (-1<b<Niveau) and (tableau[a,b] == vide) and not((a,b) in visites) :
                    if (longBloc(tableau,a,b,5,vues2)<5):
                        poser = False # il y a une case vide qui n'est pas dans un bloc d'au moins 5 cases vides
                j += 1
            i += 1
        if poser: # pas de soucis
            plateau = tableau
    return poser
         
def remplir(num) : #num entre 1 et Niveau
    global piecesAplacer
    global plateau
    global OK, Niveau, essais
    if num == 0: # le plateau est plein
        print(plateau)
        Solutions.append(plateau.copy())
        OK = True
    else : # on cherche à placer la piecesAplacer[num-1]
        pentaNum = piecesAplacer[num-1]
        nbCopies = len(Pentaminos[pentaNum-1]) # nombre de copies de la pièce à tester
        x = 0
        while not(OK) and x<5:
            y = 0
            while not(OK) and y<Niveau:
                k = 0
                while not(OK) and k < nbCopies:
                    if placerPenta(pentaNum, x, y, k):
                            essais+=1
                            remplir(num-1)
                            enleverPiece(pentaNum)
                    k+=1
                y+=1
            x+=1
            
def SauveSolutions():
    global Solutions
    name = input("Nom du fichier = ")
    f = open(name,"w")
    for sol in Solutions :
        for k in sol:
            f.writelines(list(k)+['\n'])
        f.write('\n')
    f.close()
            
def ToutTrouver(num) : #num entre 1 et Niveau
    global piecesAplacer
    global plateau
    global Niveau
    if num == 0: # le plateau est plein
        Solutions.append(plateau.copy())
    else : # on cherche à placer la piecesAplacer[num-1]
        pentaNum = piecesAplacer[num-1]
        nbCopies = len(Pentaminos[pentaNum-1]) if pentaNum !=6 else 2 if Niveau!=5 else 1# nombre de copies de la pièce à tester
        for x in range(5):
            for y in range(Niveau):
                for k in range(nbCopies):
                    if placerPenta(pentaNum, x, y, k):
                        ToutTrouver(num-1)
                        enleverPiece(pentaNum)

defPlateau([1,2,3,5,6,7,8,9,10,11,12])
t1=time()
#ToutTrouver(Niveau) # recherche exhaustive de toutes les solutions
remplir(Niveau) # recherche d'une seule solution
t2=time()
#SauveSolutions()
print("Niveau = "+str(Niveau))
print((t2-t1))
print("Nombres d'essais = "+str(essais))
print("Nombres de solutions = "+str(len(Solutions)))
