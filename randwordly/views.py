from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mot, Definition, ListeApprentissage
from django.contrib.auth.models import User

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
            random_liste_creation = ListeApprentissage(utilisateur=request.user, nom="random", mot=Mot.objects.get(pk=1))
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

    ListeApprentissage.objects.create(
            utilisateur=request.user,
            nom=request.POST.get("listes"),
            mot=word.first()
            ).save()
    return HttpResponse(status=200)