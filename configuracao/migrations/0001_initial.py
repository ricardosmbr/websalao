# Generated by Django 3.1 on 2020-11-09 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=15)),
                ('telefone', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Dias_semana',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(choices=[('SEGUNDA', 'Segunda-feira'), ('TERÇA', 'Terça_feira'), ('QUARTA', 'Quarta-feira'), ('QUINTA', 'Quinta-feira'), ('SEXTA', 'Sexta-feira'), ('SABADO', 'Sábado'), ('Domingo', 'Domingo')], max_length=50)),
                ('hora_inicio', models.TimeField(blank=True, null=True)),
                ('hora_fim', models.TimeField(blank=True, null=True)),
                ('id_configuracao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracao.configuracao')),
            ],
        ),
    ]
