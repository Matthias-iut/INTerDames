import json

from django.core.cache import cache
from .models import salleDeJeu

def cle_cache(token):
    return 'partie_' + token


def room_vers_partie(la_room):

    partie = {}
    partie['token'] = la_room.token
    partie['joueur1'] = la_room.user1Pseudo
    partie['joueur2'] = la_room.user2Pseudo
    partie['plateau'] = la_room.plateau
    partie['tour'] = la_room.tour
    partie['active'] = la_room.active
    partie['gagnant'] = la_room.gagnant
    return partie


def lire_partie(token):

    texte = cache.get(cle_cache(token))
    if texte != None:
        return json.loads(texte)
    la_room = salleDeJeu.objects.filter(token=token).first()
    if la_room == None:
        return None
    partie = room_vers_partie(la_room)
    cache.set(cle_cache(token), json.dumps(partie), 3000)
    return partie


def enregistrer_partie(partie):

    la_room = salleDeJeu.objects.get(token=partie['token'])
    la_room.plateau = partie['plateau']
    la_room.tour = partie['tour']
    la_room.active = partie['active']
    la_room.gagnant = partie['gagnant']
    la_room.save()

    cache.set(cle_cache(partie['token']), json.dumps(partie), 3000)


def oublier_partie(token):

    cache.delete(cle_cache(token))


def statut_partie(partie):

    if partie['active'] == False:
        return 'finie'
    if partie['joueur2'] == '':
        return 'attente'
    return 'en_cours'