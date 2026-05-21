import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q, Avg, Count
from django.http import HttpResponse
from .models import Etudiant, Filiere, Matiere, Note, Inscription
from .forms import EtudiantForm, NoteForm, RechercheForm, MatiereForm, ExamenForm, InscriptionForm


@login_required
def dashboard(request):
    total_etudiants = Etudiant.objects.count()
    total_actifs = Etudiant.objects.filter(statut='actif').count()
    total_filieres = Filiere.objects.count()
    etudiants_recents = Etudiant.objects.order_by('-created_at')[:5]
    stats_filiere = Filiere.objects.annotate(nb=Count('etudiants')).order_by('-nb')

    context = {
        'total_etudiants': total_etudiants,
        'total_actifs': total_actifs,
        'total_filieres': total_filieres,
        'etudiants_recents': etudiants_recents,
        'stats_filiere': stats_filiere,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
def liste_etudiants(request):
    form = RechercheForm(request.GET or None)
    etudiants = Etudiant.objects.select_related('filiere').all()

    if form.is_valid():
        q = form.cleaned_data.get('query')
        filiere = form.cleaned_data.get('filiere')
        statut = form.cleaned_data.get('statut')
        niveau = form.cleaned_data.get('niveau')

        if q:
            etudiants = etudiants.filter(
                Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(cne__icontains=q) | Q(email__icontains=q)
            )
        if filiere:
            etudiants = etudiants.filter(filiere=filiere)
        if statut:
            etudiants = etudiants.filter(statut=statut)
        if niveau:
            etudiants = etudiants.filter(niveau=niveau)

    return render(request, 'students/liste.html', {'etudiants': etudiants, 'form': form})


@login_required
def detail_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    notes = etudiant.notes.select_related('matiere').order_by('annee_academique', 'matiere__nom')
    moyenne = etudiant.moyenne_generale()
    return render(request, 'students/detail.html', {
        'etudiant': etudiant,
        'notes': notes,
        'moyenne': moyenne,
    })


@login_required
def creer_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            etudiant = form.save()
            messages.success(request, f"Étudiant {etudiant.nom_complet} créé avec succès.")
            return redirect('detail_etudiant', pk=etudiant.pk)
    else:
        form = EtudiantForm()
    return render(request, 'students/form.html', {'form': form, 'titre': 'Nouvel étudiant'})


@login_required
def modifier_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        form = EtudiantForm(request.POST, request.FILES, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Fiche mise à jour avec succès.")
            return redirect('detail_etudiant', pk=etudiant.pk)
    else:
        form = EtudiantForm(instance=etudiant)
    return render(request, 'students/form.html', {'form': form, 'titre': 'Modifier l\'étudiant', 'etudiant': etudiant})


@login_required
def supprimer_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        nom = etudiant.nom_complet
        etudiant.delete()
        messages.success(request, f"Étudiant {nom} supprimé.")
        return redirect('liste_etudiants')
    return render(request, 'students/confirmer_suppression.html', {'etudiant': etudiant})


@login_required
def ajouter_note(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.etudiant = etudiant
            note.save()
            messages.success(request, "Note ajoutée avec succès.")
            return redirect('detail_etudiant', pk=pk)
    else:
        form = NoteForm()
    return render(request, 'students/form_note.html', {'form': form, 'etudiant': etudiant})


@login_required
def export_releve_csv(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    notes = etudiant.notes.select_related('matiere').order_by('annee_academique')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="releve_{etudiant.cne}.csv"'
    response.write('\ufeff')  # BOM pour Excel

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['CNE', 'Nom', 'Prénom', 'Filière', 'Matière', 'Note', 'Session', 'Année'])
    for note in notes:
        writer.writerow([
            etudiant.cne, etudiant.nom, etudiant.prenom,
            etudiant.filiere.nom, note.matiere.nom,
            note.note, note.get_session_display(), note.annee_academique
        ])

    return response


@login_required
def liste_matieres(request):
    query = request.GET.get('q', '').strip()
    matieres = Matiere.objects.select_related('filiere').all()

    if query:
        matieres = matieres.filter(
            Q(code__icontains=query) | Q(nom__icontains=query) | Q(filiere__nom__icontains=query)
        )

    return render(request, 'students/courses_list.html', {
        'matieres': matieres,
        'query': query,
    })


@login_required
def creer_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            matiere = form.save()
            messages.success(request, f"Cours {matiere.code} créé avec succès.")
            return redirect('liste_matieres')
    else:
        form = MatiereForm()

    return render(request, 'students/course_form.html', {
        'form': form,
        'titre': 'Nouveau cours',
    })


@login_required
def modifier_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)

    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, "Cours mis à jour avec succès.")
            return redirect('liste_matieres')
    else:
        form = MatiereForm(instance=matiere)

    return render(request, 'students/course_form.html', {
        'form': form,
        'titre': f'Modifier le cours {matiere.code}',
        'matiere': matiere,
    })


@login_required
def supprimer_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)

    if request.method == 'POST':
        code = matiere.code
        matiere.delete()
        messages.success(request, f"Cours {code} supprimé.")
        return redirect('liste_matieres')

    return render(request, 'students/course_confirm_delete.html', {'matiere': matiere})


@login_required
def liste_examens(request):
    query = request.GET.get('q', '').strip()
    examens = Note.objects.select_related('etudiant', 'matiere', 'etudiant__filiere').order_by('-created_at')

    if query:
        examens = examens.filter(
            Q(etudiant__nom__icontains=query)
            | Q(etudiant__prenom__icontains=query)
            | Q(etudiant__cne__icontains=query)
            | Q(matiere__code__icontains=query)
            | Q(matiere__nom__icontains=query)
            | Q(annee_academique__icontains=query)
        )

    return render(request, 'students/exams_list.html', {
        'examens': examens,
        'query': query,
    })


@login_required
def creer_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Examen enregistré avec succès.")
                return redirect('liste_examens')
            except Exception:
                form.add_error(None, "Un examen existe déjà pour cet étudiant, cette matière, cette session et cette année.")
    else:
        form = ExamenForm()

    return render(request, 'students/exam_form.html', {
        'form': form,
        'titre': 'Nouvel examen',
    })


@login_required
def modifier_examen(request, pk):
    examen = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Examen mis à jour avec succès.")
                return redirect('liste_examens')
            except Exception:
                form.add_error(None, "Conflit de duplication détecté pour cet examen.")
    else:
        form = ExamenForm(instance=examen)

    return render(request, 'students/exam_form.html', {
        'form': form,
        'titre': 'Modifier examen',
        'examen': examen,
    })


@login_required
def supprimer_examen(request, pk):
    examen = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        examen.delete()
        messages.success(request, "Examen supprimé.")
        return redirect('liste_examens')

    return render(request, 'students/exam_confirm_delete.html', {'examen': examen})


@login_required
def liste_inscriptions(request):
    query = request.GET.get('q', '').strip()
    inscriptions = Inscription.objects.select_related('etudiant', 'filiere').all()

    if query:
        inscriptions = inscriptions.filter(
            Q(etudiant__nom__icontains=query)
            | Q(etudiant__prenom__icontains=query)
            | Q(etudiant__cne__icontains=query)
            | Q(filiere__nom__icontains=query)
            | Q(annee_academique__icontains=query)
        )

    return render(request, 'students/inscriptions_list.html', {
        'inscriptions': inscriptions,
        'query': query,
    })


@login_required
def creer_inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Inscription créée avec succès.")
                return redirect('liste_inscriptions')
            except IntegrityError:
                form.add_error(None, "Cet étudiant est déjà inscrit pour cette année académique.")
    else:
        form = InscriptionForm()

    return render(request, 'students/inscription_form.html', {
        'form': form,
        'titre': 'Nouvelle inscription',
    })


@login_required
def modifier_inscription(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)

    if request.method == 'POST':
        form = InscriptionForm(request.POST, instance=inscription)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Inscription mise à jour avec succès.")
                return redirect('liste_inscriptions')
            except IntegrityError:
                form.add_error(None, "Conflit de duplication pour cette année académique.")
    else:
        form = InscriptionForm(instance=inscription)

    return render(request, 'students/inscription_form.html', {
        'form': form,
        'titre': 'Modifier inscription',
        'inscription': inscription,
    })


@login_required
def supprimer_inscription(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)

    if request.method == 'POST':
        inscription.delete()
        messages.success(request, "Inscription supprimée.")
        return redirect('liste_inscriptions')

    return render(request, 'students/inscription_confirm_delete.html', {'inscription': inscription})
