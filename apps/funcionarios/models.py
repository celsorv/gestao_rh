from django.db import models


class Funcionario(models.Model):
    nome = models.CharField(max_length=100, help_text='Nome do funcionário')

    def __str__(self):
        return self.nome