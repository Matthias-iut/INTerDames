from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('salon/', views.salon, name='salon'),
]