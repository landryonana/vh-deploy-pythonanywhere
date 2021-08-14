from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from gallerie.forms import ImageForm, SearchForm, ImageFormUpdate
from remplissages.models import Evangelisation, Image
from history.models import History


@login_required
def gallerie_index(request):
    context = dict()
    date_req = None
    images = Image.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            date_req = form.cleaned_data['query']
            images = Image.objects.filter(publish__date=date_req)           
    else:
        form = SearchForm()

    if request.session.get('is_save'):
        context['is_save'] = request.session.get('is_save')
        del request.session['is_save']
    
    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']

    if request.session.get('is_delete'):
        context['is_delete'] = request.session.get('is_delete')
        del request.session['is_delete']

    if request.session.get('image'):
        context['image'] = request.session.get('image')
        del request.session['image']
    
    if request.session.get('image_update'):
        context['image_update'] = request.session.get('image_update')
        del request.session['image_update']

    if request.session.get('image_delete'):
        context['image_delete'] = request.session.get('image_delete')
        del request.session['image_delete']

    context['images'] = images
    context['form'] = form
    context['active'] = 'gallerie'
    context['date_req'] = date_req
    return render(request, 'gallerie/index_gallerie.html', context)



#=======================================================================================================
#=======================================================================================================
#==================================CRUD IMAGE
@login_required
def gallerie_add_image(request, pk):
    context = dict()
    images = None
    is_add = False

    evan = get_object_or_404(Evangelisation, pk=pk)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.evangelisation = evan
            image.save()
            History.objects.create(
                user=request.user,
                content_object=f"IMAGE: {image.titre} DANS {image.evangelisation}",
                action_type="ajout de"
            )
            images = evan.images.all()
            is_add = True
            request.session['is_save'] = is_add
            request.session['image'] = f"image ajouté dans {image.evangelisation} avec success"
    else:
        form = ImageForm()
        images = evan.images.all()
    context['form'] = form
    context['evan'] = evan
    context['images'] = images
    context['is_add'] = is_add
    context['active'] = 'gallerie'
    return render(request, 'gallerie/formulaire/form.html', context)



@login_required
def gallerie_add_image_gallerie(request):
    context = dict()
    is_add = False

    if request.method == 'POST':
        form = ImageFormUpdate(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            History.objects.create(
                user=request.user,
                content_object=f"IMAGE: {image.titre} DANS {image.evangelisation}",
                action_type="ajout de"
            )
            is_add = True
            request.session['is_save'] = is_add
            request.session['image'] = f"image ajouté dans {image.evangelisation} avec success"
            return redirect('gallerie:gallerie_index')
    else:
        form = ImageFormUpdate()
    context['form'] = form
    context['active'] = 'gallerie'
    return render(request, 'gallerie/formulaire/gallerie_form.html', context)



@login_required
def gallerie_update(request, pk):
    image = get_object_or_404(Image, pk=pk)
    context = dict()
    if request.method=='POST':
        form = ImageFormUpdate(instance=image, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            History.objects.create(
                user=request.user,
                content_object=f"IMAGE: {image.titre} DE {image.evangelisation}",
                action_type="mise à jour de"
            )
            request.session['is_update'] = True
            request.session['image_update'] = f"image de {image.evangelisation} modifié avec success"
            return redirect('gallerie:gallerie_index')
    else:
        form = ImageFormUpdate(instance=image)
    context['form'] = form
    context['image'] = image
    context['active'] = 'gallerie'
    return render(request, 'gallerie/formulaire/imageUpdate.html', context)


@login_required
def gallerie_delete(request, pk):
    image = get_object_or_404(Image, pk=pk)
    context = dict()
    if request.method=='POST':
        request.session['is_delete'] = True
        request.session['image_delete'] = f"image dans {image.evangelisation} a été supprimé avec success"
        History.objects.create(
            user=request.user,
            content_object=f"IMAGE: {image.titre} DANS {image.evangelisation}",
            action_type="suppresion de"
        )
        image.delete()
        return redirect('gallerie:gallerie_index')
    context['image'] = image
    context['active'] = 'gallerie'
    return render(request, 'gallerie/formulaire/imageDelete.html', context)


#=================================Modal view detail image
#=================================Modal view detail image
#=================================Modal view detail image
@login_required
def gallerie_detail_image(request, pk):
    image = None
    data = dict()
    image = get_object_or_404(Image, pk=pk)
    context = {'image': image}
    data['detail_image'] = render_to_string('gallerie/modal/image-detail.html', context, request=request)
    return JsonResponse(data)

