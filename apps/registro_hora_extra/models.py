from django.db import models

from apps.funcionarios.models import Funcionario


class RegistroHoraExtra(models.Model):
    motivo = models.CharField(max_length=100, help_text='Motivo Hora Extra')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)

    def __str__(self):
        return self.motivo
