# Generated by Django 4.1.4 on 2023-01-06 19:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analyze', '0002_rename_rateup_five_stars_weaponbanner_rateups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='characterbanner',
            name='enddate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weaponbanner',
            name='enddate',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
