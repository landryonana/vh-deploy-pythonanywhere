from history.models import History
from django.http.response import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm


from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from remplissages.models import Profile



def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
            if user is not None:
                login(request, user)
                History.objects.create(
                    user=user,
                    content_object=f"{user} c'est connecté le {user.last_login}",
                    action_type="connection"
                )
                return redirect('index_hone')
            else:
                print("==========tu_dois_etre_sauver")
                return redirect('tu_dois_etre_sauver')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def tu_dois_etre_sauver(request):
    return render(request, 'tu_dois_etre_sauver.html')


@login_required
def user_logout(request):
    History.objects.create(
        user=request.user,
        content_object=f"{request.user} c'est déconnecté",
        action_type="déconnection"
    )
    logout(request)
    return redirect('accounts:user_login')



@login_required
def param(request):
    context = dict()
    user = None
    user = request.user
    context['user'] = user
    context['active'] = "index_hone"

    if request.session.get('is_update'):
        context['is_update'] = request.session.get('is_update')
        del request.session['is_update']

    if request.session.get('is_add'):
        context['is_add'] = request.session.get('is_add')
        del request.session['is_add']
    
    if request.session.get('user_prof'):
        context['user_prof'] = request.session.get('user_prof')
        del request.session['user_prof']
    
    return render(request ,'account/settings.html', context)


@login_required
def users(request):
    users = User.objects.all()
    context = dict()
    if request.session.get('user_delete'):
        context['user_delete'] = request.session.get('user_delete')
        del request.session['user_delete']
    context['users'] = users
    context['active'] = "index_hone"
    return render(request, 'account/users.html', context)



@login_required
def user_register(request):
    form = None
    is_add = False
    context = dict()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            new_boss = form.save(commit=False)
            new_boss.is_staff = False
            new_boss.is_active = True
            new_boss.set_password(form.cleaned_data['password'])
            new_boss.save()
            History.objects.create(
                user=request.user,
                content_object=f"COMPTE:::Utilisateur: {new_boss}",
                action_type="ajout de"
            )
            Profile.objects.create(user=new_boss)
            History.objects.create(
                user=request.user,
                content_object=f"COMPTE:::Utilisateur:: profile a: {new_boss}",
                action_type="ajout de"
            )
            is_add = True
            request.session['is_add'] = is_add
    else:
        form = UserRegistrationForm()
    context['active'] = "index_hone"
    context['form'] = form
    context['is_add'] = is_add
    return render(request, 'account/add_user.html', context)


@login_required
def user_edit(request):
    user_form = None
    profile_form = None
    is_update = False
    context = dict()
    if request.method == 'POST':
        user_form = UserEditForm(
                instance=request.user,
                data=request.POST, files=request.FILES)
        profile_form = ProfileEditForm(
                instance=request.user.profile,
                data=request.POST,
                files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            History.objects.create(
                user=request.user,
                content_object=f"COMPTE:::Utilisateur",
                action_type="mise à jour de"
            )
            is_update = True
            request.session['is_update'] = is_update
            request.session['user_prof'] = {'username':request.user.username}
            return redirect('accounts:param')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context['active'] = "index_hone"
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    context['is_update'] = is_update
    return render(request, 'account/update_user.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update passeword in session
            return redirect('accounts:password_change_done')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/password_change_form.html', {
        'form': form
    })


@login_required
def password_change_done(request):
    return render(request, 'account/password_change_done.html')


@login_required
def user_delete(request, pk):
    context = dict()
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        raise Http404("Pages non disponible")
    if request.method=='POST':
        request.session['user_delete'] = {'id': user.id,'nom': str(user.username)}
        History.objects.create(
            user=request.user,
            content_object=f"COMPTE:::{user}",
            action_type="suppresion de"
        )
        user.delete()
        request.session['is_delete'] = True
        return redirect('accounts:users')

    context['user'] = user
    return render(request, 'account/user_delete.html', context)


@login_required
def user_detail(request, pk):
    user = None
    data = dict()
    user = get_object_or_404(User, pk=pk)
    context = {'user': user}
    data['detail_user'] = render_to_string('account/account_modal/user-detail.html', context, request=request)
    return JsonResponse(data)