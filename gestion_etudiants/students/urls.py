from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('etudiants/', views.liste_etudiants, name='liste_etudiants'),
    path('etudiants/nouveau/', views.creer_etudiant, name='creer_etudiant'),
    path('etudiants/<int:pk>/', views.detail_etudiant, name='detail_etudiant'),
    path('etudiants/<int:pk>/modifier/', views.modifier_etudiant, name='modifier_etudiant'),
    path('etudiants/<int:pk>/supprimer/', views.supprimer_etudiant, name='supprimer_etudiant'),
    path('etudiants/<int:pk>/note/', views.ajouter_note, name='ajouter_note'),
    path('etudiants/<int:pk>/releve/', views.export_releve_csv, name='export_releve'),
]
