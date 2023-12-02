from io import BytesIO

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
    CreateView
)
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["origem"] = "funcionario"
        return context


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
        funcionario_criado.empresa = getattr(
            self.request.user.funcionario, 'empresa', None
        )

        funcionario_criado.user = User.objects.create(username=username)

        funcionario_criado.save()
        return super(FuncionarioNovo, self).form_valid(form)


def create_pdf(funcionarios):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    end_x = width

    # Adicione cabeçalho
    p.drawString(200, height - 50, "Relatório de Funcionários")
    p.line(x1=0, y1=height - 60, x2=end_x, y2=height - 60)

    # Adicione detalhes dos funcionários
    strlin = "Nome: %s | Hora Extra: %.2f"

    y_start = height - 80
    line_height = 20

    for index, funcionario in enumerate(funcionarios):
        y = y_start - index * line_height
        p.drawString(10, y, strlin % (funcionario.nome,
                                      funcionario.total_horas_extras)
                     )

    # Adicione número da página
    page_number_text = "Página %d" % p.getPageNumber()
    p.drawRightString(end_x - 10, 30, page_number_text)

    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data


def relatorio_funcionarios(request):

    if (hasattr(request.user, 'funcionario')
            and request.user.funcionario is not None):
        empresa_logada = request.user.funcionario.empresa
        funcionarios = Funcionario.objects.filter(empresa=empresa_logada)
    else:
        funcionarios = Funcionario.objects.none()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'

    # Chame a função para criar o PDF passando os funcionários
    pdf_data = create_pdf(funcionarios)

    # Escreva os dados binários diretamente na resposta
    response.write(pdf_data)

    return response

# Primeiro teste básico
# -------------------------------------
# def pdf_reportlab(request):
#     response = HttpResponse(content_type="application/pdf")
#
#     # Content-Disposition garante faz com que o arquivo seja baixado
#     response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
#
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer)
#
#     p.drawString(10, 810, "Hello world.")
#
#     palavras = ["palavra1", "palavra2", "palavra3"]
#
#     y = 790
#     for palavra in palavras:
#         p.drawString(10, y, palavra)
#         y -= 40
#
#     p.showPage()
#     p.save()
#
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#
#     return response


# Segundo teste imprimindo funcionários
# -------------------------------------
# def pdf_reportlab(request):
#     response = HttpResponse(content_type="application/pdf")
#
#     # Content-Disposition garante faz com que o arquivo seja baixado
#     response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
#
#     buffer = io.BytesIO()
#     p = canvas.Canvas(buffer, pagesize=A4)
#
#     width, height = A4
#     end_x = width
#
#     p.drawString(200, 810, "Relatório de funcionários")
#     p.line(x1=0, y1=800, x2=end_x, y2=800)
#
#     strlin = "Nome: %s | Hora Extra: %2.f"
#
#     funcionarios = Funcionario.objects.all()
#
#     y = 750
#     for funcionario in funcionarios:
#         p.drawString(10, y, strlin % (
#             funcionario.nome, funcionario.total_horas_extras
#         ))
#         y -= 20
#
#     p.showPage()
#     p.save()
#
#     pdf = buffer.getvalue()
#     buffer.close()
#     response.write(pdf)
#
#     return response
