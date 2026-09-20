import secrets #utile pour générer un token unique pour chaque salle de jeu

from django.db import models


class salleDeJeu(models.Model):
    token = models.CharField(
        max_length=64, #on fixe une longueur maximale suffisament longue pour ne jamais être atteinte
        unique=True, #permet de créer une url unique pour chaque salle de jeu
        default=secrets.token_urlsafe, #découvert pendant le débugging, permet de générer un token unique pour chaque salle de jeu s'il n'est pas fourni lors de la création de l'objet
    )

    user1Pseudo = models.CharField(
        max_length=10 #on prend un nombre faible pour limiter les caractères du pseudo
    )

    user2Pseudo = models.CharField(
        max_length=10,
        blank=True, #permet de laisser le champ vide si l'utilisateur 2 n'est pas encore présent
    )

    dateCreation = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def isFull(self):
        return self.user1Pseudo is not None and self.user2Pseudo is not None