# Generated by Django 5.1.3 on 2024-11-26 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0011_remove_transaction_duration_session_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='fee',
            field=models.IntegerField(default=0),
        ),
    ]
