# Create your tasks here

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.funcionarios.models import Funcionario


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def send_relatorio():
    total = Funcionario.objects.all().count()

    source_address = settings.EMAIL_HOST_USER
    target_address = settings.EMAIL_TARGET_ADDRESS

    send_mail(
        "Relatório Celery",
        "Relatório geral de funcionários %f" % total,
        source_address,
        [target_address],
        fail_silently=False
    )

    return True
