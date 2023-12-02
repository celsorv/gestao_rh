import csv
import json

import xlwt
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


class ExportarParaCSV(View):
    def get(self, request):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
        )

        registro_he = RegistroHoraExtra.objects.filter(utilizada=False)

        writer = csv.writer(response)
        writer.writerow(["id", "motivo", "funcionario", "horas", "saldo"])

        for registro in registro_he:
            writer.writerow([
                registro.id,
                registro.motivo,
                registro.funcionario,
                registro.horas,
                registro.funcionario.total_horas_extras,
            ])

        return response


class ExportarExcel(View):
    def get(self, request):
        response = HttpResponse(
            content_type="application/ms-excel",
            headers={
                "Content-Disposition":
                'attachment; filename="meu_relatorio_excel.xls"'
            },
        )

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Banco de Horas")

        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font_bold = True

        columns = ["id", "motivo", "funcionario", "horas", "saldo"]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        registros = RegistroHoraExtra.objects.filter(utilizada=False)

        row_num = 1
        for registro in registros:
            nome = registro.funcionario.nome
            saldo = registro.funcionario.total_horas_extras
            ws.write(row_num, 0, registro.id, font_style)
            ws.write(row_num, 1, registro.motivo, font_style)
            ws.write(row_num, 2, nome, font_style)
            ws.write(row_num, 3, saldo, font_style)
            ws.write(row_num, 4, registro.horas, font_style)
            row_num += 1

        wb.save(response)
        return response
