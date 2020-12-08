from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Mot, Definition, ListeApprentissage, MotListe
from django.contrib.auth.models import User
from django.urls import reverse

import random
import json

@csrf_exempt
def index(request):
    context = {}
    number_checked = []
    definitions = []
    random_definitions = []
    listes = []

    word_id = random.randint(1, 9000)
    number_checked.append(word_id)
    word = Mot.objects.filter(pk=word_id).first()
    context["word"] = word
    definition = str(Definition.objects.filter(mot=word_id).first()).capitalize()
    definitions.append({"description" : definition, "right_answer" : True})
    #Right definition

    if request.user.is_authenticated:
        user_liste = set([l.nom for l in ListeApprentissage.objects.filter(utilisateur=request.user.id)])
        if "random" not in user_liste:
            random_liste_creation = ListeApprentissage(utilisateur=request.user, nom="random")
            random_liste_creation.save()
            user_liste = set([l.nom for l in ListeApprentissage.objects.filter(utilisateur=request.user.id)])
        context["listes"] = list(user_liste)

    while len(number_checked) < 4 and word_id in number_checked:
        word_id = random.randint(1, 9000)
        if word_id not in number_checked:
            definition = Definition.objects.filter(mot=word_id).first()
            definitions.append({"description" :  str(definition).capitalize()})
            number_checked.append(word_id)

    for turn in range(len(definitions)):
        choice_id = random.choice(list(enumerate(definitions)))[0]
        random_definitions.append(definitions.pop(choice_id))

    context["definitions"] = random_definitions

    if request.method == 'POST':
        context["word"] = str(word)
        return JsonResponse(context)

    return render(request, 'randwordly/main.html', context)

@csrf_exempt
def add_to_liste(request):
    word = Mot.objects.filter(id=request.POST.get("word_id"))
    list_exist = ListeApprentissage.objects.filter(utilisateur=request.user, nom=request.POST.get("listes"))
    if not word or not list_exist:
        return HttpResponse(status=400)

    liste = ListeApprentissage.objects.get(nom=request.POST.get("listes"))
    MotListe.objects.create(
            liste_id=liste.id,
            mot_id=word.first().id
            ).save()
    return HttpResponse(status=200)

@login_required
def manage_account(request, username):
    return render(request, 'randwordly/account.html')

@csrf_exempt
@login_required
def manage_list(request, username):
    root = User.objects.get(id=1)
    user_listes = listes = [liste["nom"] for liste in ListeApprentissage.objects.filter(utilisateur=request.user).values('nom').distinct()]
    listes = [liste["nom"] for liste in ListeApprentissage.objects.filter(utilisateur=root).values('nom').distinct()]
    context = {"listes":sorted(listes), "user_listes":user_listes}
    if request.POST:
        alreay_exist = ListeApprentissage.objects.filter(nom=request.POST.get("new_list_name"))
        if alreay_exist:
            context["post_response"] = "liste existe déjà"
            return render(request, 'randwordly/liste.html', context)

        ListeApprentissage.objects.create(
                    utilisateur = request.user,
                    nom = request.POST.get("new_list_name"),
                    ).save()
        for liste in request.POST.getlist("list_chosen"):
            new_liste = ListeApprentissage.objects.get(nom=request.POST.get("new_list_name"))
            liste = ListeApprentissage.objects.get(nom=liste)
            words_in_liste = MotListe.objects.filter(liste_id=liste.id)
            for word in words_in_liste:
                MotListe.objects.create(
                    mot_id = word.mot_id,
                    liste_id = new_liste.id,
                    ).save()
        context["post_response"] = "liste ajoutée"
        context["user_listes"] = [liste["nom"] for liste in ListeApprentissage.objects.filter(utilisateur=request.user).values('nom').distinct()]
        return render(request, 'randwordly/liste.html', context)

    else:
        return render(request, 'randwordly/liste.html', context)