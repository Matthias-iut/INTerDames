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

def position_valide(ligne,colonne): #sert de "debuggueur"
    if ligne <0 or ligne >9 or colonne <0 or colonne >9:
        return False
    return True

#print(position_valide(6,10))

def copier_plateau(plateau):
    copie = []
    for ligne in range(10):
        copie_ligne = []
        for colonne in range(10):
            copie_ligne.append(plateau[ligne][colonne])
        copie.append(copie_ligne)
    return copie

def plateau_test():
    plateau = []
    for i in range(10):
        plateau.append([""] * 10)
        print(plateau[i])

    plateau[5][2] = "b"
    plateau[4][3] = "n"
    plateau[2][5] = "n"

    return plateau

#print(plateau_test())

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
                    action.append({"depart": [ligne, colonne], "chemin"
                                   : [[nouvelle_ligne, nouvelle_colonne]], "prises": []})
                    #ajout de "départ", "chemin" et "prises"
                    #obligatoire pour la fonction rajouter "action_joue"
                    #crée un dictionnaire référençant la position de départ, le chemin et les prises
    return action
#si position_valide==False, il n'y a pas de case à vérifier, donc on ne fait rien
        
#ligne=6
#colonne=3
#print(deplacement_pion_possibles(plateau_depart(),ligne,colonne))



Directions=[[-1,-1],[-1,1],[1,-1],[1,1]] #les 4 directions possibles pour les déplacements et les prises

def recherche_prises(plateau,ligne, colonne,piece,prise_effectuees):
    suite=[]
    couleur=couleur_de_piece(piece)
    for d in Directions:
        l_adv=ligne+d[0]
        c_adv=colonne+d[1]  #emplacement de la pièce adverse
        l_arrivee=ligne+2*d[0]
        c_arrivee=colonne+2*d[1]    #emplacement de la case d'arrivée après la prise
        if position_valide(l_arrivee,c_arrivee)==False:
            continue #assure que la case d'arrivée est bien sur le plateau
        if couleur_de_piece(plateau[l_adv][c_adv])!=couleur_adversaire(piece):
            continue #assure que la piéce en diagonale est bien adverse
        if [l_adv,c_adv] in prise_effectuees:
            continue #assure qu'on ne peut pas prendre 2 fois la même pièce
        if plateau[l_arrivee][c_arrivee]!="":
            continue #assure que la case d'arrivée est bien vide, n'arrive normalement jamais
        else:
            prise=[l_adv,c_adv]
            arrivee=[l_arrivee,c_arrivee]
            rec=recherche_prises(plateau,l_arrivee,c_arrivee,piece,prise_effectuees+[prise]) #on ajoute la prise effectuée à la liste des prises
            if len(rec)==0:     #si on ne peut plus prendre de pièces
                suite.append({"depart":[ligne,colonne],"chemin":[arrivee],"prises":[prise]})
            else:
                for s in rec:   #on regarde tous les récursivités
                    suite.append({"depart":[ligne,colonne],"chemin":[arrivee]+s["chemin"],"prises":[prise]+s["prises"]})
    return suite
#print(recherche_prises(plateau_depart(),6,3,"b",[]))

def prises_possibles(plateau, ligne, colonne):
    piece=plateau[ligne][colonne]
    if piece=="":
        return [] #on s'assure que la case contient bien une pièce
    else:
        copie=copier_plateau(plateau) #pouvoir modifier le plateau sans modifier la partie en cours 
        copie[ligne][colonne]="" #on enlève la pièce de la case au cas où elle revienne à cette position
        recherche=recherche_prises(copie,ligne,colonne,piece,[])
        coups=[]
        for r in recherche: #au cas où il y a plusieurs chemins possibles
            coups.append({"depart":[ligne,colonne],"chemin":r["chemin"],"prises":r["prises"]})
    return coups

#print(prises_possibles(plateau_depart(),6,3))

def action_joue(plateau, action):
    coups_joue = copier_plateau(plateau)  # on crée une copie du plateau pour ne pas modifier l'original
    
    depart_ligne = action["depart"][0]
    depart_colonne = action["depart"][1]
    arrivee = action["chemin"][-1] #recupère la dernière case du chemin, utile si la pièce parcourt plusieurs cases
    piece = coups_joue[depart_ligne][depart_colonne]
    coups_joue[depart_ligne][depart_colonne] = ""
    coups_joue[arrivee[0]][arrivee[1]] = piece
    for p in action["prises"]: #on supprime les pièces prises du plateau
        coups_joue[p[0]][p[1]] = ""
    return coups_joue

#print(action_joue(plateau_test(),prises_possibles(plateau_test(),5,2)[0]))


#print(action_joue(plateau_test(), {"depart": [5, 2], "chemin": [[4, 3]], "prises": []}))

def coups_max(plateau, couleur):
    prises = []
    for ligne in range(10):
        for colonne in range(10):
            if couleur_de_piece(plateau[ligne][colonne]) == couleur: #on regarde en priorite tous les pions qui peuvent manger des pions adverses
                for coup in prises_possibles(plateau, ligne, colonne):
                    prises.append(coup)
    if len(prises) > 0:
        maximum = 0
        for coup in prises:
            if len(coup["prises"]) > maximum:   #on garde le nombre maximum de pions adv que l'on peut manger
                maximum = len(coup["prises"])   
        meilleures = []
        for coup in prises:
            if len(coup["prises"]) == maximum:  #on garde les pions qui peuvent manger le plus de pions adv
                meilleures.append(coup)
        return meilleures
    deplacements = []
    for ligne in range(10):
        for colonne in range(10):
            if couleur_de_piece(plateau[ligne][colonne]) == couleur:
                for coup in deplacement_pion_possibles(plateau, ligne, colonne):
                    deplacements.append(coup)
    return deplacements


