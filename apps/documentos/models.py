from django.db import models
from django.urls import reverse

from apps.funcionarios.models import Funcionario


class Documento(models.Model):
    descricao = models.CharField(
        max_length=100, help_text='Descrição do Documento'
    )
    pertence = models.ForeignKey(Funcionario, on_delete=models.PROTECT)

    # upload para a pasta documentos
    arquivo = models.FileField(upload_to="documentos")

    def get_absolute_url(self):
        # indica para onde ir depois da atualização do models
        # nesse caso, volta ao funcionário em edição
        return reverse("update_funcionario", args=[self.pertence.id])

    def __str__(self):
        return self.descricao
