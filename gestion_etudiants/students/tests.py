from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Etudiant, Filiere, Matiere, Note
import datetime


class FiliereModelTest(TestCase):
    def setUp(self):
        self.filiere = Filiere.objects.create(nom="Informatique", code="INFO")

    def test_str(self):
        self.assertEqual(str(self.filiere), "INFO - Informatique")

    def test_code_unique(self):
        with self.assertRaises(Exception):
            Filiere.objects.create(nom="Info2", code="INFO")


class EtudiantModelTest(TestCase):
    def setUp(self):
        self.filiere = Filiere.objects.create(nom="Informatique", code="INFO")
        self.etudiant = Etudiant.objects.create(
            cne="G123456789",
            nom="Dupont",
            prenom="Jean",
            date_naissance=datetime.date(2000, 1, 15),
            sexe="M",
            email="jean.dupont@test.com",
            filiere=self.filiere,
            niveau=2,
            annee_inscription=2022,
            statut="actif",
        )

    def test_nom_complet(self):
        self.assertEqual(self.etudiant.nom_complet, "Jean Dupont")

    def test_str(self):
        self.assertIn("G123456789", str(self.etudiant))

    def test_moyenne_sans_notes(self):
        self.assertIsNone(self.etudiant.moyenne_generale())

    def test_moyenne_avec_notes(self):
        matiere = Matiere.objects.create(nom="Algo", code="ALGO", filiere=self.filiere)
        Note.objects.create(etudiant=self.etudiant, matiere=matiere, note=14, annee_academique="2024-2025")
        Note.objects.create(etudiant=self.etudiant, matiere=Matiere.objects.create(nom="Maths", code="MATH", filiere=self.filiere), note=16, annee_academique="2024-2025")
        self.assertEqual(self.etudiant.moyenne_generale(), 15.0)

    def test_cne_unique(self):
        with self.assertRaises(Exception):
            Etudiant.objects.create(
                cne="G123456789", nom="X", prenom="Y",
                date_naissance=datetime.date(2001, 1, 1),
                sexe="M", email="autre@test.com",
                filiere=self.filiere, niveau=1,
                annee_inscription=2023, statut="actif"
            )


class NoteModelTest(TestCase):
    def setUp(self):
        self.filiere = Filiere.objects.create(nom="Informatique", code="INFO2")
        self.etudiant = Etudiant.objects.create(
            cne="G999", nom="Test", prenom="User",
            date_naissance=datetime.date(2001, 5, 10),
            sexe="F", email="test@test.com",
            filiere=self.filiere, niveau=1,
            annee_inscription=2023, statut="actif"
        )
        self.matiere = Matiere.objects.create(nom="POO", code="POO", filiere=self.filiere)

    def test_note_valide(self):
        note = Note.objects.create(
            etudiant=self.etudiant, matiere=self.matiere,
            note=12.5, annee_academique="2024-2025"
        )
        self.assertEqual(note.note, 12.5)

    def test_str_note(self):
        note = Note.objects.create(
            etudiant=self.etudiant, matiere=self.matiere,
            note=15, annee_academique="2024-2025"
        )
        self.assertIn("15", str(note))


class ViewsAuthTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='testpass123')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/')

    def test_dashboard_authenticated(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tableau de bord")

    def test_liste_etudiants(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('liste_etudiants'))
        self.assertEqual(response.status_code, 200)

    def test_creer_etudiant_get(self):
        self.client.login(username='admin', password='testpass123')
        response = self.client.get(reverse('creer_etudiant'))
        self.assertEqual(response.status_code, 200)

    def test_creer_etudiant_post(self):
        self.client.login(username='admin', password='testpass123')
        filiere = Filiere.objects.create(nom="Informatique", code="INF3")
        data = {
            'cne': 'G111222333',
            'nom': 'Martin',
            'prenom': 'Sophie',
            'date_naissance': '2001-03-15',
            'sexe': 'F',
            'email': 'sophie.martin@test.com',
            'filiere': filiere.pk,
            'niveau': 1,
            'annee_inscription': 2023,
            'statut': 'actif',
        }
        response = self.client.post(reverse('creer_etudiant'), data)
        self.assertEqual(Etudiant.objects.filter(cne='G111222333').count(), 1)
