from django.contrib import admin

from remplissages.models import Evangelisation,  Person, Site, Suivie, Image



admin.site.register(Evangelisation)
admin.site.register(Person)
admin.site.register(Site)
admin.site.register(Image)
admin.site.register(Suivie)
