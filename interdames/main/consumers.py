from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from django.template.loader import render_to_string
from .cache_partie import enregistrer_partie, lire_partie
from .damier import contexte_zone


from .salleDeJeu import jeu

class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):

        self.token = self.scope['url_route']['kwargs']['token']
        self.groupe = 'room_' + self.token
        async_to_sync(self.channel_layer.group_add)(self.groupe, self.channel_name)
        self.accept()

        self.send(text_data='<p id="etat-connexion">Connecté au serveur</p>')



    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.groupe, self.channel_name)

    def receive_json(self, contenu):
        if contenu.get('action') == 'choisir':
            self.choisir(contenu)

        if contenu.get('action') == 'jouer':
            self.jouer(contenu)


    def lire_case(self, contenu):
        try:
            return [int(contenu.get('ligne')), int(contenu.get('colonne'))]
        except (TypeError, ValueError):
            return None


    def choisir(self, contenu):
        self.depart = self.lire_case(contenu)
        self.envoyer_zone('')


    def jouer(self, contenu):
        arrivee = self.lire_case(contenu)
        partie = lire_partie(self.token)
        nouvelle_partie, erreur = jeu.tour_joueur(partie, self.pseudo, self.depart, arrivee)
        self.depart = None
        if erreur != '':
            self.envoyer_zone(erreur)
            return
        enregistrer_partie(nouvelle_partie)
        async_to_sync(self.channel_layer.group_send)(self.groupe, {'type': 'maj_room'})


    def maj_room(self, evenement):
        self.depart = None
        self.envoyer_zone('')


    def envoyer_zone(self, message):
        partie = lire_partie(self.token)
        contexte = contexte_zone(partie, self.pseudo, '', self.depart, message)
        self.send(text_data=render_to_string('main/zone_jeu.html', contexte))
