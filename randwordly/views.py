from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mot, Definition
import random

@csrf_exempt
def index(request):
    number_checked = []
    definitions = []
    random_definitions = []
    word_id = random.randint(1, 353817)
    number_checked.append(word_id)
    word = Mot.objects.filter(pk=word_id).first()
    definition = str(Definition.objects.filter(mot=word_id).first()).capitalize()
    definitions.append({"description" : definition, "right_answer" : True})
    #Right definition

    while len(number_checked) < 4 and word_id in number_checked:
        word_id = random.randint(1, 353817)
        if word_id not in number_checked:
            definition = Definition.objects.filter(mot=word_id).first()
            definitions.append({"description" :  str(definition).capitalize()})
            number_checked.append(word_id)

    for turn in range(len(definitions)):
        choice_id = random.choice(list(enumerate(definitions)))[0]
        random_definitions.append(definitions.pop(choice_id))

    context = {"word":str(word).capitalize(), "definitions":random_definitions}

    if request.method == 'POST':
        return JsonResponse(context)

    return render(request, 'randwordly/main.html', context)