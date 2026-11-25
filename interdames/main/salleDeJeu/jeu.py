##Rappels des règles
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

def couleur_de_piece(piece):
    if piece == "n" or piece == "N": #MAJ de la fonction pour prendre en compte les dames
        return "noir"
    elif piece == "b" or piece == "B":
        return "blanc"
    else:
        return "Il n'y a pas de pièce sur cette case"

#print (couleur_de_piece("n"))

def promotion_dame(plateau, action,piece):
    arrivee=action["chemin"][-1]  #récupère la dernière case du chemin
    if piece == "b" and arrivee[0] == 0:
        plateau[0][arrivee[1]] = "B"
    elif piece == "n" and arrivee[0] == 9:
        plateau[9][arrivee[1]] = "N"

    return plateau
#a partir de maintenant, N ou B designeront les dames

#print(promotion_dame(plateau_test(), {"depart": [6, 1], "chemin": [[5, 0]]}, "b"))

def couleur_adversaire(piece):
    if piece == "n" or piece == "N":
        return "blanc"
    elif piece == "b" or piece == "B":
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

Directions=[[-1,-1],[-1,1],[1,-1],[1,1]] #les 4 directions possibles pour les déplacements et les prises

def deplacement_pion_possibles(plateau, ligne, colonne):
    piece=plateau[ligne][colonne]
    action=[]
    if piece=="":
        return action
    
    if piece=="B" or piece=="N": #si c'est une dame, on peut se déplacer dans toutes les directions
        for d in Directions:
            nouvelle_ligne=ligne+d[0]
            nouvelle_colonne=colonne+d[1]
            while position_valide(nouvelle_ligne,nouvelle_colonne)==True and plateau[nouvelle_ligne][nouvelle_colonne]=="":
                action.append({"depart": [ligne, colonne], "chemin"
                               : [[nouvelle_ligne, nouvelle_colonne]], "prises": []})
                nouvelle_ligne+=d[0]
                nouvelle_colonne+=d[1]
        
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

def recherche_prises(plateau,ligne, colonne,piece,prise_effectuees):
    suite=[]
    couleur=couleur_de_piece(piece)
    for d in Directions:
        #cas des dames
        if piece=="B" or piece=="N": #si c'est une dame, on peut prendre dans toutes les directions
            l_diag=ligne+d[0]
            c_diag=colonne+d[1]
            while position_valide(l_diag,c_diag)==True and plateau[l_diag][c_diag]=="":
                l_diag+=d[0]
                c_diag+=d[1]
            if position_valide(l_diag,c_diag)==False:
                            continue
            if couleur_de_piece(plateau[l_diag][c_diag])!=couleur_adversaire(piece):
                continue
            if [l_diag,c_diag] in prise_effectuees:
                continue
            prise=[l_diag,c_diag]
            l_opps=l_diag+d[0]
            c_opps=c_diag+d[1]
            while position_valide(l_opps,c_opps)==True and plateau[l_opps][c_opps]=="":
                arrivee=[l_opps,c_opps]
                rec=recherche_prises(plateau,l_opps,c_opps,piece,prise_effectuees+[prise])
                if len(rec)==0:
                    suite.append({"depart":[ligne,colonne],"chemin":[arrivee],"prises":[prise]}) #on ajoute le coup à la liste des coups possibles
                else:
                    for s in rec:
                        suite.append({"depart":[ligne,colonne],"chemin":[arrivee]+s["chemin"],"prises":[prise]+s["prises"]})
                l_opps+=d[0]
                c_opps+=d[1]
            continue
        #modification de la fonction qui ajoutait des cases au lieu de coups

        #cas des pions
        else:
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

        prise=[l_adv,c_adv]
        arrivee=[l_arrivee,c_arrivee]
        rec=recherche_prises(plateau,l_arrivee,c_arrivee,piece,prise_effectuees+[prise]) #on ajoute la prise effectuée à la liste des prises
        if position_valide(l_adv,c_adv) == False:
            continue
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
    coups_joue = promotion_dame(coups_joue, action, piece) #on vérifie si la pièce est promue en dame
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

#print(coups_max(plateau_test(), "blanc"))

def total_pieces(plateau):
    total = {"blanc": 0, "noir": 0}
    for ligne in range(10):
        for colonne in range(10):
            piece = plateau[ligne][colonne]
            if piece == "b" or piece == "B":
                total["blanc"] += 1
            elif piece == "n" or piece == "N":
                total["noir"] += 1
    return total

#print(total_pieces(plateau_depart()))

def gagnant(plateau,couleur):
    total = total_pieces(plateau)
    if couleur == "blanc":
        adversaire = "noir"
    else:
        adversaire = "blanc"
    if total[couleur] == 0:
        return adversaire
    elif len(coups_max(plateau, couleur)) == 0:
        return adversaire
    else:
        return None
#modification de la fonction qui faisait terminer la partie si un joueur
#ne pouvait pas jouer alors que ce n'était pas son tour.

#print(gagnant(plateau_depart(), "blanc"))


#la fonction en dessous est en cours

#partie = {"plateau": plateau_depart(),
#  "joueur1": "Alice", 
# "joueur2": "Bob", 
# "tour_actuel": "blanc", 
# "active": True}


def tour_joueur(partie, pseudo, depart, arrivee):
    if partie["active"] == False:
        return "En recherche de joueurs"
    if partie["joueur2"] == "":
        return "En recherche de joueurs"
    if partie["joueur1"] == pseudo:
        couleur = "blanc"
    elif partie["joueur2"] == pseudo:
        couleur = "noir"
    else:
        return "Erreur ! Vous n'êtes pas dans cette partie"
    if partie["tour_actuel"] != couleur:
        return "Erreur ! Ce n'est pas votre tour"

    for coup in coups_max(partie["plateau"], couleur):
        if coup["depart"]==depart and coup["arrivee"]==arrivee:
            return coup
        else:
            return "Erreur ! Coup invalide"
    tour_suivant = partie.copy()
    tour_suivant["plateau"] = action_joue(partie["plateau"], coup)
    if couleur == "blanc":
        tour_suivant["tour_actuel"] = "noir"
    else:
        tour_suivant["tour_actuel"] = "blanc"
    if gagnant(tour_suivant["plateau"], tour_suivant["tour_actuel"]) != None:
        tour_suivant["active"] = False
        tour_suivant["gagnant"] = pseudo
    return tour_suivant