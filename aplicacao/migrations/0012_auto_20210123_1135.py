# Generated by Django 3.1 on 2021-01-23 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0011_auto_20210123_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caixa',
            name='data',
            field=models.DateTimeField(),
        ),
    ]
