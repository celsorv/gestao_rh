# Generated by Django 4.2.7 on 2023-11-28 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0001_initial'),
        ('documentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='arquivo',
            field=models.FileField(default='', upload_to='documentos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='documento',
            name='pertence',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='funcionarios.funcionario'),
        ),
    ]