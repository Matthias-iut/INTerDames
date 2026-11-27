from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import salleDeJeu
from .cache_partie import oublier_partie, lire_partie
from .damier import contexte_zone#, fabriquer_cases
from .salleDeJeu import jeu

def accueil(request):
    if request.user.is_authenticated:
        return redirect('salon')
    erreur = ''

    if request.method == 'POST':
        pseudo = request.POST.get('pseudo')
        mdp = request.POST.get('mdp')
        
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


@login_required
def salon(request):
    return render(request, 'main/salon.html')




@login_required
def creer_room(request):
    if request.method == 'POST':
        nouvelle_room = salleDeJeu()
        nouvelle_room.user1Pseudo = request.user.username
        nouvelle_room.plateau = jeu.plateau_depart()
        nouvelle_room.save()
        return redirect('room', token=nouvelle_room.token)
    return redirect('salon')

@login_required
def room(request, token):
    la_room = get_object_or_404(salleDeJeu, token=token)
    pseudo = request.user.username
    if la_room.user1Pseudo != pseudo and la_room.isFull() == False:
        la_room.user2Pseudo = pseudo
        la_room.save()
        oublier_partie(la_room.token)

    if la_room.user1Pseudo != pseudo and la_room.user2Pseudo != pseudo:
        return render(request, 'main/salon.html', {'erreur': 'Cette room est déjà pleine (2 joueurs max)'})
    if len(la_room.plateau) == 0:
        la_room.plateau = jeu.plateau_depart()
        la_room.save()
        oublier_partie(la_room.token)
    partie = lire_partie(la_room.token)
    
    lien = request.build_absolute_uri()
    
    contexte = contexte_zone(partie, pseudo, lien)
    contexte['room'] = la_room
    return render(request, 'main/room.html', contexte)

    

def ma_couleur(la_room, utilisateur):
    if la_room.user1Pseudo == utilisateur.username:
        return 'blanc'
    if la_room.user2Pseudo == utilisateur.username:
        return 'noir'
    return None



@login_required
def coups(request, token):
    # appele par HTMX quand on clique sur un pion
    la_room = get_object_or_404(salleDeJeu, token=token)
    couleur = ma_couleur(la_room, request.user)
    if couleur == None:
        return HttpResponseForbidden("Tu ne joues pas dans cette room")
    try:
        depart = [int(request.GET.get('l')), int(request.GET.get('c'))]
    except:
        depart = None
    cases = fabriquer_cases(la_room, couleur, depart)
    return render(request, 'main/zone_jeu.html', {'room': la_room, 'cases': cases, 'couleur': couleur})


@login_required
def rejoindre(request):
    if request.method == 'POST':
        lien = request.POST.get('lien', '')

        morceaux = lien.strip().strip('/').split('/')
        token = morceaux[len(morceaux) - 1]
        if salleDeJeu.objects.filter(token=token).exists() == False:
            return render(request, 'main/salon.html', {'erreur': "Ce lien n'est pas valide"})
        return redirect('room', token=token)
    return redirect('salon')