# Generated by Django 5.1.2 on 2024-11-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0002_address_category_enroll_learner_session_transaction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_date_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]