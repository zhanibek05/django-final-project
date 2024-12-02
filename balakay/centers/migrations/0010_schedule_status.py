# Generated by Django 5.1.2 on 2024-12-02 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('centers', '0009_center_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('cancelled', 'Cancelled')], default='active', max_length=20),
        ),
    ]
