# Generated by Django 4.1.4 on 2023-04-08 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genshinwishoracle', '0002_primogemrecord_primogemsnapshot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='primogemsnapshot',
            name='associated_record',
        ),
        migrations.DeleteModel(
            name='PrimogemRecord',
        ),
        migrations.DeleteModel(
            name='PrimogemSnapshot',
        ),
    ]
