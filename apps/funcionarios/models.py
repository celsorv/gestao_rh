from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

from apps.departamentos.models import Departamento
from apps.empresas.models import Empresa


class Funcionario(models.Model):
    nome = models.CharField(
        max_length=100, help_text='Nome do funcionário'
    )

    # só deve haver um usuário ligado ao funcionário
    # user = models.ForeignKey(User, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    departamentos = models.ManyToManyField(Departamento)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.PROTECT, null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse('list_funcionarios')

    @property
    def total_horas_extras(self):
        return (
            self.registrohoraextra_set
                .all()
                .aggregate(Sum('horas'))['horas__sum']
        )

    def __str__(self):
        return self.nome
