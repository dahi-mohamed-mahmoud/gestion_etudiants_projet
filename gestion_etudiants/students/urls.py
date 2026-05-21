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
    path('cours/', views.liste_matieres, name='liste_matieres'),
    path('cours/nouveau/', views.creer_matiere, name='creer_matiere'),
    path('cours/<int:pk>/modifier/', views.modifier_matiere, name='modifier_matiere'),
    path('cours/<int:pk>/supprimer/', views.supprimer_matiere, name='supprimer_matiere'),
    path('examens/', views.liste_examens, name='liste_examens'),
    path('examens/nouveau/', views.creer_examen, name='creer_examen'),
    path('examens/<int:pk>/modifier/', views.modifier_examen, name='modifier_examen'),
    path('examens/<int:pk>/supprimer/', views.supprimer_examen, name='supprimer_examen'),
    path('inscriptions/', views.liste_inscriptions, name='liste_inscriptions'),
    path('inscriptions/nouveau/', views.creer_inscription, name='creer_inscription'),
    path('inscriptions/<int:pk>/modifier/', views.modifier_inscription, name='modifier_inscription'),
    path('inscriptions/<int:pk>/supprimer/', views.supprimer_inscription, name='supprimer_inscription'),
]
