from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


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

        pass
