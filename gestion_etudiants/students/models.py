from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Etudiant(models.Model):
    SEXE_CHOICES = [('M', 'Masculin'), ('F', 'Féminin')]
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('diplome', 'Diplômé'),
        ('abandonne', 'Abandonné'),
    ]

    cne = models.CharField(max_length=20, unique=True, verbose_name="CNE")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.PROTECT, related_name='etudiants')
    niveau = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Niveau d'études (1 à 5)"
    )
    annee_inscription = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='actif')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.cne})"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def moyenne_generale(self):
        notes = self.notes.all()
        if not notes:
            return None
        return round(sum(n.note for n in notes) / len(notes), 2)


class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    coefficient = models.FloatField(default=1.0)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='matieres')
    niveau = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Note(models.Model):
    SESSION_CHOICES = [
        ('normale', 'Session normale'),
        ('rattrapage', 'Rattrapage'),
    ]

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='notes')
    note = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    session = models.CharField(max_length=20, choices=SESSION_CHOICES, default='normale')
    annee_academique = models.CharField(max_length=9)  # ex: 2024-2025
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        unique_together = ['etudiant', 'matiere', 'session', 'annee_academique']

    def __str__(self):
        return f"{self.etudiant} - {self.matiere}: {self.note}/20"
