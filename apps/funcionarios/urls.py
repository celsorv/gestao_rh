from django.urls import path

from .views import (
    FuncionariosList,
    FuncionarioNovo,
    FuncionarioEdit,
    FuncionarioDelete,
    relatorio_funcionarios,
    Pdf,
)

urlpatterns = [
    path("", FuncionariosList.as_view(), name="list_funcionarios"),
    path("novo/", FuncionarioNovo.as_view(), name="create_funcionario"),
    path("editar/<int:pk>/", FuncionarioEdit.as_view(), name="update_funcionario"),
    path("delete/<int:pk>/", FuncionarioDelete.as_view(), name="delete_funcionario"),
    path("relatorio-funcionarios/", relatorio_funcionarios, name="relatorio_funcionarios"),
    path("relatorio-funcionarios-html/", Pdf.as_view(), name="relatorio_funcionarios_html"),
]
