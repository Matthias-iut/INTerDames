import secrets #pour le token unique

from django.db import models


class salleDeJeu(models.Model):
<<<<<<< HEAD
    token = models.CharField(
        max_length=64,
        unique=True,
        default=secrets.token_urlsafe,
    )
=======
    class Statut(models.TextChoices):
        ATTENTE = 'attente', 'En attente'
        EN_COURS = 'en_cours', 'En cours'
        TERMINEE = 'terminee', 'Terminée'
>>>>>>> 3deecb01e702368c1a494d70b5591abaa319c6b8

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

<<<<<<< HEAD
    def isFull(self):
        return self.user1Pseudo != '' and self.user2Pseudo != ''
=======
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # sert dans le lien de partage
    player_white = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games_as_white')
    player_black = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games_as_black', null=True, blank=True)
    statut = models.CharField(max_length=12, choices=Statut.choices, default=Statut.ATTENTE)
    current_turn = models.CharField(max_length=1, choices=Color.choices, default=Color.WHITE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.CLASSIC)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
>>>>>>> 3deecb01e702368c1a494d70b5591abaa319c6b8

    
    def statut(self):
        if self.active == False:
            return 'finie'
        if self.isFull() == False:
            return 'attente'
        return 'en_cours'

<<<<<<< HEAD
    def __str__(self):
        return 'Salle '+self.token
=======

class Pawn(models.Model):
    game = models.ForeignKey(salleDeJeu, on_delete=models.CASCADE, related_name='pawns')
    color = models.CharField(max_length=1, choices=salleDeJeu.Color.choices)
    is_queen = models.BooleanField(default=False)
    x = models.PositiveSmallIntegerField(null=True, blank=True)  # null = capturé
    y = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['game', 'x', 'y'], name='one_pawn_per_square')]


class Move(models.Model):
    game = models.ForeignKey(salleDeJeu, on_delete=models.CASCADE, related_name='moves')
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE, related_name='moves')
    from_x = models.PositiveSmallIntegerField()
    from_y = models.PositiveSmallIntegerField()
    to_x = models.PositiveSmallIntegerField()
    to_y = models.PositiveSmallIntegerField()
    captured_pawn = models.ForeignKey(Pawn, on_delete=models.SET_NULL, null=True, blank=True, related_name='captured_in')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
>>>>>>> 3deecb01e702368c1a494d70b5591abaa319c6b8
