from history.models import History
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import render_to_string

from remplissages.forms import EvangForm, PersonForm, SiteForm, PersonFormUpdate
from remplissages.models import Evangelisation, Person, Site, Suivie



@login_required
def index_rempl(request, passe=None, pk=None):
    evang_oui = None
    evang_non = None
    personnes = None
    context = dict() 

    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']

    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']

    if passe and pk:
        data = dict()
        evang_modal = None
        evang_modal = get_object_or_404(Evangelisation, pk=pk)
        personnes_evang_modal = Person.objects.filter(date=evang_modal.day)
        context = {'evang_oui': evang_modal, 'personnes_evang_oui': personnes_evang_modal, 'passe':passe}

        if request.session.get('personne'):
            context['personne'] = request.session.get('personne')
            del request.session['personne']
        
        if request.session.get('personne_nom_passe'):
            context['personne_nom_passe'] = request.session.get('personne_nom_passe')
            del request.session['personne_nom_passe']

        data['evang_detail'] = render_to_string('remplissages/modal/evang-detail.html', context, request=request)
        return JsonResponse(data)
    else:
        evang_oui = Evangelisation.objects.filter(actif="oui")
        evang_non = Evangelisation.objects.filter(actif="non")
        if len(evang_oui)==0:
                context['pas_de_oui'] = True
        elif len(evang_oui)!=1:
            context['plusieur_oui'] = True
        else:
            evang_oui = evang_oui.last()
            if evang_oui is not None:
                context['evang_oui_boss'] = evang_oui.boss.all()
                context['evang_oui'] = evang_oui
                context['personnes_evang_oui'] = Person.objects.filter(date=evang_oui.day)

        if len(evang_non)==0:
                context['pas_de_non'] = True
        elif len(evang_non)==len(Evangelisation.objects.all()):
            context['tout_est_non'] = True

    #============================ADD var session IN CONTEXT==============================

    if request.session.get('evang_session'):
        context['evang_session'] = request.session.get('evang_session')
        del request.session['evang_session']
    
    if request.session.get('personne_update'):
        context['personne_update'] = request.session.get('personne_update')
        del request.session['personne_update']
    #===========================END========================================================

    #===============================personnes
    personnes = Person.objects.all()
    context['personnes'] = personnes
    active = "index_rempl"
    context['active'] = active
    
    return render(request, 'remplissages/index.html',context)


#==============================================================================================================
#===============================CRUD EVANGELISSATION======================================
@login_required
def add_rempl(request):
    is_save = False
    evang = None
    context = dict()
    form = EvangForm(request.POST or None)
    if form.is_valid():
        evang = form.save(commit=False)
        evang.author = request.user
        evang.save()
        form.save_m2m()
        History.objects.create(
            user=request.user,
            content_object=f"{evang}",
            action_type="ajout de"
        )
        is_save = True
        request.session['is_save'] = is_save
        request.session['evang_ajouter'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
        return redirect('rempl:liste_site')

    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/evang/add_evang.html',context)



@login_required
def change_rempl(request, pk):
    evang = None
    is_update = False
    form = None
    context = dict()
    try:
        evang = Evangelisation.objects.get(id=pk)
    except Evangelisation.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method == 'POST':
        form = EvangForm(instance=evang, data=request.POST)
        if form.is_valid():
            form.save()
            History.objects.create(
                user=request.user,
                content_object=f"{evang}",
                action_type="mise à jour de"
            )
            is_update = True
            context['is_update'] = is_update 
            request.session['is_update_list'] = is_update
            request.session['evang_update'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
            return redirect('rempl:liste_site')
    else:
        form = EvangForm(instance=evang)
    
    context['form'] = form
    context['evang'] = evang
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/evang/update_evang.html', context)



@login_required
def delete_rempl(request, pk):
    is_delete = False
    context = dict()
    evang =None
    try:
        evang = Evangelisation.objects.get(id=pk)
    except Evangelisation.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['evang_delete'] = {'id':evang.id, 'evang_date':f"{evang.day.day}/{evang.day.month}/{evang.day.year}"}
        History.objects.create(
            user=request.user,
            content_object=f"{evang}",
            action_type="suppresion de"
        )
        evang.delete()
        is_delete = True
        request.session['is_delete'] = is_delete
        return redirect('rempl:liste_site')

    context = {'evang':evang}
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/evang/delete_evang.html', context)



#==============================================================================================================
#===============================CRUD PERSONNE======================================
@login_required
def add_personne(request, pk=None, passe=None):
    is_save = False
    personne = None
    evangelisation = None
    oui_many = False
    passe1 = None
    pk1 = None
    passe1 = passe
    pk1 = pk
    request.session['evang_add_personne'] = {'passe':passe1, 'pk':pk1}
    context = dict()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if request.session.get('evang_add_personne'):
            passe1 = request.session.get('evang_add_personne')['passe']
            pk1 = request.session.get('evang_add_personne')['pk']
        if form.is_valid():
            personne = form.save(commit=False)
            personne.author = request.user
            passe1 = request.session.get('evang_add_personne')['passe']
            pk1 = request.session.get('evang_add_personne')['pk']
            if passe1 and pk1:
                evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
                personne.evangelisation = evangelisation
                personne.date = evangelisation.day
                personne.save()
                form.save_m2m()
                History.objects.create(
                    user=request.user,
                    content_object=f"{personne}",
                    action_type="ajout de"
                )
                Suivie.objects.create(person=personne)
                History.objects.create(
                    user=request.user,
                    content_object=f"SUIVI:: de {personne}",
                    action_type="ajout de"
                )
                is_save = True
                request.session['is_save'] = is_save
                request.session['personne_nom_passe'] = personne.nom_et_prenom
                return redirect('rempl:liste_site')
            else:
                evangelisation = Evangelisation.objects.filter(actif="oui")
                if len(evangelisation)==1:
                    personne.evangelisation = evangelisation.last()
                    personne.date = evangelisation.last().day
                    personne.save()
                    form.save_m2m()
                    History.objects.create(
                        user=request.user,
                        content_object=f"{personne}",
                        action_type="ajout de"
                    )
                    Suivie.objects.create(person=personne)
                    History.objects.create(
                        user=request.user,
                        content_object=f"SUIVI:: de {personne}",
                        action_type="ajout de"
                    )
                    is_save = True
                    request.session['is_save'] = is_save
                    request.session['personne_nom'] = personne.nom_et_prenom
                    return redirect('rempl:add_personne')
                else:
                    oui_many = True
                    context['oui_many'] = oui_many
                    return redirect('rempl:add_personne')
        else:
            if request.session.get('evang_add_personne')['pk'] and request.session.get('evang_add_personne')['passe']:
                passe1 = request.session.get('evang_add_personne')['passe']
                pk1 = request.session.get('evang_add_personne')['pk']
                evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
                context['evangelisation'] = evangelisation
                context['passe'] = passe1
    else:
        form = PersonForm()

        if request.session.get('evang_add_personne')['pk'] and request.session.get('evang_add_personne')['passe']:
            passe1 = request.session.get('evang_add_personne')['passe']
            pk1 = request.session.get('evang_add_personne')['pk']
            evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
            context['evangelisation'] = evangelisation
            context['passe'] = passe1
    if passe1 and pk1:
        evangelisation = get_object_or_404(Evangelisation, id=int(pk1))
        context['evangelisation'] = evangelisation
        context['passe'] = passe1
    
    print(request.session.get('personne_nom'))
    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']

    if request.session.get('personne_nom'):
        context['personne_nom'] = request.session.get('personne_nom')
        del request.session['personne_nom']

    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/personne/add_person.html',context)


@login_required
def add_personne_autre(request):
    is_save = False
    personne = None
    context = dict()
    form = PersonForm(request.POST or None)
    if form.is_valid():
        personne = form.save(commit=False)
        personne.author = request.user
        personne.save()
        form.save_m2m()
        is_save = True
        request.session['is_save'] = is_save
        return redirect('rempl:add_personne_autre')
    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/personne/add_person.html',context)


@login_required
def change_personne(request, pk, passe=None):
    person = None
    is_update = False
    form = None
    passe1 = passe
    context = dict()
    request.session['passe'] = passe1
    try:
        person = Person.objects.get(id=pk)
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")

    if request.method == 'POST':
        form = PersonFormUpdate(instance=person, data=request.POST)
        if request.session.get('passe'):
            passe1 = request.session.get('passe')
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            History.objects.create(
                user=request.user,
                content_object=f"{person}",
                action_type="mise à jour de"
            )
            context['is_update'] = True 
            request.session['is_update'] = True
            request.session['personne_update'] = {'id':person.id, 'nom':person.nom_et_prenom}
            request.session['personne'] = {'id':person.id, 'nom':person.nom_et_prenom}
            if passe1:
                return redirect('rempl:liste_site')
            else:
                return redirect('rempl:index_rempl')
        else:
            if request.session.get('passe'):
                context['passe'] = request.session.get('passe')
    else:
        form = PersonFormUpdate(instance=person)
        if request.session.get('passe'):
            context['passe'] = request.session.get('passe')
    if passe1:
        context['passe'] = passe1
    context['form'] = form
    context['person'] = person
    context['passe'] = passe
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/personne/update_person.html', context)


@login_required
def delete_personne(request, pk, passe=None):
    is_delete = False
    context = dict()
    person =None
    passe1 = passe
    context = dict()
    request.session['passe'] = passe1
    try:
        person = Person.objects.get(id=pk)
    except Person.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['personne_delete'] = {
            'id': person.id,
            'nom_et_prenom': str(person.nom_et_prenom)
        }
        History.objects.create(
            user=request.user,
            content_object=f"{person}",
            action_type="suppresion de"
        )
        person.delete()
        is_delete = True
        request.session['is_delete'] = is_delete
        if passe1:
            return redirect('rempl:liste_site')
        else:
            return redirect('rempl:index_rempl')

    if request.session.get('passe'):
        print(request.session.get('passe'))
        context['passe'] = request.session.get('passe')
    context['person'] = person
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/personne/delete_person.html', context)


@login_required
def detail_personne(request, pk):
    personne = None
    data = dict()
    personne = get_object_or_404(Person, pk=pk)
    context = {'personne': personne}
    data['detail_personne'] = render_to_string('remplissages/modal/person-detail.html', context, request=request)
    return JsonResponse(data)

#==============================================================================================================
#===============================CRUD SITE======================================
@login_required
def add_site(request):
    is_save = False
    context = dict()

    form = SiteForm(request.POST, files=request.FILES or None)
    if form.is_valid():
        site = form.save(commit=False)
        site.author = request.user
        site.save()
        History.objects.create(
            user=request.user,
            content_object=f"LIEU D'ÉVANGELISATION:::{site}",
            action_type="ajout de"
        )
        is_save = True
        request.session['is_save'] = is_save
        request.session['site_ajout'] = {'nom':site.nom_site_evangelisation}
        return redirect('rempl:liste_site')
    context['form'] = form
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/site/add_site.html',context)


@login_required
def change_site(request, pk):
    site = None
    is_update = False
    form = None
    context = dict()
    try:
        site = Site.objects.get(id=pk)
    except Site.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method == 'POST':
        form = SiteForm(instance=site, data=request.POST, files=request.FILES)
        if form.is_valid():
            site = form.save(commit=False)
            site.save()
            History.objects.create(
                user=request.user,
                content_object=f"LIEU D'ÉVANGELISATION:::{site}",
                action_type="mise à jour de"
            )
            is_update = True
            context['is_update'] = is_update 
            request.session['is_update'] = is_update
            request.session['site_update'] = {'nom':site.nom_site_evangelisation}
            return redirect('rempl:liste_site')
    else:
        form = SiteForm(instance=site)
    context['form'] = form
    context['site'] = site
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/site/update_site.html', context)


@login_required
def delete_site(request, pk):
    is_delete = False
    context = dict()
    site =None
    try:
        site = Site.objects.get(id=pk)
    except Site.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['site_delete'] = {'id': site.id,'nom': str(site.nom_site_evangelisation)}
        History.objects.create(
            user=request.user,
            content_object=f"LIEU D'ÉVANGELISATION:::{site}",
            action_type="suppresion de"
        )
        site.delete()
        is_delete = True
        request.session['is_delete'] = is_delete
        return redirect('rempl:liste_site')

    context = {'site':site}
    active = "index_rempl"
    context['active'] = active
    return render(request, 'remplissages/site/delete_site.html', context)


@login_required
def liste_site_evang(request):
    context = dict()
    sites =None
    sites = Site.objects.all()
    evangs = Evangelisation.objects.all()
    
    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']
    
    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')

    if request.session.get('is_update_list'):
        context['is_update'] = request.session.get('is_update_list')
        del request.session['is_update_list']

    if request.session.get('personne'):
        context['personne'] = request.session.get('personne')

    if request.session.get('personne_delete'):
        context['personne_delete'] = request.session.get('personne_delete')
        del request.session['personne_delete']
    
    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']

    if request.session.get('personne_nom_passe'):
        context['personne_nom_passe'] = request.session.get('personne_nom_passe')

    #============EVANG CRUD SESSION=====================================
    if request.session.get('evang_ajouter'):
        context['evang_ajouter'] = request.session.get('evang_ajouter')
        del request.session['evang_ajouter']#
    
    if request.session.get('evang_update'):
        context['evang_update'] = request.session.get('evang_update')
        del request.session['evang_update']#
    
    if request.session.get('evang_delete'):
        context['evang_delete'] = request.session.get('evang_delete')
        del request.session['evang_delete']#
    
    #============SITE CRUD SESSION=====================================
    if request.session.get('site_ajout'):
        context['site_ajout'] = request.session.get('site_ajout')
        del request.session['site_ajout']#
    
    if request.session.get('site_update'):
        context['site_update'] = request.session.get('site_update')
        del request.session['site_update']#
    
    if request.session.get('site_delete'):
        context['site_delete'] = request.session.get('site_delete')
        del request.session['site_delete']#


    active = "index_rempl"
    context['active'] = active
    context['sites'] = sites
    context['evangs'] = evangs
    return render(request, 'remplissages/site/sites.html', context)
