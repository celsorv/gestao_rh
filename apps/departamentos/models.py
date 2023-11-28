from django.db import models
from django.urls import reverse

from apps.empresas.models import Empresa


class Departamento(models.Model):
    nome = models.CharField(
        max_length=70, help_text='Nome do departamento'
    )

    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse('list_departamentos')

    def __str__(self):
        return self.nome
