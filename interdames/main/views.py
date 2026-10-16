from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def accueil(request):
    return render(request, 'main/accueil.html')


@login_required
def salon(request):
    return render(request, 'main/salon.html')