from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from .models import Departamento


class DepartamentosList(ListView):
    model = Departamento

    def get_queryset(self):
        if (hasattr(self.request.user, 'funcionario')
                and self.request.user.funcionario is not None):

            # se usuário logado tem funcionário vinculado
            # filtra departamentos dessa empresa apenas
            empresa_logada = self.request.user.funcionario.empresa
            return Departamento.objects.filter(empresa=empresa_logada)

        else:
            # não retorna nada
            return Departamento.objects.none()


class DepartamentoCreate(CreateView):
    model = Departamento
    fields = ['nome']

    def form_valid(self, form):
        departamento_criado = form.save(commit=False)

        # se funcionário logado é vinculado a uma empresa,
        # atribui a empresa dele ao novo departamento
        departamento_criado.empresa = getattr(self.request.user.funcionario, 'empresa', None)

        departamento_criado.save()
        return super(DepartamentoCreate, self).form_valid(form)


class DepartamentoUpdate(UpdateView):
    model = Departamento
    fields = ['nome']


class DepartamentoDelete(DeleteView):
    model = Departamento
    success_url = reverse_lazy('list_departamentos')  # volta para a listagem
