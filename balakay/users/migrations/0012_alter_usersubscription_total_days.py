# Generated by Django 5.1.2 on 2024-11-01 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_usersubscription_total_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersubscription',
            name='total_days',
            field=models.PositiveIntegerField(),
        ),
    ]
