from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.template.loader import render_to_string
from .cache_partie import lire_partie
from .damier import contexte_zone


class RoomConsumer(JsonWebsocketConsumer):
    def connect(self):

        self.token = self.scope['url_route']['kwargs']['token']
        self.pseudo = self.scope['user'].username
        self.groupe = 'room_' + self.token
        self.depart = None
        async_to_sync(self.channel_layer.group_add)(self.groupe, self.channel_name)
        self.accept()

        self.send(text_data='<p id="etat-connexion">Connecté au serveur</p>')



    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.groupe, self.channel_name)

    def receive_json(self, contenu):
        #print(1)
        if contenu.get('action') == 'choisir':
            self.choisir(contenu)

    def lire_case(self,contenu):
        try:
            return [int(contenu.get('ligne')), int(contenu.get('colonne'))]
        except (TypeError, ValueError):
            return None

    def choisir(self, contenu):
        self.depart = self.lire_case(contenu)
        # print(0)
        self.envoyer_zone('')

    def envoyer_zone(self, message):
        partie = lire_partie(self.token)
        if partie is None:
            return
        contexte = contexte_zone(partie, self.pseudo, '', self.depart, message)
        self.send(text_data=render_to_string('main/zone_jeu.html', contexte))

