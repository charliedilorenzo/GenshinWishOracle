# Generated by Django 4.1.4 on 2023-04-08 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_primogem_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primogemsnapshot',
            name='associated_record',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.primogemrecord'),
        ),
    ]
