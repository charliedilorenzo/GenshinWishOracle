# Generated by Django 4.1.4 on 2023-04-08 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='primogem_record',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.primogemrecord'),
            preserve_default=False,
        ),
    ]