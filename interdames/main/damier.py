from .cache_partie import statut_partie
from .salleDeJeu import jeu

def ma_couleur(partie, pseudo):
    if partie['joueur1'] == pseudo:
        return 'blanc'
    return 'noir'

def fabriquer_cases(plateau, coups, depart):
    cases = [] # on transforme le plateau en une liste de cases plus facile a afficher dans le template
    for l in range(10):
        ligne = []
        for c in range(10):
            case = {}
            case['l'] = l
            case['c'] = c
            case['piece'] = plateau[l][c]
            if (l + c) % 2 == 1:
                case['couleur'] = 'foncee'
            else:
                case['couleur'] = 'claire'
            case['cliquable'] = False
            case['selection'] = False
            case['rond_vert'] = False
            for coup in coups:
                if coup['depart'] == [l, c]:
                    case['cliquable'] = True
                
                if depart != None and coup['depart'] == depart and coup['chemin'][-1] == [l, c]:
                    case['rond_vert'] = True
            if depart == [l, c] and case['cliquable'] == True:
                case['selection'] = True
            ligne.append(case)
        cases.append(ligne)
    return cases

def contexte_zone(partie, pseudo, lien, depart=None, message=''):
    statut = statut_partie(partie)
    couleur = ma_couleur(partie, pseudo)
    coups = []
    if statut == 'en_cours' and partie['tour'] == couleur:
        coups = jeu.coups_max(partie['plateau'], couleur)
    contexte = {}
    contexte['partie'] = partie
    contexte['statut'] = statut
    contexte['couleur'] = couleur
    contexte['cases'] = fabriquer_cases(partie['plateau'], coups, depart)
    contexte['lien'] = lien
    contexte['message'] = message
    print(coups)
    return contexte

