from django import forms
from .models import Etudiant, Note, Filiere


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = [
            'cne', 'nom', 'prenom', 'date_naissance', 'sexe', 'email',
            'telephone', 'adresse', 'filiere', 'niveau', 'annee_inscription',
            'statut', 'photo'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'adresse': forms.Textarea(attrs={'rows': 3}),
            'cne': forms.TextInput(attrs={'placeholder': 'Ex: G123456789'}),
            'email': forms.EmailInput(attrs={'placeholder': 'etudiant@example.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs['class'] = 'form-control'


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['matiere', 'note', 'session', 'annee_academique']
        widgets = {
            'annee_academique': forms.TextInput(attrs={'placeholder': 'Ex: 2024-2025'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class RechercheForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom, prénom, CNE...'})
    )
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(),
        required=False,
        empty_label="Toutes les filières",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        choices=[('', 'Tous les statuts')] + Etudiant.STATUT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    niveau = forms.IntegerField(
        required=False,
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Niveau'})
    )
