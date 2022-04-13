# Generated by Django 4.0.3 on 2022-04-08 16:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('games_rental', '0017_alter_customergamerent_return_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customergamerent',
            name='return_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='customergamerent',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]