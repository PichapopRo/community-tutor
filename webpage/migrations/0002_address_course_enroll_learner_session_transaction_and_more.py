# Generated by Django 5.1.1 on 2024-11-21 02:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('street_address', models.CharField(max_length=255)),
                ('sub_district', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('province', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('enroll_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learning_interests', models.ManyToManyField(to='webpage.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_date_time', models.DateTimeField()),
                ('course_description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.course')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
                ('fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learner_transactions', to=settings.AUTH_USER_MODEL)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.session')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teaching_interests', models.ManyToManyField(to='webpage.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.address')),
            ],
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AddField(
            model_name='enroll',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.session'),
        ),
        migrations.AlterUniqueTogether(
            name='enroll',
            unique_together={('user_id', 'session')},
        ),
    ]
