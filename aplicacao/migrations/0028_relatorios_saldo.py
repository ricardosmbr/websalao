# Generated by Django 3.1.4 on 2022-03-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0027_auto_20211106_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatorios',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
