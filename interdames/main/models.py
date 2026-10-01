from django.db import models


class User(models.Model):
    """Modèle représentant un utilisateur"""
    name = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Position(models.Model):
    """Modèle représentant une position sur le plateau"""
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()

    def __str__(self):
        return f"({self.pos_x}, {self.pos_y})"

    class Meta:
        unique_together = ('pos_x', 'pos_y')


class Pawn(models.Model):
    """Modèle représentant un pion"""
    PAWN_TYPES = [
        ('PAWN', 'Pion'),
        ('QUEEN', 'Reine'),
    ]

    type = models.CharField(max_length=10, choices=PAWN_TYPES)
    alive_status = models.BooleanField(default=True)
    position = models.OneToOneField(Position, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_type_display()} - {'Alive' if self.alive_status else 'Captured'}"


class Board(models.Model):
    """Modèle représentant un plateau de jeu"""
    white_pawns = models.ManyToManyField(Pawn, related_name='board_white')
    black_pawns = models.ManyToManyField(Pawn, related_name='board_black')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Board {self.id}"


class Game(models.Model):
    """Modèle représentant une partie"""
    STATUS_CHOICES = [
        (True, 'En cours'),
        (False, 'Terminée'),
    ]

    MODE_CHOICES = [
        ('CLASSIC', 'Classique'),
        ('BLITZ', 'Blitz'),
    ]

    game_id = models.AutoField(primary_key=True)
    player_white_pseudo = models.CharField(max_length=16)
    player_black_pseudo = models.CharField(max_length=16)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)
    current_player = models.CharField(max_length=16)
    board = models.OneToOneField(Board, on_delete=models.CASCADE)
    winner_pseudo = models.CharField(max_length=16, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='CLASSIC')

    def __str__(self):
        return f"Game {self.game_id} - {self.player_white_pseudo} vs {self.player_black_pseudo}"

    class Meta:
        ordering = ['-created_at']


class Move(models.Model):
    """Modèle représentant un mouvement"""
    move_id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='move_history')
    player_pseudo = models.CharField(max_length=16)
    pawn = models.ForeignKey(Pawn, on_delete=models.CASCADE)
    from_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='moves_from')
    to_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='moves_to')
    captured_position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True, related_name='captures')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Move {self.move_id} - {self.player_pseudo}"

    class Meta:
        ordering = ['timestamp']


class Player(models.Model):
    """Modèle d'association entre User et Game"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_white = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.name} - Game {self.game.game_id}"

    class Meta:
        unique_together = ('user', 'game')