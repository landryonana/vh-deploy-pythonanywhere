from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from history.models import History



@login_required
def index(request):
    context = dict()
    user = request.user
    if user is not None:
        if user.is_superuser:
            histories = History.objects.all()
        else:
          histories = History.objects.filter(user=user) 
    context['active'] = "index_hone"
    context['histories'] = histories
    return render(request, 'index.html', context)

