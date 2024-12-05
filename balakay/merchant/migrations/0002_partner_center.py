# Generated by Django 5.1.2 on 2024-11-23 16:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0009_center_partner'),
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='center',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partners', to='centers.center'),
        ),
    ]
