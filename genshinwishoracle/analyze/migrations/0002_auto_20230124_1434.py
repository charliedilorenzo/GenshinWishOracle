# Generated by Django 4.1.4 on 2023-01-24 19:34

from django.db import migrations
from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "initial_data.json")

class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0001_initial'),
    ]

    operations = [
    ]