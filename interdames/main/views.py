from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import salleDeJeu
from .salleDeJeu import jeu


def accueil(request):
    #si l'user est connecté, on le redireige vers le salon
    if request.user.is_authenticated:
        return redirect('salon')
    erreur = ''
    # l'user n'est pas conncté :

    # on vérifie si le formulaire de connexion a été soumis
    if request.method == 'POST':
        pseudo = request.POST.get('username')
        mdp = request.POST.get('password')
        
        utilisateur = authenticate(request, username=pseudo, password=mdp)
        if utilisateur != None:
            login(request, utilisateur)
            return redirect('salon')
        else:
            erreur = 'Pseudo ou mot de passe incorrect'
    return render(request, 'main/accueil.html', {'erreur': erreur})


def inscription(request):
    erreur = ''
    if request.method == 'POST':
        pseudo = request.POST.get('pseudo', '')
        mdp = request.POST.get('mdp', '')
        mdp2 = request.POST.get('mdp2', '')
        if pseudo == '':
            erreur = 'Il faut mettre un pseudo'
        elif len(pseudo) > 10:
            erreur = 'Le pseudo doit faire 10 caractères maximum'
        elif User.objects.filter(username=pseudo).exists():
            erreur = 'Ce pseudo est déjà pris'
        elif mdp == '':
            erreur = 'Il faut mettre un mot de passe'
        elif mdp != mdp2:
            erreur = 'Les deux mots de passe ne sont pas pareils'
        else:
            utilisateur = User.objects.create_user(username=pseudo, password=mdp)
            login(request, utilisateur)
            return redirect('salon')
    return render(request, 'main/inscription.html', {'erreur': erreur})

def deconnexion(request):
    logout(request)
    return redirect('accueil')

# deconexion de l'user
@login_required
def salon(request):
    return render(request, 'main/salon.html')


# création d'une room
@login_required
def creer_room(request):
    if request.method == 'POST': 
        nouvelle_room = salleDeJeu.objects.create(player_white=request.user)
        return redirect('room', token=nouvelle_room.id)
    return redirect('salon')

@login_required
def room(request, token):
    la_room = get_object_or_404(salleDeJeu, id=token) 
    utilisateur = request.user
    # si l'user n'est pas dans la room, on l'ajoute en tant que user2
    if la_room.player_white != utilisateur and la_room.player_black is None:
        la_room.player_black = utilisateur
        la_room.save()
        
    if la_room.player_white != utilisateur and la_room.player_black != utilisateur:
        return render(request, 'main/salon.html', {'erreur': 'Cette room est déjà pleine (2 joueurs max)'})   
    lien = request.build_absolute_uri()
    return render(request, 'main/room.html', {'room': la_room, 'lien': lien})

@login_required
def rejoindre(request):
    if request.method == 'POST':
        lien = request.POST.get('lien', '')
        morceaux = lien.strip().strip('/').split('/')
        token = morceaux[-1]
        if salleDeJeu.objects.filter(id=token).exists() == False:
            return render(request, 'main/salon.html', {'erreur': "Ce lien est pas valide"})
        return redirect('room', token=token)
    
    return redirect('salon')


def fabriquer_cases(la_room):
    # on transforme le plateau en une liste de cases 
    cases = []
    for l in range(10):
        ligne = []
        for c in range(10):
            # enregistre coordonnés et état de la case  
            case = {} 
            case['l'] = l
            case['c'] = c
            case['piece'] = la_room.pawns.filter(x=c, y=l).first() # on récupère le pion sur cette case, s'il y en a un
            #alterne les couleurs des cases avec parité
            if (l + c) % 2 == 1:
                case['couleur'] = 'foncee'
            else:
                case['couleur'] = 'claire'
            ligne.append(case)
        cases.append(ligne)
    return cases


