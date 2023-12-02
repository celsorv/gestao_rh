from django.db import models
from django.urls import reverse

from apps.funcionarios.models import Funcionario


class RegistroHoraExtra(models.Model):
    motivo = models.CharField(max_length=100, help_text='Motivo Hora Extra')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    horas = models.DecimalField(max_digits=5, decimal_places=2)
    utilizada = models.BooleanField(default=False)

    def get_absolute_url(self):
        # após atualizar o models, fica no formulário
        return reverse('update_hora_extra', args=[self.id])

    def __str__(self):
        return self.motivo
