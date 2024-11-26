# Generated by Django 5.1.2 on 2024-11-26 15:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0009_session_maximum_participant'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='joined_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]