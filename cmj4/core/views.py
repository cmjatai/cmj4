from random import random

from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render

from cmj4.core.models import Teste


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:

    context = {
        "django_message": "Hello from Django!",
        "vue_message": "This message has been passed to a Vue component from a Django view.",
        "initial_value": 1000
    }
    

    return render(request, "index.html", context)


def teste(request: HttpRequest) -> JsonResponse:

    teste = Teste()
    teste.teste = str(random())
    teste.save()

    return JsonResponse(model_to_dict(teste))
