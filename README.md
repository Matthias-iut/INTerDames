# INTerDames

L'objectif est de faire un Jeu de Dames à l'image de Chess.com pour les échecs, qui n'existe pas actuellement pour les passionnés du jeu.

# Lancer le projet

A compléter

# Compte par défaut

admin / projetinfo2a

# RoadMap

[x] ce qui a déjà été fait
[] ce qu'il reste à faire

[] Prise d'un pion
[] transformation d'un pion en dame
[] prise obligatoire
[] système d'authentification
[] création de la room
[] bloqué la room à 2 joueurs
[] début de partie
[] fin de partie
[] création du damier
[] cliquer sur un pion et le déplacer
[] correction des pages d'erreur (404 et 500)
[] room visibles dans l'admin
[] Dockerfile + gunicorn
[] pouvoir coller et envoyer des URLs
[] Boutons de connexion / déconnexion
[] page d'inscription


# Modèle de donnée


# Règles choisies

Règles du Jeu de Dames

Règle générale
Le jeu se pratique sur un damier de 10 cases sur 10, orienté avec une case foncée en bas à gauche. Chaque joueur possède 20 pions, placés sur les cases foncées des 4 premières rangées.
Les joueurs jouent chacun leur tour. Les blancs commencent toujours. 
Le but du jeu est de capturer tous les pions adverses. Si un joueur ne peut plus bouger, même s'il lui reste des pions, il perd la partie. Chaque pion peut se déplacer d'une case vers l'avant en diagonale. Un pion arrivant sur la dernière rangée et s'y arrêtant est promu en « dame ». Il est alors doublé (on pose dessus un deuxième pion de sa couleur). La dame se déplace sur une même diagonale d'autant de cases qu'elle le désire, en avant et en arrière.

La prise par un pion
Un pion peut en prendre un autre en sautant par dessus le pion adverse pour se rendre sur la case vide située derrière celui-ci. Le pion sauté est retiré du jeu. La prise peut également s'effectuer en arrière. La prise est obligatoire. Si, après avoir pris un premier pion, vous vous retrouvez de nouveau en position de prise, vous devez continuer, jusqu'à ce que cela ne soit plus possible. Les pions doivent être enlevés à la fin de la prise et non pas un par un au fur et à mesure.

La prise majoritaire
Lorsque plusieurs prises sont possibles, il faut toujours prendre du côté du plus grand nombre de pièces. Cela signifie que si on peut prendre une dame ou deux pions, il faut prendre les deux pions.

La prise par la dame
Puisque la dame a une plus grande marge de manœuvre, elle a aussi de plus grandes possibilités pour les prises. La dame doit prendre tout pion situé sur sa diagonale (s'il y a une case libre derrière) et doit changer de direction à chaque fois qu'une  nouvelle prise est possible. On ne peut passer qu'une seule fois sur un même pion. En revanche, on peut passer deux fois sur la même case.

#Crée un environnement
python -m venv venv
venv\Scripts\activate

#Requirements
pour installer les dépendances, faire à chaque fois
pip install -r requirements.txt

#faire les migrations
python manage.py makemigrations
python manage.py migrate
python manage.py runserver