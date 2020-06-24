from django.contrib import admin

# Register your models here.
from .models import Mot, Definition

admin.site.register(Mot)
admin.site.register(Definition)
