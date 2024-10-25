from random import random

from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render

from cmj4.core.models import Teste
from cmj4.core.tasks import debug_task


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:

    context = {
        "django_message": "Hello from Django!",
        "vue_message": "This message has been passed to a Vue component from a Django view.",
        "initial_value": 1000
    }
    

    return render(request, "index.html", context)


def teste(request: HttpRequest) -> JsonResponse:

    teste = Teste.objects.order_by('id').last() or Teste()

    debug_task.apply_async((), countdown = 5)

    return JsonResponse(dict(
        message = 'ultimo cadastrado. task chamada para criar novo',
        teste = model_to_dict(teste)
        ))
