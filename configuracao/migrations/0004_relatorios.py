# Generated by Django 3.1.4 on 2021-10-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracao', '0003_delete_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relatorios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ini', models.DateField()),
                ('data_fim', models.DateField()),
            ],
        ),
    ]