# Generated by Django 3.1 on 2021-01-30 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacao', '0015_produto'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='agenda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='aplicacao.agendaservico'),
        ),
    ]
