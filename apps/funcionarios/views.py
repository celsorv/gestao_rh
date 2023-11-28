from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)

from .models import Funcionario


class FuncionariosList(ListView):
    model = Funcionario

    def get_queryset(self):
        if (hasattr(self.request.user, 'funcionario')
                and self.request.user.funcionario is not None):
            empresa_logada = self.request.user.funcionario.empresa
            return Funcionario.objects.filter(empresa=empresa_logada)
        else:
            return Funcionario.objects.none()


class FuncionarioEdit(UpdateView):
    model = Funcionario
    fields = ['nome', 'departamentos']


class FuncionarioDelete(DeleteView):
    model = Funcionario
    success_url = reverse_lazy('list_funcionarios')  # volta para a listagem


class FuncionarioNovo(CreateView):
    model = Funcionario
    fields = ['nome', 'departamentos']

    def form_valid(self, form):
        funcionario_criado = form.save(commit=False)

        name_split = funcionario_criado.nome.split(' ')
        username = ''.join(name_split)

        # se funcionário logado é vinculado a uma empresa,
        # atribui a empresa dele ao novo funcionário
        funcionario_criado.empresa = getattr(self.request.user.funcionario, 'empresa', None)

        funcionario_criado.user = User.objects.create(username=username)

        funcionario_criado.save()
        return super(FuncionarioNovo, self).form_valid(form)
