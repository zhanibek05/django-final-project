# Generated by Django 5.1.2 on 2024-10-31 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_usersubscription_daily_visits_limit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscription',
            name='remaining_freeze_days',
        ),
    ]
