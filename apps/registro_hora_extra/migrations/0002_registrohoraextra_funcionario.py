# Generated by Django 4.2.7 on 2023-11-26 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0002_funcionario_departamentos_funcionario_empresa_and_more'),
        ('registro_hora_extra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrohoraextra',
            name='funcionario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='funcionarios.funcionario'),
            preserve_default=False,
        ),
    ]
