#Rappels des règles
#Plateau de jeu : 10 x 10 cases
#case foncé en bas à gauche
#chaque joueur a 20 pions sur les cases foncées des 4 premières lignes de son côté du plateau
#les blancs commencent toujours

def plateau_depart():
    plateau = []
    for ligne in range(10):
        chaque_ligne = []
        for colonne in range(10):
            if (ligne + colonne) % 2 == 1:
                if ligne < 4:
                    chaque_ligne.append("n")
                elif ligne > 5:
                    chaque_ligne.append("b")
                else:
                    chaque_ligne.append("")
            else:
                chaque_ligne.append("")
        plateau.append(chaque_ligne)
    return plateau

#print (plateau_depart())

def couleur_de_piece(piece):
    if piece == "n":
        return "noir"
    elif piece == "b":
        return "blanc"
    else:
        return "erreur"

#print (couleur_de_piece("n"))

def couleur_adversaire(piece):
    if piece == "n":
        return "blanc"
    elif piece == "b":
        return "noir"
    else:
        return "erreur"

#print (couleur_adversaire("n"))

def position_valide(ligne,colonne):
    if ligne <0 or ligne >9 or colonne <0 or colonne >9:
        return False
    return True

#print(position_valide(6,10))

def deplacement_pion_possibles(plateau, ligne, colonne):
    piece=plateau[ligne][colonne]
    action=[]
    if piece=="":
        return action
    else:
        if couleur_de_piece(piece)=="blanc":
            sens=-1  #les lignes diminuent pour les blancs
        else:
            sens=1   #les lignes augmentent pour les noirs
        for diag in [-1, 1]:  #les diagonales gauche et droite
            nouvelle_ligne=ligne+sens
            nouvelle_colonne=colonne+diag
            if position_valide(nouvelle_ligne,nouvelle_colonne)==True:
                if plateau[nouvelle_ligne][nouvelle_colonne]=="":
                    action.append((nouvelle_ligne, nouvelle_colonne))
    return action
#si position_valide==False, il n'y a pas de case à vérifier, donc on ne fait rien
        
#ligne=6
#colonne=3
#print(deplacement_pion_possibles(plateau_depart(),ligne,colonne))


