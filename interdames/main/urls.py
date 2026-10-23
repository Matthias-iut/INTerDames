from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('salon/', views.salon, name='salon'),
    path('room/creer/', views.creer_room, name='creer_room'),
    path('room/<str:token>/', views.room, name='room'),
    path('room/rejoindre/', views.rejoindre, name='rejoindre'),
]

