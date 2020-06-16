from django.urls import path

from . import views

app_name = 'randwordly'
urlpatterns = [
    path('', views.index, name='random'),
]