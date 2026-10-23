from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

def accueil(request):
    erreur = ''

    if request.method == 'POST':
        pseudo = request.POST.get('username')
        mdp = request.POST.get('password')
        
        utilisateur = authenticate(request, username=pseudo, password=mdp)
        if utilisateur != None:
            login(request, utilisateur)
            return redirect('accueil')
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
            return redirect('accueil')
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

    if la_room.user1Pseudo != pseudo and la_room.user2Pseudo != pseudo:
        return render(request, 'main/salon.html', {'erreur': 'Cette room est déjà pleine (2 joueurs max)'})
    lien = request.build_absolute_uri()
    
    
    return render(request, 'main/room.html', {'room': la_room, 'lien': lien})

@login_required
def rejoindre(request):
    if request.method == 'POST':
        lien = request.POST.get('lien', '')

        morceaux = lien.strip().strip('/').split('/')
        token = morceaux[len(morceaux) - 1]
        if salleDeJeu.objects.filter(token=token).exists() == False:
            return render(request, 'main/salon.html', {'erreur': "Ce lien est pas valide"})
        return redirect('room', token=token)
    
    return redirect('salon')

