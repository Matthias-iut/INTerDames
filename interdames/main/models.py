import secrets #pour le token unique

from django.db import models


class salleDeJeu(models.Model):
    token = models.CharField(
        max_length=64,
        unique=True,
        default=secrets.token_urlsafe,
    )

    user1Pseudo = models.CharField(
        max_length=10 )

    user2Pseudo = models.CharField(
        max_length=10,
        blank=True,)
    dateCreation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) 
    plateau = models.JSONField(default=list, blank=True)
    tour = models.CharField(max_length=5, default='blanc')
    gagnant = models.CharField(max_length=10, blank=True)

    def isFull(self):
        return self.user1Pseudo != '' and self.user2Pseudo != ''

    
    def statut(self):
        if self.active == False:
            return 'finie'
        if self.isFull() == False:
            return 'attente'
        return 'en_cours'

    def __str__(self):
        return 'Salle '+self.token
