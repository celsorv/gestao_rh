import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)

from .forms import RegistroHoraExtraForm
from .models import RegistroHoraExtra


class HoraExtraList(ListView):
    model = RegistroHoraExtra

    def get_queryset(self):
        if (hasattr(self.request.user, 'funcionario')
                and self.request.user.funcionario is not None):
            empresa_logada = self.request.user.funcionario.empresa
            return RegistroHoraExtra.objects.filter(
                funcionario__empresa=empresa_logada
            )
        else:
            return RegistroHoraExtra.objects.none()


class HoraExtraEdit(UpdateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        # obtém os argumentos padrão que seriam passados ao formulário
        kwargs = super(HoraExtraEdit, self).get_form_kwargs()

        # atualiza o dicionário de argumentos do formulário
        # incluindo um novo par chave-valor, no caso, user
        kwargs.update({"user": self.request.user})

        # retorna o dicionário de argumentos atualizado
        return kwargs


class HoraExtraDelete(DeleteView):
    model = RegistroHoraExtra
    success_url = reverse_lazy('list_hora_extra')  # volta para a listagem


class HoraExtraNovo(CreateView):
    model = RegistroHoraExtra
    form_class = RegistroHoraExtraForm

    def get_form_kwargs(self):
        # obtém os argumentos padrão que seriam passados ao formulário
        kwargs = super(HoraExtraNovo, self).get_form_kwargs()

        # atualiza o dicionário de argumentos do formulário
        # incluindo um novo par chave-valor, no caso, user
        kwargs.update({"user": self.request.user})

        # retorna o dicionário de argumentos atualizado
        return kwargs


# class UtilizouHoraExtra(View):
#     def post(self, *args, **kwargs):
#         registro_hora_extra = RegistroHoraExtra.objects.get(id=kwargs['pk'])
#         registro_hora_extra.utilizada = True
#         registro_hora_extra.save()
#
#         funcionario = self.request.user.funcionario
#
#         response = json.dumps({
#             "mensagem": "Requisição executada",
#             "horas": float(funcionario.total_horas_extras)
#         })
#
#         return HttpResponse(response, content_type="application/json")

class UtilizouHoraExtra(View):
    def post(self, request, pk):
        registro_hora_extra = get_object_or_404(RegistroHoraExtra, id=pk)
        registro_hora_extra.utilizada = True
        registro_hora_extra.save()

        funcionario = request.user.funcionario

        response_data = {
            "mensagem": "Requisição executada",
            "horas": float(funcionario.total_horas_extras)
        }

        return JsonResponse(response_data)


class NaoUtilizouHoraExtra(View):
    def post(self, request, pk):
        registro_hora_extra = get_object_or_404(RegistroHoraExtra, id=pk)
        registro_hora_extra.utilizada = False
        registro_hora_extra.save()

        funcionario = request.user.funcionario

        response_data = {
            "mensagem": "Requisição executada",
            "horas": float(funcionario.total_horas_extras)
        }

        return JsonResponse(response_data)
