# Generated by Django 3.1.4 on 2021-10-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0023_auto_20211029_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatorios',
            name='nome',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
