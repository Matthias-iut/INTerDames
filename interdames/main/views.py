from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


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
