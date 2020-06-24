from django.urls import path

from . import views

app_name = 'randwordly'
urlpatterns = [
    path('', views.index, name='random'),
    path('add_favorite', views.add_to_liste, name='add_favorite'),
]