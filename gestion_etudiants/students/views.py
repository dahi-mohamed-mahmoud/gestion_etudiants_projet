import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import HttpResponse
from .models import Etudiant, Filiere, Matiere, Note
from .forms import EtudiantForm, NoteForm, RechercheForm


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
