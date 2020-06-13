from django.contrib import admin

# Register your models here.
from .models import Mot, Definition, Utilisateur

admin.site.register(Mot)
admin.site.register(Definition)
admin.site.register(Utilisateur)
