from .cache_partie import statut_partie

def ma_couleur(partie, pseudo):
    if partie['joueur1'] == pseudo:
        return 'blanc'
    return 'noir'

def fabriquer_cases(plateau):
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
            ligne.append(case)
        cases.append(ligne)
    return cases

def contexte_zone(partie, pseudo, lien):
    contexte = {}
    contexte['partie'] = partie
    contexte['statut'] = statut_partie(partie)
    contexte['couleur'] = ma_couleur(partie, pseudo)
    contexte['cases'] = fabriquer_cases(partie['plateau'])
    contexte['lien'] = lien
    return contexte

