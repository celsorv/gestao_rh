from django.forms import ModelForm

from apps.funcionarios.models import Funcionario
from .models import RegistroHoraExtra


class RegistroHoraExtraForm(ModelForm):

    def __init__(self, user, *args, **kwargs):

        # apenas executa o método __init__ da superclasse
        super(RegistroHoraExtraForm, self).__init__(*args, **kwargs)

        # redefine os registros de fields['funcionario']
        # somente com os funcionários da empresa logada
        #
        if hasattr(user, "funcionario") and user.funcionario is not None:
            self.fields["funcionario"].queryset = Funcionario.objects.filter(
                empresa=user.funcionario.empresa
            )
        else:
            self.fields["funcionario"].queryset = Funcionario.objects.all()

    class Meta:
        model = RegistroHoraExtra
        fields = ['motivo', 'funcionario', 'horas']
