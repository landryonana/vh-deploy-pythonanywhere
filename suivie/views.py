from history.models import History
import suivie
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404


from suivie.forms import SuivieForm, SearchForm
from remplissages.models import Evangelisation, Person, Site, Suivie


@login_required
def index_suivie(request):
    context = dict()
    last_suivi = None
    last_suivi_date = None
    person_oui = None
    person_non = None
    person_ras = None
    person_deja = None
    suivie_person = Person.objects.all()
    form = SearchForm()
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            last_suivi = suivie_person.filter(date=query)
            person_oui = last_suivi.filter(accepte_jesus='oui').count()
            person_non = last_suivi.filter(accepte_jesus='non').count()
            person_ras = last_suivi.filter(accepte_jesus='ras').count()
            person_deja = last_suivi.filter(accepte_jesus='déjà').count()
            last_suivi_date = query
    else:
        last_suivi = suivie_person
        person_oui = suivie_person.filter(accepte_jesus='oui').count()
        person_non = suivie_person.filter(accepte_jesus='non').count()
        person_ras = suivie_person.filter(accepte_jesus='ras').count()
        person_deja = suivie_person.filter(accepte_jesus='déjà').count()

    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']
    
    if request.session.get('add_suivi_personne'):
        context['add_suivi_personne'] = request.session.get('add_suivi_personne')
        del request.session['add_suivi_personne']

    context['active'] = 'index_suivie'
    context['person_oui'] = person_oui
    context['person_non'] = person_non
    context['person_ras'] = person_ras
    context['person_deja'] = person_deja
    context['last_suivi'] = last_suivi
    context['last_suivi_date'] = last_suivi_date
    context['form'] = form
    return render(request, 'suivie/index_suivie.html', context)



@login_required
def add_suivie(request, pk):
    context = dict()
    form = None
    suivi = get_object_or_404(Suivie, id=pk)
    if request.method == 'POST':
        form = SuivieForm(instance=suivi, data=request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(
                user=request.user,
                content_object=f"SUIVI:::{suivi}",
                action_type="ajout de"
            )
            request.session['is_update'] = True
            request.session['add_suivi_personne'] = f"{suivi.person}"
            return redirect('suivie:index_suivie')
    else:
        form = SuivieForm(instance=suivi)
    context['form'] = form
    return render(request, 'suivie/add_suivie.html', context)



@login_required
def search_suivie(request):
    return