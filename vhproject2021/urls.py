from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts import views
from . import views as hone_views

urlpatterns = [
    path('', hone_views.index, name="index_hone"),
    path('vh-cam-yde/tu-dois-etre-sauver', views.tu_dois_etre_sauver, name="tu_dois_etre_sauver"),
    path('vh-cam-yde/', include('accounts.urls', namespace='accounts')),
    path('vh-cam-yde/remplissages/', include('remplissages.urls', namespace='rempl')),
    path('vh-cam-yde/suivie/', include('suivie.urls', namespace='suivie')),
    path('vh-cam-yde/rapport/', include('rapport.urls', namespace='rapport')),
    path('vh-cam-yde/gallerie/', include('gallerie.urls', namespace='gallerie')),

    path('admin/', admin.site.urls),
]
#urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
