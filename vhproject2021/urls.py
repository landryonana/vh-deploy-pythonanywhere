from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from . import views as hone_views

urlpatterns = [
    path('evangelisation', hone_views.index, name="index_hone"),
    path('tu-dois-etre-sauver', views.tu_dois_etre_sauver, name="tu_dois_etre_sauver"),
    path('evangelisation/compte/', include('accounts.urls', namespace='accounts')),
    path('evangelisation/remplissages/', include('remplissages.urls', namespace='rempl')),
    path('evangelisation/suivie/', include('suivie.urls', namespace='suivie')),
    path('evangelisation/rapport/', include('rapport.urls', namespace='rapport')),
    path('evangelisation/gallerie/', include('gallerie.urls', namespace='gallerie')),

    path('admin/', admin.site.urls),
]
urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
