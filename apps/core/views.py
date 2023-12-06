from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .tasks import send_relatorio


@login_required
def home(request):
    data = {}

    # cria uma variável "usuário" acessível no HTML
    data["usuario"] = request.user

    return render(request, "core/index.html", data)


def celery(request):
    # tarefa enviada à fila para execução assíncrona
    send_relatorio.delay()

    # navegador não fica travado aguardando a execução
    return HttpResponse("Tarefa incluída na fila para execução")
