from django.contrib import admin
from .models import Etudiant, Filiere, Matiere, Note


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom']
    search_fields = ['code', 'nom']


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['cne', 'nom', 'prenom', 'filiere', 'niveau', 'statut']
    list_filter = ['filiere', 'niveau', 'statut', 'sexe']
    search_fields = ['cne', 'nom', 'prenom', 'email']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'filiere', 'niveau', 'coefficient']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['etudiant', 'matiere', 'note', 'session', 'annee_academique']
    list_filter = ['session', 'annee_academique', 'matiere__filiere']
