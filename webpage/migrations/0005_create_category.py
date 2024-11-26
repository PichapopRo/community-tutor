# Generated by Django 5.1.2 on 2024-11-26 08:23

from django.db import migrations


def create_default_categories(apps, schema_editor):
    Category = apps.get_model('webpage', 'Category')
    categories = [
        "Yoga",
        "House work",
        "Gardening",
        "Cooking",
        "Languages",
    ]
    for category_name in categories:
        Category.objects.get_or_create(category_name=category_name)


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0004_userinfo_date_of_birth'),
    ]

    operations = [
    ]