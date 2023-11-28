from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView

from .models import Empresa


class EmpresaCreate(CreateView):
    model = Empresa
    fields = ["nome"]

    def form_valid(self, form):
        empresa_criada = form.save()
        funcionario = self.request.user.funcionario

        # vincula nova empresa ao funcionario
        funcionario.empresa = empresa_criada

        funcionario.save()

        return HttpResponse("OK")


class EmpresaEdit(UpdateView):
    model = Empresa
    fields = ["nome"]
