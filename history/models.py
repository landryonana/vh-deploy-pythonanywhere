from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from remplissages.models import Site, Evangelisation, Suivie, Person, Image, Profile


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content_object = models.CharField(max_length=200)
    action_type = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created',)

    def __str__(self):
        return f"{self.action_type} {self.content_object} par {self.user} à {self.created}"
