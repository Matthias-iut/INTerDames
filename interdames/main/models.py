import uuid
from django.conf import settings
from django.db import models


class Game(models.Model):
    class Status(models.TextChoices):
        WAITING = 'WAITING', 'En attente'
        IN_PROGRESS = 'IN_PROGRESS', 'En cours'
        FINISHED = 'FINISHED', 'Terminée'

    class Color(models.TextChoices):
        WHITE = 'W', 'Blanc'
        BLACK = 'B', 'Noir'

    class Mode(models.TextChoices):
        CLASSIC = 'CLASSIC', 'Classique'
        BLITZ = 'BLITZ', 'Blitz'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # sert dans le lien de partage
    player_white = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games_as_white')
    player_black = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='games_as_black', null=True, blank=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.WAITING)
    current_turn = models.CharField(max_length=1, choices=Color.choices, default=Color.WHITE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_won')
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.CLASSIC)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Pawn(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='pawns')
    color = models.CharField(max_length=1, choices=Game.Color.choices)
    is_queen = models.BooleanField(default=False)
    x = models.PositiveSmallIntegerField(null=True, blank=True)  # null = capturé
    y = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['game', 'x', 'y'], name='one_pawn_per_square')]


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='moves')
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